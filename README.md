# THE WORLD — Wednesday 18 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261118-blue)](https://make.fun/bounty/news-image-20261118)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Entry](https://img.shields.io/badge/entry-2026--11--18-green)](https://github.com/Fslrm123/news-image-20261118-entry)

A one-page newspaper front page that sums up Wednesday 18 November 2026 in a
single image. The masthead names the day prominently, and every story on the
page is a real event reported on that day — across regions and fields, from
the Shenzhen summit to the Gulf, the Kerch Bridge, the Alaska Senate race,
Nvidia's record quarter, and the Ebola outbreak in DR Congo.

> Built with [make.fun](https://make.fun/r/3v2j7j85) — referral code `3v2j7j85`.
> Earn USDC by letting your AI agent code: join via the link above.

## What's on the page

- **Lead:** Trump, Xi and Putin to hold their first three-way summit in
  Shenzhen, on the sidelines of the APEC summit.
- **The Gulf:** Iran fires drones at a US base in Kuwait and sites in
  Bahrain after US jets hit a missile site on Qeshm Island.
- **Ukraine:** the Kerch Bridge is hit for a second day; part of the road
  span collapses.
- **12 illustrated stories**, including the Democrats taking the US Senate
  56–44, Nvidia's revenue doubling to $115.8B, Israel's new Gaza ground
  operation, Ebola passing 11,000 cases, the US losing measles-free status,
  Anthropic's $81.3B record offering, the Fed minutes sinking stocks, and
  COP31 deadlocked in Antalya.
- **Flashpoints:** 12 places that defined the day, from Shenzhen to Siberia.
- **By the Numbers:** 3 leaders, 141 drones, 56–44, 11,000 cases, $115.8B —
  every figure already in the stories above.
- **In Brief:** 24 more verified items from the same day.
- **Pull-quote:** "An unprecedented operation." — Volodymyr Zelenskyy, on
  the Kerch Bridge strike.

## How it is made

`draw_poster.py` draws the front page with Python (PIL) into a deterministic
1024×1024 `entry.png` (under 1 MiB). No network access at runtime; the same
script always writes identical bytes.

`main.ts` copies the committed `entry.png` to `/output/entry.png`.

## Run it

```sh
python3 draw_poster.py        # regenerate entry.png
node main.ts                  # writes /output/entry.png
```

## Sources

Every headline, number and dateline was checked against reporting published
on 18 November 2026 (AP, AFP, Reuters, Anadolu Agency, Al Jazeera, Motley
Fool, and other outlets via same-day news briefs). Nothing on the page is
invented.
