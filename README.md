# richbrutality

Educational Bitcoin keypair brute force experiment.

## What it does

Generates random private keys in a loop, derives the corresponding Bitcoin address and checks if the address has any balance. A hands-on study of elliptic curve cryptography (secp256k1) and the Bitcoin address derivation process.

## Why it exists

Bitcoin addresses are derived from 256-bit private keys — a space of approximately 10^77 possibilities. This project explores in practice just how vast that space is and how wallet generation works under the hood, without relying on third-party wallets.

It's the kind of experiment you run to understand, not to get rich. The probability of hitting an address with a balance is astronomically small — lower than picking a specific atom in the observable universe.

## How it works

```
Generate random 256-bit number
          ↓
Private key (hex)
          ↓
secp256k1 elliptic curve → Public key
          ↓
SHA256 → RIPEMD160 → Base58Check
          ↓
Bitcoin address
          ↓
Check balance on .txt from http://addresses.loyce.club/
          ↓
Balance > 0? → address.txt
Balance = 0? → next attempt
```

## Stack

- Python
- Elliptic curve cryptography (secp256k1)
- Bitcoin public API

## Disclaimer

This project is strictly educational. There is no realistic expectation of finding a funded wallet — the math guarantees that. The goal is to understand how Bitcoin wallets work internally.

## References

- [Bitcoin Wiki — Technical background of version 1 Bitcoin addresses](https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses)
- [Mastering Bitcoin — Andreas Antonopoulos](https://github.com/bitcoinbook/bitcoinbook)
