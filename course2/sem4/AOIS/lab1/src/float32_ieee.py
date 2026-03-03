from __future__ import annotations

import math

from src.bit_core import (
    _add_unsigned_bits,
    _divide_unsigned_bits,
    _fit_unsigned_to_width,
    _int_to_unsigned_bits,
    _multiply_unsigned_bits,
    _subtract_unsigned_bits,
    _unsigned_bits_to_int,
    _validate_bits,
)
from src.common_types import (
    FLOAT_EXP_BIAS,
    FLOAT_EXP_BITS,
    FLOAT_FRAC_BITS,
    FloatOpResult,
    BitArray,
)


_EXP_ALL_ONES = (1 << FLOAT_EXP_BITS) - 1
_HIDDEN_BIT = 1 << FLOAT_FRAC_BITS
_ROUND_BITS = 3
_NORMAL_EXT_MIN = _HIDDEN_BIT << _ROUND_BITS
_NORMAL_EXT_MAX = _NORMAL_EXT_MIN << 1


def _compose_float32_bits(sign: int, exponent: int, fraction: int) -> BitArray:
    if sign not in (0, 1):
        raise ValueError("sign must be 0 or 1")
    if exponent < 0 or exponent > _EXP_ALL_ONES:
        raise ValueError("Exponent out of range")
    if fraction < 0 or fraction >= (1 << FLOAT_FRAC_BITS):
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
    if exponent == _EXP_ALL_ONES:
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
        return _compose_float32_bits(0, _EXP_ALL_ONES, 1)

    sign = 1 if math.copysign(1.0, value) < 0 else 0
    if math.isinf(value):
        return _compose_float32_bits(sign, _EXP_ALL_ONES, 0)

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
    if exponent_field >= _EXP_ALL_ONES:
        return _compose_float32_bits(sign, _EXP_ALL_ONES, 0)

    if exponent_field <= 0:
        scaled = abs_value * (2**149)
        fraction = _round_ties_to_even(scaled)
        if fraction <= 0:
            return _compose_float32_bits(sign, 0, 0)
        if fraction >= (1 << FLOAT_FRAC_BITS):
            return _compose_float32_bits(sign, 1, 0)
        return _compose_float32_bits(sign, 0, fraction)

    raw_fraction = (normalized - 1.0) * (2**FLOAT_FRAC_BITS)
    fraction = _round_ties_to_even(raw_fraction)
    if fraction >= (1 << FLOAT_FRAC_BITS):
        fraction = 0
        exponent_field += 1
        if exponent_field >= _EXP_ALL_ONES:
            return _compose_float32_bits(sign, _EXP_ALL_ONES, 0)

    return _compose_float32_bits(sign, exponent_field, fraction)


def _is_nan(exponent: int, fraction: int) -> bool:
    return exponent == _EXP_ALL_ONES and fraction != 0


def _is_inf(exponent: int, fraction: int) -> bool:
    return exponent == _EXP_ALL_ONES and fraction == 0


def _is_zero(exponent: int, fraction: int) -> bool:
    return exponent == 0 and fraction == 0


def _canonical_nan_bits() -> BitArray:
    return _compose_float32_bits(0, _EXP_ALL_ONES, 1)


def _finite_to_unbiased_parts(exponent: int, fraction: int) -> tuple[int, int]:
    if exponent == 0:
        return -126, fraction
    return exponent - FLOAT_EXP_BIAS, _HIDDEN_BIT + fraction


def _shift_right_with_sticky(value: int, shift: int) -> int:
    if shift <= 0 or value == 0:
        return value
    if shift >= value.bit_length():
        return 1
    lost_mask = (1 << shift) - 1
    lost = value & lost_mask
    value >>= shift
    if lost != 0:
        value |= 1
    return value


def _unsigned_to_bits(value: int) -> BitArray:
    if value < 0:
        raise ValueError("Only non-negative values are supported")
    width = max(1, value.bit_length())
    return _int_to_unsigned_bits(value, width)


