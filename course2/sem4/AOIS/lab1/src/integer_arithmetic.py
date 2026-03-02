from __future__ import annotations

from src.bit_core import (
    _add_unsigned_bits,
    _int_to_unsigned_bits,
    _max_magnitude,
    _negate_twos,
    _unsigned_bits_to_int,
    _unsigned_divide,
    _unsigned_multiply,
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
    a_mag = _unsigned_bits_to_int(a_bits[1:])
    b_mag = _unsigned_bits_to_int(b_bits[1:])
    raw_product = _unsigned_multiply(a_mag, b_mag)

    sign = a_bits[0] ^ b_bits[0]
    max_mag = _max_magnitude()
    overflow = raw_product > max_mag
    modulus = max_mag + 1
    stored_mag = raw_product % modulus

    bits = [sign] + _int_to_unsigned_bits(stored_mag, MAG_WIDTH)
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

    abs_dividend = -dividend if dividend < 0 else dividend
    abs_divisor = -divisor if divisor < 0 else divisor

    scale = 1
    for _ in range(precision):
        scale *= 10
    scaled_dividend = _unsigned_multiply(abs_dividend, scale)
    scaled_quotient, remainder = _unsigned_divide(scaled_dividend, abs_divisor)

    max_mag = _max_magnitude()
    modulus = max_mag + 1
    overflow = scaled_quotient > max_mag
    stored_mag = scaled_quotient % modulus
    bits = [sign] + _int_to_unsigned_bits(stored_mag, MAG_WIDTH)

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
