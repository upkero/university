from __future__ import annotations

from src.common_types import BIT_WIDTH, MAG_WIDTH, BitArray


def _validate_bits(bits: BitArray, width: int = BIT_WIDTH) -> None:
    if len(bits) != width:
        raise ValueError(f"Expected {width} bits, got {len(bits)}")
    _validate_bit_values(bits)


def _validate_bit_values(bits: BitArray) -> None:
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
    _validate_bit_values(bits)
    value = 0
    for bit in bits:
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


def _add_unsigned_bits(a: BitArray, b: BitArray, carry_in: int = 0) -> tuple[BitArray, int]:
    if len(a) != len(b):
        raise ValueError("Unsigned addition expects equal bit widths")
    if carry_in not in (0, 1):
        raise ValueError("carry_in must be 0 or 1")
    width = len(a)
    _validate_bits(a, width=width)
    _validate_bits(b, width=width)
    result = [0] * width
    carry = carry_in
    for index in range(width - 1, -1, -1):
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


def _trim_leading_zeros(bits: BitArray) -> BitArray:
    if not bits:
        return [0]
    _validate_bit_values(bits)
    first_non_zero = 0
    while first_non_zero < len(bits) - 1 and bits[first_non_zero] == 0:
        first_non_zero += 1
    return bits[first_non_zero:]


def _compare_unsigned_bits(a: BitArray, b: BitArray) -> int:
    a_trimmed = _trim_leading_zeros(a)
    b_trimmed = _trim_leading_zeros(b)
    if len(a_trimmed) < len(b_trimmed):
        return -1
    if len(a_trimmed) > len(b_trimmed):
        return 1
    for index in range(len(a_trimmed)):
        if a_trimmed[index] < b_trimmed[index]:
            return -1
        if a_trimmed[index] > b_trimmed[index]:
            return 1
    return 0


def _subtract_unsigned_bits(a: BitArray, b: BitArray) -> BitArray:
    if _compare_unsigned_bits(a, b) < 0:
        raise ValueError("Unsigned subtraction expects minuend >= subtrahend")

    a_le = list(reversed(_trim_leading_zeros(a)))
    b_le = list(reversed(_trim_leading_zeros(b)))
    result_le: BitArray = []
    borrow = 0
    for index in range(len(a_le)):
        b_bit = b_le[index] if index < len(b_le) else 0
        diff = a_le[index] - b_bit - borrow
        if diff < 0:
            diff += 2
            borrow = 1
        else:
            borrow = 0
        result_le.append(diff)

    if borrow == 1:
        raise ValueError("Unsigned subtraction underflow")
    return _trim_leading_zeros(list(reversed(result_le)))


def _multiply_unsigned_bits(a: BitArray, b: BitArray) -> BitArray:
    a_trimmed = _trim_leading_zeros(a)
    b_trimmed = _trim_leading_zeros(b)
    if a_trimmed == [0] or b_trimmed == [0]:
        return [0]

    a_le = list(reversed(a_trimmed))
    b_le = list(reversed(b_trimmed))
    result_le: BitArray = [0] * (len(a_le) + len(b_le))

    for b_index, b_bit in enumerate(b_le):
        if b_bit == 0:
            continue
        carry = 0
        for a_index, a_bit in enumerate(a_le):
            result_index = b_index + a_index
            total = result_le[result_index] + a_bit + carry
            result_le[result_index] = total % 2
            carry = total // 2

        result_index = b_index + len(a_le)
        while carry > 0:
            if result_index >= len(result_le):
                result_le.append(0)
            total = result_le[result_index] + carry
            result_le[result_index] = total % 2
            carry = total // 2
            result_index += 1

    return _trim_leading_zeros(list(reversed(result_le)))


def _divide_unsigned_bits(dividend: BitArray, divisor: BitArray) -> tuple[BitArray, BitArray]:
    divisor_trimmed = _trim_leading_zeros(divisor)
    if divisor_trimmed == [0]:
        raise ValueError("Unsigned division expects divisor > 0")

    dividend_trimmed = _trim_leading_zeros(dividend)
    quotient: BitArray = []
    remainder: BitArray = [0]

    for bit in dividend_trimmed:
        if remainder == [0]:
            remainder = [bit]
        else:
            remainder.append(bit)
        remainder = _trim_leading_zeros(remainder)

        if _compare_unsigned_bits(remainder, divisor_trimmed) >= 0:
            remainder = _subtract_unsigned_bits(remainder, divisor_trimmed)
            quotient.append(1)
        else:
            quotient.append(0)

    if not quotient:
        quotient = [0]
    return _trim_leading_zeros(quotient), _trim_leading_zeros(remainder)


def _fit_unsigned_to_width(value_bits: BitArray, width: int) -> BitArray:
    if width <= 0:
        raise ValueError("width must be positive")
    trimmed = _trim_leading_zeros(value_bits)
    if len(trimmed) >= width:
        return trimmed[-width:]
    return [0] * (width - len(trimmed)) + trimmed
