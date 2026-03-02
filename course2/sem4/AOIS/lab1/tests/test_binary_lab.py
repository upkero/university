from __future__ import annotations

import math

import pytest

import src
from src import (
    add_excess3,
    add_in_twos_complement,
    bits_to_string,
    decimal_to_all_codes,
    decimal_to_excess3_bits,
    decimal_to_float32_bits,
    decimal_to_ones_complement,
    decimal_to_sign_magnitude,
    decimal_to_twos_complement,
    divide_in_sign_magnitude,
    excess3_bits_to_decimal,
    float32_add,
    float32_bits_to_decimal,
    float32_div,
    float32_mul,
    float32_sub,
    invert_bits,
    multiply_in_sign_magnitude,
    ones_complement_to_decimal,
    sign_magnitude_to_decimal,
    subtract_in_twos_complement,
    twos_complement_to_decimal,
)
from src.main import main


def test_public_api_from_init_all() -> None:
    for name in src.__all__:
        assert hasattr(src, name)


def test_all_codes_for_positive_value() -> None:
    forms = decimal_to_all_codes(5)
    assert bits_to_string(forms.direct) == "00000000000000000000000000000101"
    assert bits_to_string(forms.ones) == "00000000000000000000000000000101"
    assert bits_to_string(forms.twos) == "00000000000000000000000000000101"


def test_all_codes_for_negative_value() -> None:
    forms = decimal_to_all_codes(-5)
    assert bits_to_string(forms.direct) == "10000000000000000000000000000101"
    assert bits_to_string(forms.ones) == "11111111111111111111111111111010"
    assert bits_to_string(forms.twos) == "11111111111111111111111111111011"


@pytest.mark.parametrize("value", [-1024, -1, 0, 1, 1024])
def test_sign_magnitude_roundtrip(value: int) -> None:
    bits = decimal_to_sign_magnitude(value)
    assert sign_magnitude_to_decimal(bits) == value


def test_sign_magnitude_overflow() -> None:
    with pytest.raises(OverflowError):
        decimal_to_sign_magnitude(2**31)


def test_ones_complement_roundtrip_and_negative_zero() -> None:
    for value in (-12345, -1, 0, 42):
        bits = decimal_to_ones_complement(value)
        assert ones_complement_to_decimal(bits) == value
    assert ones_complement_to_decimal([1] * 32) == 0


def test_ones_complement_overflow() -> None:
    with pytest.raises(OverflowError):
        decimal_to_ones_complement(-(2**31))


@pytest.mark.parametrize("value", [-(2**31), -255, -1, 0, 1, 255, (2**31) - 1])
def test_twos_complement_roundtrip(value: int) -> None:
    bits = decimal_to_twos_complement(value)
    assert twos_complement_to_decimal(bits) == value


def test_twos_complement_overflow() -> None:
    with pytest.raises(OverflowError):
        decimal_to_twos_complement(2**31)
    with pytest.raises(OverflowError):
        decimal_to_twos_complement(-(2**31) - 1)


def test_twos_addition_regular_and_overflow() -> None:
    regular = add_in_twos_complement(10, -3)
    assert regular.decimal == 7
    assert regular.overflow is False
    assert regular.exact_decimal == 7

    overflow = add_in_twos_complement((2**31) - 1, 1)
    assert overflow.decimal == -(2**31)
    assert overflow.overflow is True
    assert overflow.exact_decimal == 2**31


def test_twos_subtraction_via_negation_and_addition() -> None:
    result = subtract_in_twos_complement(10, 3)
    assert result.decimal == 7
    assert result.overflow is False
    assert result.exact_decimal == 7

    overflow = subtract_in_twos_complement(-(2**31), 1)
    assert overflow.decimal == (2**31) - 1
    assert overflow.overflow is True
    assert overflow.exact_decimal == -(2**31) - 1


def test_invert_bits() -> None:
    bits = [0] * 31 + [1]
    assert invert_bits(bits) == [1] * 31 + [0]


def test_multiply_in_sign_magnitude_regular_and_overflow() -> None:
    regular = multiply_in_sign_magnitude(-7, 3)
    assert regular.decimal == -21
    assert regular.exact_decimal == -21
    assert regular.overflow is False

    overflow = multiply_in_sign_magnitude(50_000, 50_000)
    assert overflow.overflow is True
    assert overflow.exact_decimal == 2_500_000_000
    assert overflow.decimal == 352_516_352


