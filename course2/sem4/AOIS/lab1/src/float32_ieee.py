from __future__ import annotations

import math

from src.bit_core import _int_to_unsigned_bits, _unsigned_bits_to_int, _validate_bits
from src.common_types import (
    FLOAT_EXP_BIAS,
    FLOAT_EXP_BITS,
    FLOAT_FRAC_BITS,
    FloatOpResult,
    BitArray,
)


def _compose_float32_bits(sign: int, exponent: int, fraction: int) -> BitArray:
    if sign not in (0, 1):
        raise ValueError("sign must be 0 or 1")
    if exponent < 0 or exponent >= 2**FLOAT_EXP_BITS:
        raise ValueError("Exponent out of range")
    if fraction < 0 or fraction >= 2**FLOAT_FRAC_BITS:
        raise ValueError("Fraction out of range")

    exponent_bits = _int_to_unsigned_bits(exponent, FLOAT_EXP_BITS)
    fraction_bits = _int_to_unsigned_bits(fraction, FLOAT_FRAC_BITS)
    return [sign] + exponent_bits + fraction_bits


def _split_float32_bits(bits: BitArray) -> tuple[int, int, int]:
    _validate_bits(bits)
    sign = bits[0]
    exponent = _unsigned_bits_to_int(bits[1 : 1 + FLOAT_EXP_BITS])
    fraction = _unsigned_bits_to_int(bits[1 + FLOAT_EXP_BITS :])
    return sign, exponent, fraction


def float32_bits_to_decimal(bits: BitArray) -> float:
    sign, exponent, fraction = _split_float32_bits(bits)
    if exponent == 255:
        if fraction == 0:
            return -math.inf if sign else math.inf
        return math.nan
    if exponent == 0:
        if fraction == 0:
            return -0.0 if sign else 0.0
        mantissa = fraction / (2**FLOAT_FRAC_BITS)
        value = mantissa * (2 ** (-126))
    else:
        mantissa = 1.0 + (fraction / (2**FLOAT_FRAC_BITS))
        value = mantissa * (2 ** (exponent - FLOAT_EXP_BIAS))
    return -value if sign else value


def _round_ties_to_even(value: float) -> int:
    floor_value = int(value)
    fraction = value - floor_value
    epsilon = 1e-12
    if fraction > 0.5 + epsilon:
        return floor_value + 1
    if fraction < 0.5 - epsilon:
        return floor_value
    if floor_value % 2 == 0:
        return floor_value
    return floor_value + 1


def decimal_to_float32_bits(value: float) -> BitArray:
    if math.isnan(value):
        return _compose_float32_bits(0, 255, 1)

    sign = 1 if math.copysign(1.0, value) < 0 else 0
    if math.isinf(value):
        return _compose_float32_bits(sign, 255, 0)

    abs_value = -value if value < 0 else value
    if abs_value == 0.0:
        return _compose_float32_bits(sign, 0, 0)

    exponent = 0
    normalized = abs_value
    while normalized >= 2.0:
        normalized /= 2.0
        exponent += 1
    while normalized < 1.0:
        normalized *= 2.0
        exponent -= 1

    exponent_field = exponent + FLOAT_EXP_BIAS
    if exponent_field >= 255:
        return _compose_float32_bits(sign, 255, 0)

    if exponent_field <= 0:
        scaled = abs_value * (2**149)
        fraction = _round_ties_to_even(scaled)
        if fraction <= 0:
            return _compose_float32_bits(sign, 0, 0)
        if fraction >= 2**FLOAT_FRAC_BITS:
            return _compose_float32_bits(sign, 1, 0)
        return _compose_float32_bits(sign, 0, fraction)

    raw_fraction = (normalized - 1.0) * (2**FLOAT_FRAC_BITS)
    fraction = _round_ties_to_even(raw_fraction)
    if fraction >= 2**FLOAT_FRAC_BITS:
        fraction = 0
        exponent_field += 1
        if exponent_field >= 255:
            return _compose_float32_bits(sign, 255, 0)

    return _compose_float32_bits(sign, exponent_field, fraction)


def _float_op(a: float, b: float, op: str) -> FloatOpResult:
    a_bits = decimal_to_float32_bits(a)
    b_bits = decimal_to_float32_bits(b)
    a_value = float32_bits_to_decimal(a_bits)
    b_value = float32_bits_to_decimal(b_bits)

    if op == "add":
        raw = a_value + b_value
    elif op == "sub":
        raw = a_value - b_value
    elif op == "mul":
        raw = a_value * b_value
    elif op == "div":
        if b_value == 0.0:
            if a_value == 0.0:
                raw = math.nan
            else:
                raw_sign = 1 if (math.copysign(1.0, a_value) < 0) ^ (math.copysign(1.0, b_value) < 0) else 0
                raw = -math.inf if raw_sign else math.inf
        else:
            raw = a_value / b_value
    else:
        raise ValueError("Unsupported float operation")

    result_bits = decimal_to_float32_bits(raw)
    result_decimal = float32_bits_to_decimal(result_bits)
    return FloatOpResult(a_bits=a_bits, b_bits=b_bits, result_bits=result_bits, decimal=result_decimal)


def float32_add(a: float, b: float) -> FloatOpResult:
    return _float_op(a, b, "add")


def float32_sub(a: float, b: float) -> FloatOpResult:
    return _float_op(a, b, "sub")


def float32_mul(a: float, b: float) -> FloatOpResult:
    return _float_op(a, b, "mul")


def float32_div(a: float, b: float) -> FloatOpResult:
    return _float_op(a, b, "div")
