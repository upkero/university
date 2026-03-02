from __future__ import annotations

from src.common_types import BIT_WIDTH, MAG_WIDTH, BitArray


def _validate_bits(bits: BitArray, width: int = BIT_WIDTH) -> None:
    if len(bits) != width:
        raise ValueError(f"Expected {width} bits, got {len(bits)}")
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("Bit arrays may contain only 0 or 1")


def bits_to_string(bits: BitArray) -> str:
    _validate_bits(bits)
    return "".join(str(bit) for bit in bits)


def _int_to_unsigned_bits(value: int, width: int) -> BitArray:
    if value < 0:
        raise ValueError("Only non-negative values are supported")
    limit = 1
    for _ in range(width):
        limit *= 2
    if value >= limit:
        raise OverflowError(f"{value} does not fit in {width} bits")

    bits = [0] * width
    index = width - 1
    current = value
    while current > 0 and index >= 0:
        bits[index] = current % 2
        current //= 2
        index -= 1
    return bits


def _unsigned_bits_to_int(bits: BitArray) -> int:
    value = 0
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("Bit arrays may contain only 0 or 1")
        value = value * 2 + bit
    return value


def _max_magnitude() -> int:
    value = 1
    for _ in range(MAG_WIDTH):
        value *= 2
    return value - 1


def _twos_modulus() -> int:
    value = 1
    for _ in range(BIT_WIDTH):
        value *= 2
    return value


def invert_bits(bits: BitArray) -> BitArray:
    _validate_bits(bits)
    return [1 - bit for bit in bits]


def _add_unsigned_bits(a: BitArray, b: BitArray) -> tuple[BitArray, int]:
    _validate_bits(a)
    _validate_bits(b)
    result = [0] * BIT_WIDTH
    carry = 0
    for index in range(BIT_WIDTH - 1, -1, -1):
        total = a[index] + b[index] + carry
        if total >= 2:
            result[index] = total - 2
            carry = 1
        else:
            result[index] = total
            carry = 0
    return result, carry


def _negate_twos(bits: BitArray) -> BitArray:
    _validate_bits(bits)
    one = [0] * BIT_WIDTH
    one[-1] = 1
    inverted = invert_bits(bits)
    result, _ = _add_unsigned_bits(inverted, one)
    return result


def _unsigned_multiply(a: int, b: int) -> int:
    if a < 0 or b < 0:
        raise ValueError("Unsigned multiplication expects non-negative values")
    result = 0
    multiplicand = a
    multiplier = b
    while multiplier > 0:
        if multiplier % 2 == 1:
            result += multiplicand
        multiplicand += multiplicand
        multiplier //= 2
    return result


def _int_to_bits_dynamic(value: int) -> BitArray:
    if value < 0:
        raise ValueError("Only non-negative values are supported")
    if value == 0:
        return [0]

    reversed_bits: BitArray = []
    current = value
    while current > 0:
        reversed_bits.append(current % 2)
        current //= 2

    bits: BitArray = []
    for index in range(len(reversed_bits) - 1, -1, -1):
        bits.append(reversed_bits[index])
    return bits


def _unsigned_divide(dividend: int, divisor: int) -> tuple[int, int]:
    if dividend < 0 or divisor <= 0:
        raise ValueError("Unsigned division expects dividend >= 0 and divisor > 0")

    remainder = 0
    quotient_bits: BitArray = []
    for bit in _int_to_bits_dynamic(dividend):
        remainder = remainder * 2 + bit
        if remainder >= divisor:
            remainder -= divisor
            quotient_bits.append(1)
        else:
            quotient_bits.append(0)
    quotient = _unsigned_bits_to_int(quotient_bits)
    return quotient, remainder
