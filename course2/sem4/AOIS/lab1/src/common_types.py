from __future__ import annotations

from dataclasses import dataclass


BIT_WIDTH = 32
MAG_WIDTH = 31
BCD_DIGITS = 8
FLOAT_EXP_BITS = 8
FLOAT_FRAC_BITS = 23
FLOAT_EXP_BIAS = 127

BitArray = list[int]


@dataclass(frozen=True)
class CodeForms:
    direct: BitArray
    ones: BitArray
    twos: BitArray


@dataclass(frozen=True)
class IntegerOpResult:
    bits: BitArray
    decimal: int
    overflow: bool
    exact_decimal: int


@dataclass(frozen=True)
class DivisionResult:
    bits: BitArray
    decimal: float
    overflow: bool
    exact_decimal: float
    remainder: int
    precision: int


@dataclass(frozen=True)
class FloatOpResult:
    a_bits: BitArray
    b_bits: BitArray
    result_bits: BitArray
    decimal: float


@dataclass(frozen=True)
class BCDOpResult:
    bits: BitArray
    decimal: int
    overflow: bool
    exact_decimal: int
