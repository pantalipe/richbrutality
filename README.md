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

## What I learned

### Elliptic curve cryptography on secp256k1

Bitcoin private keys are 256-bit integers chosen at random from the finite field defined by the secp256k1 curve. The curve equation is y² = x³ + 7 over a prime field, and the security guarantee is that given a public key Q = k × G (where G is the generator point and k is the private key), recovering k from Q is computationally infeasible. This is the elliptic curve discrete logarithm problem. The code uses the `ecdsa` library's `SigningKey.generate(curve=ecdsa.SECP256k1)` to produce a valid private key, and `.get_verifying_key()` to derive the corresponding public key point on the curve.

### Uncompressed public key format

The public key is a point (x, y) on secp256k1, each coordinate being 32 bytes. The uncompressed encoding prepends `04` to signal that both coordinates follow, producing a 65-byte (130 hex character) public key. This is visible in the code as `'04' + ecdsaPrivateKey.get_verifying_key().to_string().hex()`. Compressed keys (33 bytes, prefixed `02` or `03` depending on the parity of y) are the modern standard but this project deliberately uses uncompressed keys to keep the derivation explicit.

### Address derivation pipeline

Bitcoin addresses are not public keys — they are the result of a multi-step hashing and encoding pipeline designed to be short, error-resistant, and to provide an extra layer of separation from the raw key material:

1. **SHA-256** of the public key bytes
2. **RIPEMD-160** of the SHA-256 hash — this produces the 20-byte *public key hash*
3. Prepend `0x00` as the mainnet version byte
4. Double-SHA-256 of the versioned payload to produce the checksum; take the first 4 bytes
5. Append the checksum to the versioned payload
6. **Base58Check** encode the result

Implementing this manually — rather than calling a wallet library — makes it clear why Bitcoin addresses are 25-34 characters long and why they start with `1`. The `1` is a direct consequence of Base58Check encoding a payload that begins with `0x00`.

### Base58Check and why it exists

Base58 removes visually ambiguous characters (`0`, `O`, `I`, `l`) from standard Base64 to reduce transcription errors. The `Check` suffix means a 4-byte checksum is embedded, so any single-character typo in a Bitcoin address will almost certainly be detected. Implementing `b58encode` manually (as in `btcwif.py`) made it clear that Base58 is just positional notation in base 58, the same way hexadecimal is positional notation in base 16.

### Wallet Import Format (WIF)

Private keys are stored and shared using WIF, which applies a similar pipeline: prepend `0x80` (mainnet prefix), double-SHA-256 for a 4-byte checksum, append checksum, Base58 encode. Implementing `privToWif` and `wifToPriv` (with `wifChecksum`) in `btcwif.py` made the round-trip explicit and testable: a WIF string encodes exactly one private key and the embedded checksum makes invalid strings detectable before any network call.

### The scale of the key space

Running this loop in practice makes the abstract math concrete. The private key space has 2²⁵⁶ ≈ 10⁷⁷ possibilities. Even at a billion attempts per second, exhaustively searching it would take longer than the age of the universe by many orders of magnitude. The probability of randomly generating an address that exists in the `Bitcoin_addresses_LATEST.txt` lookup file is lower than selecting one specific atom from all matter in the observable universe. The experiment is not about finding a funded wallet — it is about feeling that scale in a running process rather than just reading a number.

## References

- [Bitcoin Wiki — Technical background of version 1 Bitcoin addresses](https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses)
- [Mastering Bitcoin — Andreas Antonopoulos](https://github.com/bitcoinbook/bitcoinbook)
