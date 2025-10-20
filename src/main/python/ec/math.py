import contextlib
from functools import reduce


def chinese_remainder(
    moduli: tuple[int, ...], remainders: tuple[int, ...]
) -> int:
    def mul_inv(a: int, b: int) -> int:
        b0 = b
        x0, x1 = 0, 1
        if b == 1:
            return 1
        while a > 1:
            q = a // b
            a, b = b, a % b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += b0
        return x1

    the_sum = 0
    product = reduce(lambda a, b: a * b, moduli)
    for modulus, remainder in zip(moduli, remainders, strict=True):
        p = product // modulus
        the_sum += remainder * mul_inv(p, modulus) * p
    return the_sum % product


if __name__ == "__main__":
    assert chinese_remainder((3, 5, 7), (2, 3, 2)) == 23
    assert chinese_remainder((11, 12, 13), (10, 4, 12)) == 1000
    with contextlib.suppress(ZeroDivisionError):
        chinese_remainder((2, 3, 2), (3, 5, 7))
