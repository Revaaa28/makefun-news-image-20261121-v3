# The World in One Day — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Revaaa28/makefun-news-image-20261121-v3/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Revaaa28/makefun-news-image-20261121-v3/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for the make.fun bounty [news-image-20261121](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121):
one image that sums up the world news of **Saturday 21 November 2026**.

The page is a broadsheet front page drawn entirely in code: a giant
serif masthead, a six-number stat strip, a seven-region count bar,
three illustrated hero stories (COP31 in overtime, five Houthi
missiles downed over Saudi Arabia, the 6.7 quake in Junín, Peru), ten
illustrated briefs, a world map with 35 numbered pins, a 22-story
index, and an itemised DATE CHECK strip that names the stories left
out — Friday's news and older — with their real dates.

Every story happened, or was first reported, on Saturday 21 November
2026, and each carries its source on the page. The full source list is
in [SOURCES.md](SOURCES.md).

## Run it

```sh
python3 draw.py            # renders entry.png (1024x1024, deterministic)
python3 main.py            # validates entry.png, copies it to $MAKEFUN_OUTPUT_DIR (default /output)
```

Requires Python 3 and Pillow (for `draw.py` only; `main.py` is
stdlib-only). Rendering is deterministic: two runs of `draw.py`
produce byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
