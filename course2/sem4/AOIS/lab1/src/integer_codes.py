from __future__ import annotations

from src.bit_core import (
    _int_to_unsigned_bits,
    _max_magnitude,
    _negate_twos,
    _twos_modulus,
    _unsigned_bits_to_int,
    _validate_bits,
    invert_bits,
)
from src.common_types import BIT_WIDTH, CodeForms, BitArray


def decimal_to_sign_magnitude(value: int) -> BitArray:
    abs_value = -value if value < 0 else value
    if abs_value > _max_magnitude():
        raise OverflowError("Value does not fit in sign-magnitude 32-bit format")
    magnitude = _int_to_unsigned_bits(abs_value, 31)
    sign = 1 if value < 0 else 0
    return [sign] + magnitude


def sign_magnitude_to_decimal(bits: BitArray) -> int:
    _validate_bits(bits)
    sign = bits[0]
    magnitude = _unsigned_bits_to_int(bits[1:])
    if sign == 1 and magnitude == 0:
        return 0
    return -magnitude if sign else magnitude


def decimal_to_ones_complement(value: int) -> BitArray:
    abs_value = -value if value < 0 else value
    if abs_value > _max_magnitude():
        raise OverflowError("Value does not fit in ones' complement 32-bit format")
    positive = _int_to_unsigned_bits(abs_value, BIT_WIDTH)
    if value >= 0:
        return positive
    return invert_bits(positive)


def ones_complement_to_decimal(bits: BitArray) -> int:
    _validate_bits(bits)
    if bits[0] == 0:
        return _unsigned_bits_to_int(bits)
    if all(bit == 1 for bit in bits):
        return 0
    inverted = invert_bits(bits)
    return -_unsigned_bits_to_int(inverted)


def decimal_to_twos_complement(value: int) -> BitArray:
    min_value = -(_twos_modulus() // 2)
    max_value = (_twos_modulus() // 2) - 1
    if value < min_value or value > max_value:
        raise OverflowError("Value does not fit in two's complement 32-bit format")
    if value >= 0:
        return _int_to_unsigned_bits(value, BIT_WIDTH)
    abs_value = -value
    positive = _int_to_unsigned_bits(abs_value, BIT_WIDTH)
    return _negate_twos(positive)


def twos_complement_to_decimal(bits: BitArray) -> int:
    _validate_bits(bits)
    if bits[0] == 0:
        return _unsigned_bits_to_int(bits)
    positive = _negate_twos(bits)
    return -_unsigned_bits_to_int(positive)


def decimal_to_all_codes(value: int) -> CodeForms:
    return CodeForms(
        direct=decimal_to_sign_magnitude(value),
        ones=decimal_to_ones_complement(value),
        twos=decimal_to_twos_complement(value),
    )
