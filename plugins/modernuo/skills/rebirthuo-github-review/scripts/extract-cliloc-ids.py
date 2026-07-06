#!/usr/bin/env python3
"""Extract selected cliloc IDs from modern or BWT-compressed UO Cliloc.* files.

Usage:
  python scripts/extract-cliloc-ids.py "C:/path/to/Cliloc.enu" 1151541 1151542 1152435

This is intended for RebirthUO GitHub item-property reviews where exact tooltip,
message, or long-description strings matter. It ports the ModernUO loader shape
from Projects/Server/Localization/Localization.cs and BWT decompressor from
Projects/Server/Client/BwtDecompress.cs closely enough for review extraction.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _frequency(counts: list[int]) -> list[int]:
    tmp = counts[:]
    output: list[int] = []

    for _ in range(256):
        max_value = -1
        index = 0
        for i, value in enumerate(tmp):
            if value > max_value:
                index = i
                max_value = value

        if max_value == 0:
            break

        output.append(index)
        tmp[index] = 0

    return output


def _shift_left(symbol_table: bytearray, max_index: int) -> None:
    for i in range(max_index):
        symbol_table[i] = symbol_table[i + 1]


def _internal_decompress(data: bytearray) -> bytearray:
    counts = [int.from_bytes(data[i * 4 : i * 4 + 4], "little", signed=True) for i in range(256)]
    total = sum(counts)
    non_zero_count = 256 - counts.count(0)

    symbol_table = bytearray(range(256))
    partial_input = [0] * (256 * 3)
    partial_input[:256] = counts

    frequencies = _frequency(counts)
    m = 0
    for i in range(non_zero_count):
        freq = frequencies[i]
        symbol_table[data[m + 1024]] = freq
        partial_input[freq + 256] = m + 1
        m += partial_input[freq]
        partial_input[freq + 512] = m

    value = symbol_table[0]
    output = bytearray(total)
    count = 0

    while count < total:
        first_ref = partial_input[value + 256]
        output[count] = value

        if first_ref >= partial_input[value + 512]:
            old_non_zero_count = non_zero_count
            non_zero_count -= 1
            if old_non_zero_count > 0:
                _shift_left(symbol_table, non_zero_count)
                value = symbol_table[0]
        else:
            index = data[first_ref + 1024]
            partial_input[value + 256] = first_ref + 1

            if index != 0:
                _shift_left(symbol_table, index)
                symbol_table[index] = value
                value = symbol_table[0]

        count += 1

    return output


def _bwt_decompress(raw: bytes) -> bytearray:
    first_char = raw[0]
    table: list[int] = []
    first_byte = first_char
    second_byte = 0

    for _ in range(256 * 256):
        table.append(first_byte + (second_byte << 8))
        first_byte = (first_byte + 1) & 0xFF
        if first_byte == 0:
            second_byte = (second_byte + 1) & 0xFF

    table.sort()

    output = bytearray(len(raw))
    out_index = 0
    position = 1

    while position < len(raw):
        current_value = first_char
        value = table[current_value]

        while current_value > 0:
            table[current_value] = table[current_value - 1]
            current_value -= 1

        table[0] = value
        output[out_index] = value & 0xFF
        out_index += 1
        first_char = raw[position]
        position += 1

    return _internal_decompress(output)


def _load_cliloc(path: Path) -> dict[int, str]:
    raw = path.read_bytes()

    if int.from_bytes(raw[:4], "little", signed=True) == 2 and int.from_bytes(raw[4:6], "little", signed=True) == 1:
        data = raw[6:]
    else:
        # Matches Localization.cs: skip four-byte header, decompress remaining file.
        data = _bwt_decompress(raw[4:])

    if int.from_bytes(data[:4], "little", signed=True) != 2 or int.from_bytes(data[4:6], "little", signed=True) != 1:
        raise ValueError(f"Invalid cliloc header after decompression: {path}")

    entries: dict[int, str] = {}
    position = 6

    while position + 7 <= len(data):
        number = int.from_bytes(data[position : position + 4], "little", signed=True)
        position += 4
        position += 1  # flag: original/custom/modified
        length = int.from_bytes(data[position : position + 2], "little", signed=True)
        position += 2
        text = data[position : position + length].decode("utf-8", errors="replace")
        position += length
        entries[number] = text

    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cliloc", type=Path, help="Path to Cliloc.enu/deu/... file")
    parser.add_argument("ids", nargs="+", type=int, help="Cliloc IDs to print")
    args = parser.parse_args()

    entries = _load_cliloc(args.cliloc)
    print(f"client_path={args.cliloc}")
    for number in args.ids:
        print(f"{number} = {entries.get(number)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
