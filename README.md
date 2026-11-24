# world-in-a-day-nov24

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/jpmax2027/world-in-a-day-nov24/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/jpmax2027/world-in-a-day-nov24/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page for Tuesday 24 November 2026, generated with
Google Gemini (AI Plus) from the day's reported headlines and packaged
as a make.fun entry by a small Python program. The masthead reads
"THE WORLD IN A DAY" over the date line "TUESDAY 24 NOVEMBER 2026";
the lead story is Jensen Huang's reinstatement at Nvidia as the stock
soared 31% in a record tech rebound, with panels on Ukraine sinking a
Russian warship off Libya, Mexico defying a US extradition request so
cartel boss "El Chapo Isidro" is tried at home, and oil sliding to $80
on US-Iran talks, plus a ticker with the Colombia car bomb, the
SpaceX-Tesla merger talks and the UN chief's call for AI rules.

The program (main.py, Python 3 standard library only, no network)
ships the page as front-page.jpg, checks it is a whole JPEG inside the
competition limits (at most 1 MiB, at most 1024x1024 pixels, read from
the JPEG header), and writes the bytes unchanged to
$MAKEFUN_OUTPUT_DIR/entry.png. Two runs produce byte-identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=zbqpv30a&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