def test_divide_in_sign_magnitude_regular_negative_and_overflow() -> None:
    regular = divide_in_sign_magnitude(7, 2, precision=5)
    assert regular.decimal == pytest.approx(3.5, abs=1e-8)
    assert regular.exact_decimal == pytest.approx(3.5, abs=1e-8)
    assert regular.overflow is False

    negative = divide_in_sign_magnitude(-1, 8, precision=5)
    assert negative.decimal == pytest.approx(-0.125, abs=1e-8)
    assert negative.exact_decimal == pytest.approx(-0.125, abs=1e-8)

    overflow = divide_in_sign_magnitude((2**31) - 1, 1, precision=5)
    assert overflow.overflow is True


def test_divide_in_sign_magnitude_raises() -> None:
    with pytest.raises(ZeroDivisionError):
        divide_in_sign_magnitude(1, 0, precision=5)
    with pytest.raises(ValueError):
        divide_in_sign_magnitude(1, 1, precision=-1)


def test_float32_encoding_known_patterns() -> None:
    one = decimal_to_float32_bits(1.0)
    minus_two_and_half = decimal_to_float32_bits(-2.5)
    assert bits_to_string(one) == "00111111100000000000000000000000"
    assert bits_to_string(minus_two_and_half) == "11000000001000000000000000000000"


def test_float32_decode_known_patterns() -> None:
    one_bits = [int(ch) for ch in "00111111100000000000000000000000"]
    minus_two_and_half_bits = [int(ch) for ch in "11000000001000000000000000000000"]
    assert float32_bits_to_decimal(one_bits) == pytest.approx(1.0)
    assert float32_bits_to_decimal(minus_two_and_half_bits) == pytest.approx(-2.5)


def test_float32_special_values() -> None:
    inf_bits = decimal_to_float32_bits(math.inf)
    ninf_bits = decimal_to_float32_bits(-math.inf)
    nan_bits = decimal_to_float32_bits(math.nan)
    tiny_bits = decimal_to_float32_bits(1e-45)
    huge_bits = decimal_to_float32_bits(1e40)

    assert math.isinf(float32_bits_to_decimal(inf_bits))
    assert math.isinf(float32_bits_to_decimal(ninf_bits))
    assert math.isnan(float32_bits_to_decimal(nan_bits))
    assert tiny_bits[1:9] == [0] * 8
    assert huge_bits[1:9] == [1] * 8


def test_float32_operations() -> None:
    add_result = float32_add(1.25, 2.5)
    sub_result = float32_sub(5.5, 2.25)
    mul_result = float32_mul(-3.0, 0.5)
    div_result = float32_div(7.0, 2.0)

    assert add_result.decimal == pytest.approx(3.75, abs=1e-6)
    assert sub_result.decimal == pytest.approx(3.25, abs=1e-6)
    assert mul_result.decimal == pytest.approx(-1.5, abs=1e-6)
    assert div_result.decimal == pytest.approx(3.5, abs=1e-6)


def test_float32_division_by_zero_semantics() -> None:
    inf_result = float32_div(1.0, 0.0)
    nan_result = float32_div(0.0, 0.0)
    assert math.isinf(inf_result.decimal)
    assert math.isnan(nan_result.decimal)


def test_excess3_roundtrip_and_bounds() -> None:
    bits = decimal_to_excess3_bits(12_345_678)
    assert excess3_bits_to_decimal(bits) == 12_345_678
    assert excess3_bits_to_decimal(decimal_to_excess3_bits(0)) == 0
    with pytest.raises(OverflowError):
        decimal_to_excess3_bits(100_000_000)


def test_excess3_invalid_nibble() -> None:
    bad = [0] * 32
    with pytest.raises(ValueError):
        excess3_bits_to_decimal(bad)


def test_add_excess3_regular_and_overflow() -> None:
    regular = add_excess3(59, 73)
    assert regular.decimal == 132
    assert regular.exact_decimal == 132
    assert regular.overflow is False

    overflow = add_excess3(99_999_999, 1)
    assert overflow.overflow is True
    assert overflow.decimal == 0
    assert overflow.exact_decimal == 100_000_000


def test_add_excess3_negative_values_not_supported() -> None:
    with pytest.raises(ValueError):
        add_excess3(-1, 2)


def test_bits_validation() -> None:
    with pytest.raises(ValueError):
        bits_to_string([0, 1, 0])
    with pytest.raises(ValueError):
        twos_complement_to_decimal([0] * 31 + [2])


def test_main_smoke(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    answers = iter(
        [
            "5",     # conversion number
            "7",     # integer a
            "2",     # integer b
            "1.5",   # float a
            "0.5",   # float b
            "12",    # bcd a
            "34",    # bcd b
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    main()
    output = capsys.readouterr().out
    assert "Прямой код" in output
    assert "IEEE-754 float32 сложение" in output
    assert "Сложение в BCD Excess-3" in output
    assert "Готово." in output
