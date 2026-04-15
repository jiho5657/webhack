# Hollowed -- writeup

## Recon

`output.txt` contains

```
prime_bits   = 683
unknown_bits = 213
leak_bits    = 470
e            = 65537
N = <2048-bit integer>
p_high = <470-bit integer>
c = <2048-bit integer>
```

The comment on top says `N = p * q * r`, three balanced primes. So
`p_high` is the top 470 bits of one of them, and we have to recover
the remaining 213 bits.

## Why the usual Coppersmith recipe fails

The standard "partial prime exposure" lemma says: given `N = p * q`
with `p >= N^{1/2}`, knowing half of `p` lets Coppersmith's theorem
recover the rest. Plugging `beta = 1/2` into `small_roots` is the
reflex.

Here that reflex is wrong. Our modulus is a product of **three**
primes of equal size, so

```
log_2 p   ~  log_2 N / 3
beta      =  log p / log N  ~  1 / 3
```

The Coppersmith bound for a monic degree-1 polynomial with a root
modulo a divisor of size `N^beta` is

```
|x_0|  <  N^{beta^2 - epsilon}
```

Plugging `beta = 1/2` gives `N^{1/4 - epsilon} ~ 2^{511}` of slack,
which is enormous -- and wrong. The real bound is

```
N^{beta^2} = N^{1/9} ~ 2^{227.56}
```

and we have 213 unknown bits, leaving only ~14.5 bits of slack.
Sage's default `epsilon = beta / 7 ~ 0.0476` eats
`0.0476 * 2048 ~ 97` bits of slack, which we do not have. The
attack silently returns `[]` and the novice declares the problem
unsolvable.

## Setting up the polynomial

We write the unknown 213 low bits of `p` as `x`:

```
p = p_high * 2^213 + x,       0 <= x < 2^213
```

Define

```
f(x) = p_high * 2^213 + x    in  Z[x]
```

By construction `f(x_0) = p`, so `f(x_0) ≡ 0 (mod p)` and `p | N`.
Coppersmith's theorem therefore promises to recover `x_0` provided
`|x_0| < N^{beta^2 - epsilon}`.

## Parameter tuning

The slack budget is

```
epsilon  <  (log_2 N^{1/9} - log_2 X) / log_2 N
         =  (227.56 - 213) / 2048
         ~  0.0071
```

Anything up to ~0.006 is safe. Setting `epsilon = 0.005` forces the
lattice dimension

```
m ~ ceil(beta / epsilon) = ceil((1/3) / 0.005) ~ 67
```

which LLL can still reduce in seconds.

## Exploit (SageMath)

```python
P.<x> = PolynomialRing(Zmod(N))
f = (p_high << 213) + x
f = f.monic()

roots = f.small_roots(X=2^213, beta=1/3, epsilon=0.005)
assert roots, "tighten epsilon further"

p = (p_high << 213) + int(roots[0])
assert N % p == 0
```

`p` drops out in a few seconds. At this point we don't even need to
factor `q * r`: the flag is 55 bytes (~440 bits), much smaller than
the 683-bit prime `p`, so reduction modulo `p` is lossless:

```python
d_p  = inverse_mod(e, p - 1)
m    = power_mod(c, d_p, p)
flag = long_to_bytes(int(m))
```

## Flag

```
flag{c0pp3rsm1th_w1th_b3t4_0n3_th1rd_1s_th3_k3y_ad3f12}
```

## Take-aways

- `beta` in `small_roots` is `log p / log N`, not a fixed `1/2`.
  Multi-prime RSA drops it.
- The default `epsilon` is generous; when you're sitting close to
  the theoretical bound, drop it explicitly and pay in lattice
  dimension.
- Once you have any single prime factor `p` with the property
  `message < p`, you never needed the others -- CRT decryption
  degenerates to a single exponentiation mod `p`.
