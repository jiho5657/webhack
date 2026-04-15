# Hollowed

> *A very hard crypto challenge.*

A three-prime RSA modulus, a flag encrypted under textbook RSA, and a
single leaked chunk of one of the primes. Surely a handful of bits
can't hurt, right?

## Category

Crypto / Lattices (hard)

## Files given to the player

```
challenge/output.txt     public parameters
```

The player receives:

- `N`, the RSA modulus (2048 bits)
- `e = 65537`
- `c = flag^e mod N`
- `p_high`, the 470 most-significant bits of one prime factor `p`
- the bit-sizes that describe what `p_high` is

That is it. No oracle, no source-code instrumentation, no side
channel. Everything needed sits in `output.txt`.

## Intended solution

See `solution/solve.sage` and `solution/writeup.md`. In one line:

```
Coppersmith's theorem with beta = 1/3 (not 1/2) recovers p.
```

## Reproducing the challenge

```sh
pip install pycryptodome
python3 challenge/gen.py
```

Running the generator overwrites `challenge/output.txt`. The flag is
hard-coded in `gen.py`; swap in your event's flag before deploying.

## Running the solver

The reference solution uses SageMath's `small_roots`:

```sh
cd solution && sage solve.sage
```

Expect the LLL step to take a few seconds on the default parameters.

## Flag

`MJSEC{c0pp3rsm1th_w1th_b3t4_0n3_th1rd_1s_th3_k3y_ad3f12}`
