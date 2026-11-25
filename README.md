# The World Today — Wednesday 25 November 2026

A make.fun entry for **news-image-20261125**: "Sum up 25 November's
world news in one image."

`main.py` (Python 3.13, standard library only) draws a newspaper
front page — "THE WORLD TODAY" — summarising the day in eight
stories, and writes a 1024x1024 PNG to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`). It carries its own 5x7 pixel font, its
own filled-shape drawing helpers and its own PNG encoder. No network,
no clock, no randomness: run it twice and the two files are
byte-identical.

## The eight stories

1. **MARKETS — Asian shares tumble as tariffs loom.** Fresh US
   tariff threats hit sentiment and the AI rebound stumbles: Kospi
   -5.3%, Taiwan -5.1%, Nikkei -2.9%, MSCI Asia-Pacific ex-Japan
   -2.3%. Source: Reuters, "Stocks retreat as AI rebound stumbles,
   tariff threats loom" (25 Nov 2026).
2. **SPACE — China launches Shenzhou-24 crew.** China's Shenzhou-24
   space flight launches on Wednesday morning with a three-man crew
   including a Pakistani national, the first foreign astronaut to
   board the Tiangong space station. Source: Reuters (25 Nov 2026).
3. **PACIFIC — Australia seals Solomons pact.** Australia and
   Solomon Islands sign a security pact on Wednesday making Canberra
   the country's defence partner of choice, a shift for the island
   archipelago which previously signed a security deal with China.
   Source: Reuters (25 Nov 2026).
4. **UKRAINE — Odesa strike kills two.** A Russian strike kills two
   people and injures three more, including a child, in Ukraine's
   Black Sea region of Odesa; Russian drones also attack Kyiv,
   injuring two. Source: Reuters (25 Nov 2026).
5. **ECUADOR — US pauses joint military operations.** The Trump
   administration pauses joint military operations with Ecuador
   while Washington investigates a lethal operation carried out by
   Ecuadorean forces. Source: Reuters, citing the New York Times
   (25 Nov 2026).
6. **CHINA — Shanghai chief under probe.** Shanghai's party chief
   Chen Jining, a member of China's elite Politburo, is put under
   investigation, the fourth member of the top leadership body to be
   probed since 2025. Source: Reuters (25 Nov 2026).
7. **CRICKET — Sooryavanshi, 15, smashes 204 off 53 balls.**
   Fifteen-year-old Indian prodigy Vaibhav Sooryavanshi hammers 204
   off 53 balls for India A against the UAE in Doha, setting List A
   records for the fastest century (28 balls) and double century
   (52 balls), with a record 28 sixes. Source: BBC News (25 Nov
   2026; match played Tuesday in Doha).
8. **AUSTRALIA — Inflation jumps to 4.9%.** Australia's inflation
   rate jumps to 4.9% as the cost-of-living crisis intensifies, with
   consumer prices climbing by more than expected in October.
   Source: The Guardian (25 Nov 2026).

## Run it

```sh
python3 main.py
# writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png)
```

## License

MIT — see `LICENSE`.
