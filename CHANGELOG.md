# Changelog

All notable changes to richbrutality are documented here.

---

## [Unreleased]

---

## [1.0]

### Added
- `rb.py` — main loop: generates random 256-bit private keys, derives Bitcoin addresses
  via secp256k1 + SHA256 + RIPEMD160 + Base58Check, checks against local lookup file;
  prints every 100 attempts and writes matches to a file named after the address
- `btcwif.py` — WIF encoding/decoding with checksum validation (`privToWif`, `wifToPriv`,
  `wifChecksum`)
- `wallet.py` — wallet utility helpers
- `brute.py` — CSV loader for early address lookup experiments using pandas
- Address lookup via `Bitcoin_addresses_LATEST.txt` from addresses.loyce.club (gitignored,
  ~2.3 GB)
- NumPy vectorized address comparison — significantly faster than Python list iteration
  for tens of millions of addresses
- Commented-out `multiprocessing.Pool` block documenting the parallel scaling path
