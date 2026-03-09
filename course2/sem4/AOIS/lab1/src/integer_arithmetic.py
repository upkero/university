from __future__ import annotations

from src.bit_core import (
    _add_unsigned_bits,
    _compare_unsigned_bits,
    _divide_unsigned_bits,
    _fit_unsigned_to_width,
    _multiply_unsigned_bits,
    _negate_twos,
    _subtract_unsigned_bits,
    _trim_leading_zeros,
    _unsigned_bits_to_int,
)
from src.common_types import DivisionResult, IntegerOpResult, MAG_WIDTH
from src.integer_codes import (
    decimal_to_sign_magnitude,
    sign_magnitude_fixed_point_to_decimal,
    decimal_to_twos_complement,
    twos_complement_to_decimal,
)


def add_in_twos_complement(a: int, b: int) -> IntegerOpResult:
    a_bits = decimal_to_twos_complement(a)
    b_bits = decimal_to_twos_complement(b)
    sum_bits, _ = _add_unsigned_bits(a_bits, b_bits)
    decimal = twos_complement_to_decimal(sum_bits)
    overflow = (a_bits[0] == b_bits[0]) and (sum_bits[0] != a_bits[0])
    return IntegerOpResult(bits=sum_bits, decimal=decimal, overflow=overflow, exact_decimal=a + b)


def subtract_in_twos_complement(minuend: int, subtrahend: int) -> IntegerOpResult:
    a_bits = decimal_to_twos_complement(minuend)
    b_bits = decimal_to_twos_complement(subtrahend)
    negative_b = _negate_twos(b_bits)
    diff_bits, _ = _add_unsigned_bits(a_bits, negative_b)
    decimal = twos_complement_to_decimal(diff_bits)
    overflow = (a_bits[0] != b_bits[0]) and (diff_bits[0] != a_bits[0])
    return IntegerOpResult(
        bits=diff_bits,
        decimal=decimal,
        overflow=overflow,
        exact_decimal=minuend - subtrahend,
    )


def multiply_in_sign_magnitude(a: int, b: int) -> IntegerOpResult:
    a_bits = decimal_to_sign_magnitude(a)
    b_bits = decimal_to_sign_magnitude(b)

    sign = a_bits[0] ^ b_bits[0]
    a_mag_bits = _trim_leading_zeros(a_bits[1:])
    b_mag_bits = _trim_leading_zeros(b_bits[1:])
    raw_product_bits = _multiply_unsigned_bits(a_mag_bits, b_mag_bits)
    overflow = len(raw_product_bits) > MAG_WIDTH
    stored_mag_bits = _fit_unsigned_to_width(raw_product_bits, MAG_WIDTH)

    bits = [sign] + stored_mag_bits
    stored_mag = _unsigned_bits_to_int(stored_mag_bits)
    raw_product = _unsigned_bits_to_int(raw_product_bits)
    decimal = -stored_mag if sign else stored_mag
    exact = -(raw_product) if sign else raw_product
    return IntegerOpResult(bits=bits, decimal=decimal, overflow=overflow, exact_decimal=exact)


def divide_in_sign_magnitude(dividend: int, divisor: int, precision: int = 5) -> DivisionResult:
    if precision < 0:
        raise ValueError("precision must be non-negative")
    if divisor == 0:
        raise ZeroDivisionError("Division by zero")

    dividend_bits = decimal_to_sign_magnitude(dividend)
    divisor_bits = decimal_to_sign_magnitude(divisor)
    sign = dividend_bits[0] ^ divisor_bits[0]

    dividend_mag_bits = _trim_leading_zeros(dividend_bits[1:])
    divisor_mag_bits = _trim_leading_zeros(divisor_bits[1:])

    integer_bits, remainder_bits = _divide_unsigned_bits(dividend_mag_bits, divisor_mag_bits)
    integer_part_bits = [] if integer_bits == [0] else integer_bits
    used_precision = min(precision, MAG_WIDTH - len(integer_part_bits))

    fraction_bits: list[int] = []
    remainder_work = remainder_bits
    two_bits = [1, 0]
    for _ in range(used_precision):
        if remainder_work == [0]:
            fraction_bits.append(0)
            continue

        doubled_remainder = _multiply_unsigned_bits(remainder_work, two_bits)
        if _compare_unsigned_bits(doubled_remainder, divisor_mag_bits) >= 0:
            fraction_bits.append(1)
            remainder_work = _subtract_unsigned_bits(doubled_remainder, divisor_mag_bits)
        else:
            fraction_bits.append(0)
            remainder_work = doubled_remainder

    magnitude_bits = integer_part_bits + fraction_bits
    if not magnitude_bits:
        magnitude_bits = [0]

    overflow = len(integer_part_bits) > MAG_WIDTH
    if overflow:
        stored_mag_bits = _fit_unsigned_to_width(integer_part_bits, MAG_WIDTH)
        used_precision = 0
    else:
        stored_mag_bits = [0] * (MAG_WIDTH - len(magnitude_bits)) + magnitude_bits

    bits = [sign] + stored_mag_bits
    decimal = sign_magnitude_fixed_point_to_decimal(bits, used_precision)
    exact = decimal
    remainder = _unsigned_bits_to_int(remainder_work)
    return DivisionResult(
        bits=bits,
        decimal=decimal,
        overflow=overflow,
        exact_decimal=exact,
        remainder=remainder,
        precision=used_precision,
    )
