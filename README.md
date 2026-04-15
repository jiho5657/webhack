# Hollowed

세 개의 소수로 이루어진 RSA 모듈러스와, 그 중 하나의 상위 비트 일부가 새어나갔다.
`challenge/output.txt` 를 보고 플래그를 복구하라.

공개 값:

- `N` : 2048비트 RSA 모듈러스
- `e = 65537`
- `c = flag^e mod N`
- `p_high` : 어떤 소수 인수 `p` 의 상위 `leak_bits` 비트
- `prime_bits`, `unknown_bits`, `leak_bits` : 비트 수 파라미터

플래그 포맷: `MJSEC{...}`

## Hints

1. `N` 의 소인수는 두 개가 아니다.
2. Coppersmith 의 `beta` 는 고정된 값이 아니라 `log p / log N` 이다.
3. SageMath `small_roots` 의 기본 `epsilon` 은 이 문제에서 여유가 부족하다.
