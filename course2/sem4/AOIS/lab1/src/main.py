from __future__ import annotations

from src import (
    add_excess3,
    add_in_twos_complement,
    bits_to_string,
    decimal_to_all_codes,
    decimal_to_float32_bits,
    divide_in_sign_magnitude,
    float32_add,
    float32_bits_to_decimal,
    float32_div,
    float32_mul,
    float32_sub,
    multiply_in_sign_magnitude,
    subtract_in_twos_complement,
)


def _print_int_result(title: str, result_bits: list[int], result_decimal: int) -> None:
    print(title)
    print(f"2:  {bits_to_string(result_bits)}")
    print(f"10: {result_decimal}")
    print()


def main() -> None:
    n = int(input("Число для перевода в прямой/обратный/дополнительный код: "))
    codes = decimal_to_all_codes(n)
    _print_int_result("Прямой код", codes.direct, n)
    _print_int_result("Обратный код", codes.ones, n)
    _print_int_result("Дополнительный код", codes.twos, n)

    a = int(input("Первое целое число (для +, -, *, /): "))
    b = int(input("Второе целое число (для +, -, *, /): "))

    add_result = add_in_twos_complement(a, b)
    _print_int_result("Сложение в дополнительном коде", add_result.bits, add_result.decimal)

    sub_result = subtract_in_twos_complement(a, b)
    _print_int_result("Вычитание (через отрицание + сложение) в дополнительном коде", sub_result.bits, sub_result.decimal)

    mul_result = multiply_in_sign_magnitude(a, b)
    _print_int_result("Умножение в прямом коде", mul_result.bits, mul_result.decimal)

    div_result = divide_in_sign_magnitude(a, b, precision=5)
    print("Деление в прямом коде (точность 5 знаков)")
    print(f"2:  {bits_to_string(div_result.bits)}")
    print(f"10: {div_result.decimal:.5f}")
    print()

    fa = float(input("Первое число с плавающей точкой (IEEE-754 float32): "))
    fb = float(input("Второе число с плавающей точкой (IEEE-754 float32): "))

    for title, op in (
        ("IEEE-754 float32 сложение", float32_add),
        ("IEEE-754 float32 вычитание", float32_sub),
        ("IEEE-754 float32 умножение", float32_mul),
        ("IEEE-754 float32 деление", float32_div),
    ):
        result = op(fa, fb)
        print(title)
        print(f"A (2): {bits_to_string(result.a_bits)}")
        print(f"A (10): {float32_bits_to_decimal(result.a_bits)}")
        print(f"B (2): {bits_to_string(result.b_bits)}")
        print(f"B (10): {float32_bits_to_decimal(result.b_bits)}")
        print(f"R (2): {bits_to_string(result.result_bits)}")
        print(f"R (10): {result.decimal}")
        print()

    bcd_a = int(input("Первое число для Excess-3 (0..99999999): "))
    bcd_b = int(input("Второе число для Excess-3 (0..99999999): "))
    bcd_result = add_excess3(bcd_a, bcd_b)
    print("Сложение в BCD Excess-3")
    print(f"2:  {bits_to_string(bcd_result.bits)}")
    print(f"10: {bcd_result.decimal}")
    print()

    print("Готово.")


if __name__ == "__main__":
    main()
