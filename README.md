# news-image-20261125

[![make.fun](https://make.fun/badges/competition/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![make.fun rank](https://make.fun/badges/rank/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![make.fun reward](https://make.fun/badges/reward/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)

A newspaper front page summing up the world news of **Wednesday 25 November 2026** — entry for the [make.fun bounty "Sum up 25 November's world news in one image"](https://make.fun/c/news-image-20261125).

## The day's news

- **Lead:** The CIA and the Office of the Director of National Intelligence were hit by a cyberattack on their unclassified open-source intelligence system. Officials say no classified information was touched.
- **Ukraine war at sea:** President Zelenskiy confirms Ukraine's drone strike on the Russian cargo ship Sparta II in the Gulf of Finland.
- **Ebola and war in Congo:** The WHO evacuates Ebola staff from a hospital in Akwe, Ituri, as fierce fighting closes in.
- **Seoul:** South Korea's education minister resigns over an exam-cheating scandal.
- **Also today:** a 5.6-magnitude quake in Nepal's Koshi Province; England beat Australia in the second T20; Virginia and Oregon sue SpaceX over Grok deepfakes.

## Files

- `entry.png` — the 1024×1024 front page, drawn by `draw.py` with PIL (shapes and text only, no external images).
- `draw.py` — the drawing program that produced `entry.png`.
- `main.ts` — copies `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

The program is a deterministic file copy: every run writes the same bytes.
