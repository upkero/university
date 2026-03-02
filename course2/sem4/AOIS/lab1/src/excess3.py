from __future__ import annotations

from src.bit_core import _int_to_unsigned_bits, _unsigned_bits_to_int, _validate_bits
from src.common_types import BCD_DIGITS, BIT_WIDTH, BCDOpResult, BitArray


def _non_negative_int_to_digits(value: int) -> list[int]:
    if value < 0:
        raise ValueError("Value must be non-negative")
    if value == 0:
        return [0]

    reversed_digits: list[int] = []
    current = value
    while current > 0:
        reversed_digits.append(current % 10)
        current //= 10

    digits: list[int] = []
    for index in range(len(reversed_digits) - 1, -1, -1):
        digits.append(reversed_digits[index])
    return digits


def _digits_to_int(digits: list[int]) -> int:
    value = 0
    for digit in digits:
        value = value * 10 + digit
    return value


def decimal_to_excess3_bits(value: int) -> BitArray:
    digits = _non_negative_int_to_digits(value)
    if len(digits) > BCD_DIGITS:
        raise OverflowError("Excess-3 format supports up to 8 decimal digits in 32 bits")

    bits = [0] * BIT_WIDTH
    zero_code = _int_to_unsigned_bits(3, 4)
    for nibble_index in range(BCD_DIGITS):
        start = nibble_index * 4
        bits[start : start + 4] = zero_code

    offset = BCD_DIGITS - len(digits)
    for index, digit in enumerate(digits):
        code = digit + 3
        code_bits = _int_to_unsigned_bits(code, 4)
        start = (offset + index) * 4
        bits[start : start + 4] = code_bits
    return bits


def excess3_bits_to_decimal(bits: BitArray) -> int:
    _validate_bits(bits)
    digits: list[int] = []
    for nibble_index in range(BCD_DIGITS):
        start = nibble_index * 4
        code = _unsigned_bits_to_int(bits[start : start + 4])
        if code < 3 or code > 12:
            raise ValueError("Invalid Excess-3 nibble")
        digits.append(code - 3)

    first_non_zero = 0
    while first_non_zero < len(digits) - 1 and digits[first_non_zero] == 0:
        first_non_zero += 1
    return _digits_to_int(digits[first_non_zero:])


def add_excess3(a: int, b: int) -> BCDOpResult:
    if a < 0 or b < 0:
        raise ValueError("Excess-3 addition in this implementation supports non-negative integers only")

    a_bits = decimal_to_excess3_bits(a)
    b_bits = decimal_to_excess3_bits(b)
    result = [0] * BIT_WIDTH
    carry = 0

    for nibble_index in range(BCD_DIGITS - 1, -1, -1):
        start = nibble_index * 4
        a_code = _unsigned_bits_to_int(a_bits[start : start + 4])
        b_code = _unsigned_bits_to_int(b_bits[start : start + 4])
        raw_sum = a_code + b_code + carry

        if raw_sum >= 16:
            carry = 1
            corrected = (raw_sum - 16) + 3
        else:
            carry = 0
            corrected = raw_sum - 3

        if corrected < 0 or corrected > 15:
            raise ValueError("Unexpected Excess-3 correction result")

        result[start : start + 4] = _int_to_unsigned_bits(corrected, 4)

    overflow = carry == 1
    stored_decimal = excess3_bits_to_decimal(result)
    exact_decimal = a + b
    return BCDOpResult(bits=result, decimal=stored_decimal, overflow=overflow, exact_decimal=exact_decimal)