def _pack_finite_from_extended(sign: int, exponent: int, significand_ext: int) -> BitArray:
    if significand_ext == 0:
        return _compose_float32_bits(0, 0, 0)

    while significand_ext >= _NORMAL_EXT_MAX:
        significand_ext = _shift_right_with_sticky(significand_ext, 1)
        exponent += 1

    while significand_ext < _NORMAL_EXT_MIN and exponent > -126:
        significand_ext <<= 1
        exponent -= 1

    if exponent > 127:
        return _compose_float32_bits(sign, _EXP_ALL_ONES, 0)

    if exponent < -126:
        significand_ext = _shift_right_with_sticky(significand_ext, -126 - exponent)
        exponent = -126

    guard = (significand_ext >> 2) & 1
    round_bit = (significand_ext >> 1) & 1
    sticky = significand_ext & 1
    significand = significand_ext >> _ROUND_BITS

    if guard == 1 and (round_bit == 1 or sticky == 1 or (significand & 1) == 1):
        significand += 1

    if significand == 0:
        return _compose_float32_bits(0, 0, 0)

    if significand >= (_HIDDEN_BIT << 1):
        significand >>= 1
        exponent += 1
        if exponent > 127:
            return _compose_float32_bits(sign, _EXP_ALL_ONES, 0)

    if exponent > -126:
        return _compose_float32_bits(sign, exponent + FLOAT_EXP_BIAS, significand - _HIDDEN_BIT)

    if significand >= _HIDDEN_BIT:
        return _compose_float32_bits(sign, 1, significand - _HIDDEN_BIT)

    return _compose_float32_bits(sign, 0, significand)


def _add_or_sub_bits(a_bits: BitArray, b_bits: BitArray, subtract: bool) -> BitArray:
    sign_a, exponent_a, fraction_a = _split_float32_bits(a_bits)
    sign_b, exponent_b, fraction_b = _split_float32_bits(b_bits)
    if subtract:
        sign_b ^= 1

    if _is_nan(exponent_a, fraction_a) or _is_nan(exponent_b, fraction_b):
        return _canonical_nan_bits()

    if _is_inf(exponent_a, fraction_a) or _is_inf(exponent_b, fraction_b):
        if _is_inf(exponent_a, fraction_a) and _is_inf(exponent_b, fraction_b):
            if sign_a != sign_b:
                return _canonical_nan_bits()
            return _compose_float32_bits(sign_a, _EXP_ALL_ONES, 0)
        if _is_inf(exponent_a, fraction_a):
            return _compose_float32_bits(sign_a, _EXP_ALL_ONES, 0)
        return _compose_float32_bits(sign_b, _EXP_ALL_ONES, 0)

    exponent_a_unbiased, significand_a = _finite_to_unbiased_parts(exponent_a, fraction_a)
    exponent_b_unbiased, significand_b = _finite_to_unbiased_parts(exponent_b, fraction_b)
    significand_a_ext = significand_a << _ROUND_BITS
    significand_b_ext = significand_b << _ROUND_BITS

    if exponent_a_unbiased > exponent_b_unbiased:
        shift = exponent_a_unbiased - exponent_b_unbiased
        significand_b_ext = _shift_right_with_sticky(significand_b_ext, shift)
        exponent_res = exponent_a_unbiased
    elif exponent_b_unbiased > exponent_a_unbiased:
        shift = exponent_b_unbiased - exponent_a_unbiased
        significand_a_ext = _shift_right_with_sticky(significand_a_ext, shift)
        exponent_res = exponent_b_unbiased
    else:
        exponent_res = exponent_a_unbiased

    if sign_a == sign_b:
        width = max(significand_a_ext.bit_length(), significand_b_ext.bit_length(), 1)
        bits_a = _fit_unsigned_to_width(_unsigned_to_bits(significand_a_ext), width)
        bits_b = _fit_unsigned_to_width(_unsigned_to_bits(significand_b_ext), width)
        sum_bits, carry = _add_unsigned_bits(bits_a, bits_b)
        if carry == 1:
            sum_bits = [1] + sum_bits
        significand_res_ext = _unsigned_bits_to_int(sum_bits)
        sign_res = sign_a
    else:
        if significand_a_ext > significand_b_ext:
            significand_res_ext = _unsigned_bits_to_int(
                _subtract_unsigned_bits(_unsigned_to_bits(significand_a_ext), _unsigned_to_bits(significand_b_ext))
            )
            sign_res = sign_a
        elif significand_b_ext > significand_a_ext:
            significand_res_ext = _unsigned_bits_to_int(
                _subtract_unsigned_bits(_unsigned_to_bits(significand_b_ext), _unsigned_to_bits(significand_a_ext))
            )
            sign_res = sign_b
        else:
            return _compose_float32_bits(0, 0, 0)

    return _pack_finite_from_extended(sign_res, exponent_res, significand_res_ext)


