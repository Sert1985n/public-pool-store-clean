# Miningcore template notes

This folder contains helper templates based on the working server state from 2026-03-22.

Files:
- `config.current-working.example.json` — example Miningcore config aligned to the working pool state.
- `coins.bch2.snippet.json` — BCH2 coin snippet that can be merged into `coins.json`.

Known status at export time:
- Enabled / working or syncing: btc, bch, bc2, btcs, dgb, doge, grs, lcc, lcc2, ltc, ppc, rvn, wjk, xna
- Disabled intentionally: bch2, xmr, pepew, bsv, xec, vtc
- `bch2` needs a Miningcore engine patch for address parsing.
- `pepew` image is incompatible with non-AVX2 CPUs (exit 132).
- `xmr` wallet should be configured after the node is fully synced.
