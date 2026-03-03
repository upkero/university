from __future__ import annotations

from src.bit_core import (
    _add_unsigned_bits,
    _divide_unsigned_bits,
    _fit_unsigned_to_width,
    _multiply_unsigned_bits,
    _negate_twos,
    _trim_leading_zeros,
    _unsigned_bits_to_int,
)
from src.common_types import DivisionResult, IntegerOpResult, MAG_WIDTH
from src.integer_codes import (
    decimal_to_sign_magnitude,
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

    ten_bits = [1, 0, 1, 0]
    scale_bits = [1]
    for _ in range(precision):
        scale_bits = _multiply_unsigned_bits(scale_bits, ten_bits)

    scaled_dividend_bits = _multiply_unsigned_bits(dividend_mag_bits, scale_bits)
    quotient_bits, remainder_bits = _divide_unsigned_bits(scaled_dividend_bits, divisor_mag_bits)

    overflow = len(quotient_bits) > MAG_WIDTH
    stored_mag_bits = _fit_unsigned_to_width(quotient_bits, MAG_WIDTH)
    bits = [sign] + stored_mag_bits

    scale = _unsigned_bits_to_int(scale_bits)
    stored_mag = _unsigned_bits_to_int(stored_mag_bits)
    scaled_quotient = _unsigned_bits_to_int(quotient_bits)
    remainder = _unsigned_bits_to_int(remainder_bits)
    decimal = stored_mag / scale
    exact = scaled_quotient / scale
    if sign:
        decimal = -decimal
        exact = -exact
    return DivisionResult(
        bits=bits,
        decimal=decimal,
        overflow=overflow,
        exact_decimal=exact,
        remainder=remainder,
        precision=precision,
    )
