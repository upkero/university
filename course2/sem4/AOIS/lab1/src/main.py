from __future__ import annotations

from src import (
    add_excess3,
    add_in_twos_complement,
    bits_to_string,
    decimal_to_all_codes,
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
    try:
        n = int(input("Integer for code conversion (direct/ones/twos): "))
        codes = decimal_to_all_codes(n)
        _print_int_result("Direct code", codes.direct, n)
        _print_int_result("Ones' complement", codes.ones, n)
        _print_int_result("Two's complement", codes.twos, n)

        a = int(input("First integer (for +, -, *, /): "))
        b = int(input("Second integer (for +, -, *, /): "))

        add_result = add_in_twos_complement(a, b)
        _print_int_result("Two's complement addition", add_result.bits, add_result.decimal)

        sub_result = subtract_in_twos_complement(a, b)
        _print_int_result("Two's complement subtraction", sub_result.bits, sub_result.decimal)

        mul_result = multiply_in_sign_magnitude(a, b)
        _print_int_result("Sign-magnitude multiplication", mul_result.bits, mul_result.decimal)

        div_result = divide_in_sign_magnitude(a, b, precision=5)
        print("Sign-magnitude division (precision 5)")
        print(f"2:  {bits_to_string(div_result.bits)}")
        print(f"10: {div_result.decimal:.5f}")
        print()

        fa = float(input("First float (IEEE-754 float32): "))
        fb = float(input("Second float (IEEE-754 float32): "))

        for title, op in (
            ("IEEE-754 float32 addition", float32_add),
            ("IEEE-754 float32 subtraction", float32_sub),
            ("IEEE-754 float32 multiplication", float32_mul),
            ("IEEE-754 float32 division", float32_div),
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

        bcd_a = int(input("First number for Excess-3 (0..99999999): "))
        bcd_b = int(input("Second number for Excess-3 (0..99999999): "))
        bcd_result = add_excess3(bcd_a, bcd_b)
        print("BCD Excess-3 addition")
        print(f"2:  {bits_to_string(bcd_result.bits)}")
        print(f"10: {bcd_result.decimal}")
        print()

        print("Done.")
    except (ValueError, OverflowError, ZeroDivisionError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