def _mul_bits(a_bits: BitArray, b_bits: BitArray) -> BitArray:
    sign_a, exponent_a, fraction_a = _split_float32_bits(a_bits)
    sign_b, exponent_b, fraction_b = _split_float32_bits(b_bits)
    sign_res = sign_a ^ sign_b

    if _is_nan(exponent_a, fraction_a) or _is_nan(exponent_b, fraction_b):
        return _canonical_nan_bits()

    if (_is_inf(exponent_a, fraction_a) and _is_zero(exponent_b, fraction_b)) or (
        _is_inf(exponent_b, fraction_b) and _is_zero(exponent_a, fraction_a)
    ):
        return _canonical_nan_bits()

    if _is_inf(exponent_a, fraction_a) or _is_inf(exponent_b, fraction_b):
        return _compose_float32_bits(sign_res, _EXP_ALL_ONES, 0)

    if _is_zero(exponent_a, fraction_a) or _is_zero(exponent_b, fraction_b):
        return _compose_float32_bits(sign_res, 0, 0)

    exponent_a_unbiased, significand_a = _finite_to_unbiased_parts(exponent_a, fraction_a)
    exponent_b_unbiased, significand_b = _finite_to_unbiased_parts(exponent_b, fraction_b)
    exponent_res = exponent_a_unbiased + exponent_b_unbiased

    product = _unsigned_bits_to_int(_multiply_unsigned_bits(_unsigned_to_bits(significand_a), _unsigned_to_bits(significand_b)))
    significand_res_ext = _shift_right_with_sticky(product << _ROUND_BITS, FLOAT_FRAC_BITS)
    return _pack_finite_from_extended(sign_res, exponent_res, significand_res_ext)


def _div_bits(a_bits: BitArray, b_bits: BitArray) -> BitArray:
    sign_a, exponent_a, fraction_a = _split_float32_bits(a_bits)
    sign_b, exponent_b, fraction_b = _split_float32_bits(b_bits)
    sign_res = sign_a ^ sign_b

    if _is_nan(exponent_a, fraction_a) or _is_nan(exponent_b, fraction_b):
        return _canonical_nan_bits()

    if _is_inf(exponent_a, fraction_a) and _is_inf(exponent_b, fraction_b):
        return _canonical_nan_bits()

    if _is_zero(exponent_a, fraction_a) and _is_zero(exponent_b, fraction_b):
        return _canonical_nan_bits()

    if _is_inf(exponent_a, fraction_a):
        return _compose_float32_bits(sign_res, _EXP_ALL_ONES, 0)

    if _is_inf(exponent_b, fraction_b):
        return _compose_float32_bits(sign_res, 0, 0)

    if _is_zero(exponent_b, fraction_b):
        return _compose_float32_bits(sign_res, _EXP_ALL_ONES, 0)

    if _is_zero(exponent_a, fraction_a):
        return _compose_float32_bits(sign_res, 0, 0)

    exponent_a_unbiased, significand_a = _finite_to_unbiased_parts(exponent_a, fraction_a)
    exponent_b_unbiased, significand_b = _finite_to_unbiased_parts(exponent_b, fraction_b)
    exponent_res = exponent_a_unbiased - exponent_b_unbiased

    numerator = significand_a << (FLOAT_FRAC_BITS + _ROUND_BITS)
    quotient_bits, remainder_bits = _divide_unsigned_bits(_unsigned_to_bits(numerator), _unsigned_to_bits(significand_b))
    quotient = _unsigned_bits_to_int(quotient_bits)
    remainder = _unsigned_bits_to_int(remainder_bits)
    if remainder != 0:
        quotient |= 1
    return _pack_finite_from_extended(sign_res, exponent_res, quotient)


def _float_op(a: float, b: float, op: str) -> FloatOpResult:
    a_bits = decimal_to_float32_bits(a)
    b_bits = decimal_to_float32_bits(b)

    if op == "add":
        result_bits = _add_or_sub_bits(a_bits, b_bits, subtract=False)
    elif op == "sub":
        result_bits = _add_or_sub_bits(a_bits, b_bits, subtract=True)
    elif op == "mul":
        result_bits = _mul_bits(a_bits, b_bits)
    elif op == "div":
        result_bits = _div_bits(a_bits, b_bits)
    else:
        raise ValueError("Unsupported float operation")

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
