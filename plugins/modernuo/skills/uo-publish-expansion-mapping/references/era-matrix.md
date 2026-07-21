# UO Publish-to-Expansion Era Matrix

Use this matrix only after checking the linked official source for the requested
Publish. The Publish ranges are RebirthUO activation policy: a Publish after one
true expansion boundary and through the next boundary maps forward to that next
named expansion. They do not claim that the target expansion was live throughout
the range.

## Matrix

| True era | Official boundary evidence | Policy Publish range | Current ModernUO gate |
| --- | --- | --- | --- |
| Base game | Predates expansion and numbered Publish boundaries | None | `Expansion.None`; no `Core` era flag |
| The Second Age (T2A) | Predates the numbered Publish sequence preserved by UO.com | None; use the official release boundary | `Core.T2A` |
| Renaissance (UOR) | Launch falls after the early dated/numbered sequence and before Publish 6 in the official 2000 archive | Unnumbered post-T2A Publishes and Publish 1-5 | `Core.UOR` |
| Third Dawn (UOTD) | Official Publish 11 introduced Ilshenar and required the Third Dawn client | Publish 6-11 | `Core.UOTD` |
| Lord Blackthorn's Revenge (LBR) | Launch falls after Publish 15.5 and before Publish 16 in the official 2002 archive | Publish 12-15.5 | `Core.LBR` |
| Age of Shadows (AOS) | Official Age of Shadows material is grouped under Publish 17 | Publish 16-17.x | `Core.AOS` |
| Samurai Empire (SE) | Launch falls after Publish 27 and before Publish 28 in the official 2004/2005 archives | Publish 18-27 | `Core.SE` |
| Mondain's Legacy (ML) | Launch falls after Publish 35 and before Publish 36 in the official 2005 archive | Publish 28-35 | `Core.ML` |
| Stygian Abyss (SA) | Official Stygian Abyss launch is Publish 60 | Publish 36-60 | `Core.SA` |
| High Seas (HS) | Official High Seas launch is Publish 68 | Publish 61-68 | `Core.HS` |
| Time of Legends (TOL) | Official worldwide Time of Legends launch is Publish 90 | Publish 69 onward | `Core.TOL` |

Treat decimal and multipart releases as part of their base Publish unless the
official notes establish a different worldwide boundary. For example, `17.3`
stays in the Publish 17/AOS row.

## Endless Journey Exception

Official Publish 99 launched Endless Journey as a free, restricted account mode.
The current official FAQ describes expansion access and purchases separately.
Therefore:

- map Publish 99 and later production Publishes to TOL under this matrix;
- do not add an EJ row as a true expansion;
- do not use `Core.EJ` as the activation gate for Publish-era behavior;
- model an EJ prohibition as a separate per-account entitlement or restriction
  only when the official mechanic requires it.

## Source Index

Official chronology:

- Previous Publishes index: https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/
- 2000 archive (UOR boundary): https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2000-2/
- Publish 11 / Third Dawn: https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2001-2/2001-publish-11-14th-march/
- 2002 archive (LBR boundary): https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2002-2/
- Publish 17 / Age of Shadows: https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2003-2/publish-17-1-age-of-shadows/
- 2004 archive (SE boundary): https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2004-2/
- 2005 archive (SE and ML boundaries): https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2005-2/
- Publish 60 / Stygian Abyss: https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2009-2/publish-60-8th-september-stygian-abyss/
- Publish 68 / High Seas: https://uo.com/wiki/ultima-online-wiki/technical/previous-publishes/2010-2/publish-68-12th-october/
- Publish 90 / Time of Legends: https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-90/
- Time of Legends worldwide notice: https://uo.com/2015/10/07/time-of-legends-available-world-wide/
- Publish 99 / Endless Journey: https://uo.com/wiki/ultima-online-wiki/publish-notes/publish-99/
- Current Endless Journey FAQ: https://uo.com/endless-journey/

Implementation evidence:

- Current ModernUO `Core` flags: https://github.com/modernuo/ModernUO/blob/main/Projects/Server/Main.cs

Reinspect the consuming repository's pinned revision before returning a concrete
gate. `Core.EJ` existing in ModernUO proves only an implementation flag; it does
not turn Endless Journey into a true expansion or a per-account entitlement.
