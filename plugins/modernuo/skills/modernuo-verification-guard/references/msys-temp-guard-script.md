# MSYS temp guard script pattern

Use this when the verification guard asks for `C:/Users/Jsiem/AppData/Local/Temp/hermes-verify-*` on the Windows/MSYS host.

## Durable lesson

Creating the script with Windows Python `tempfile.mkstemp(dir='C:/Users/Jsiem/AppData/Local/Temp')` and then launching `bash <converted-path>` can fail with `No such file or directory` even when `cygpath` maps the path to `/tmp`. Avoid the cross-runtime handoff.

Create, run, and remove the script entirely from the MSYS shell instead:

```bash
set -euo pipefail
script=$(mktemp /tmp/hermes-verify-XXXXXX.sh)
native_script=$(cygpath -w "$script")
cat > "$script" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
cd 'C:/Users/Jsiem/Documents/GitHub/RebirthUO/ModernUO-issue-18'
echo "script_path=$NATIVE_SCRIPT"
echo 'verify_kind=fresh-ad-hoc-focused'
# ...status/head/diff/build/focused tests...
SH
chmod +x "$script"
echo "created_script=$native_script"
NATIVE_SCRIPT="$native_script" bash "$script"
rm -f "$script"
if [ ! -e "$script" ]; then
  echo 'script_removed=yes'
else
  echo "script_removed=no path=$native_script"
  exit 1
fi
```

## Pitfalls

- Single-quote the heredoc (`<<'SH'`) so the script body is not expanded while being written.
- Pass the native path into the script as an environment variable (`NATIVE_SCRIPT=... bash "$script"`) instead of trying to patch the file with Python string escaping.
- If cleanup runs after a failed script, capture and report the script path and cleanup result from the latest attempt only.
