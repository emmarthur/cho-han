# Book directions — Cho-Han

**Catalog #446** · Al Sweigart, *The Big Book of Small Python Projects*, **Project #15** — Cho-Han

- Invent with Python: [project15.html](https://inventwithpython.com/bigbookpython/project15.html)
- Upstream: [chohan.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/chohan.py)
- Local reference: [`reference/chohan.py`](./reference/chohan.py)
- Shared logic: [`cho_han_core.py`](./cho_han_core.py)

## What the book asks you to build

Traditional Japanese even/odd dice game:

1. Start with **5000 mon** purse.
2. Bet an amount each round.
3. Dealer rolls two dice (hidden until guess).
4. Player calls **CHO** (even total) or **HAN** (odd).
5. Win: gain pot minus **10% house fee**; lose: forfeit pot.
6. Game ends at **0 mon**.

## Web version (`web/` — FastAPI, port **3034**)

| Book step | Web equivalent |
|-----------|----------------|
| Bet loop | `POST /api/bet` |
| CHO/HAN | `POST /api/guess` |
| Japanese labels | `ICHI`…`ROKU` on reveal |
| Broke | `phase: broke` + reset endpoint |
