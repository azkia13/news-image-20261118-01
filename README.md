# news-image-20261118-01

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/azkia13/news-image-20261118-01/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/azkia13/news-image-20261118-01/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world's news of **Wednesday 18 November 2026** — round 3, a new picture from scratch. A dark "night globe" page: a world globe drawn from real longitude/latitude coastlines with eight numbered pins (leader lines where four pins crowd the east Mediterranean and the Gulf), a lead panel on the Shenzhen summit (APEC opens, Xi hosts Putin at midday, Trump lands from Manila and is greeted by Xi on the tarmac, and the first-ever US–China–Russia summit lands on Thursday, with nuclear arms, Iran and Ukraine on the table), eight numbered story tiles (the US strike on Qeshm and Iran's drone attacks on Bahrain and Kuwait, the fallen Kerch bridge arch after 1,441 drones, the doubling Ebola outbreak in DR Congo, the Democrats' 56 Senate seats, cold and floods in Gaza's tents, Category 5 Cyclone Xavier, COP31's 144 disputed items, and Voyager 1 crossing one light-day), plus an "also today" wire strip with the Siberian plane crash, the North Korean missile, the French pay strike, Eisenkot, the Papua New Guinea quake, and the Myanmar case ruling due on Thursday.

Round 3 fixes three facts round 2 got wrong: the Gulf headline no longer claims "five tankers sunk" (no outlet confirmed any sinking; the verified story is the Qeshm strike and the drone attacks), the France march is now the 18 November figure (140,000+ in a public-sector pay strike, not the 146,000 of 7 November), and the Myanmar item now says the World Court rules on Thursday, since the ICJ delivers its judgment on 19 November.

The image is a 1024×1024 PNG drawn deterministically by `draw_world.py` (Python + Pillow, no network, no randomness) from stories reported on 18 November 2026, cross-checked across AP, Reuters, AFP, BBC, CNN, Euronews and One Turn's daily brief. `main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory, exactly like the kit starter.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# or regenerate the image first:
python3 draw_world.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
