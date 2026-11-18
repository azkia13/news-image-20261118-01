# news-image-20261118-01

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/azkia13/news-image-20261118-01/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/azkia13/news-image-20261118-01/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world's news of **Wednesday 18 November 2026** — round 2, a new picture from scratch. A dark "night globe" page: a world globe with seven numbered pins, a lead panel on the Shenzhen summit (APEC opens, Xi hosts Putin, Trump flies in from Manila, and the first-ever US–China–Russia summit lands on Thursday), six numbered story tiles (the Gulf tanker war, the fallen Kerch bridge span, the doubling Ebola outbreak in DR Congo, the Democrats' 56 Senate seats, cold killing in Gaza's tents, and Category 5 Cyclone Xavier), plus an "also today" wire strip with the Siberian plane crash, COP31's 144 disputed items, the North Korean missile, France's cost-of-living march, Eisenkot, and the Papua New Guinea quake.

The image is a 1024×1024 PNG drawn deterministically by `draw_world.py` (Python + Pillow, no network, no randomness) from stories reported on 18 November 2026, cross-checked across several outlets. `main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory, exactly like the kit starter.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# or regenerate the image first:
python3 draw_world.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
