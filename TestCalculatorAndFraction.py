import os
import unittest

from Calculator import Calculator
from ComplexFraction import ComplexFraction
from EmptyHistoryError import EmptyHistoryError
from FileManager import FileManager
from Fraction import Fraction, MathExpression


class TestFraction(unittest.TestCase):

    # --- Constructors ---

    def test_default_constructor_gives_zero(self):
        f = Fraction()
        self.assertEqual(f.numerator, 0)
        self.assertEqual(f.denominator, 1)

    def test_int_int_constructor_reduces(self):
        f = Fraction(2, 4)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_negative_denominator_moves_sign_to_numerator(self):
        f = Fraction(1, -2)
        self.assertEqual(f.numerator, -1)
        self.assertEqual(f.denominator, 2)

    def test_both_negative_gives_positive(self):
        f = Fraction(-3, -6)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_zero_denominator_raises_value_error(self):
        with self.assertRaises(ValueError):
            Fraction(1, 0)

    def test_copy_constructor_copies_numerator_and_denominator(self):
        f1 = Fraction(1, 3)
        f2 = Fraction(f1)
        self.assertEqual(f2.numerator, 1)
        self.assertEqual(f2.denominator, 3)

    def test_copy_constructor_is_independent(self):
        f1 = Fraction(1, 3)
        f2 = Fraction(f1)
        f1.numerator = 99
        self.assertEqual(f2.numerator, 1)

    def test_float_constructor_half(self):
        f = Fraction(0.5)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_float_constructor_quarter(self):
        f = Fraction(0.25)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 4)

    def test_float_constructor_negative(self):
        f = Fraction(-0.5)
        self.assertEqual(f.numerator, -1)
        self.assertEqual(f.denominator, 2)

    def test_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            Fraction("not a fraction")

    # --- Setters ---

    def test_denominator_setter_zero_raises_value_error(self):
        f = Fraction(1, 2)
        with self.assertRaises(ValueError):
            f.denominator = 0

    def test_denominator_setter_negative_moves_sign(self):
        f = Fraction(3, 4)
        f.denominator = -4
        self.assertEqual(f.numerator, -3)
        self.assertEqual(f.denominator, 4)

    # --- from_string ---

    def test_from_string_simple_fraction(self):
        f = Fraction.from_string("3/4")
        self.assertEqual(f.numerator, 3)
        self.assertEqual(f.denominator, 4)

    def test_from_string_integer(self):
        f = Fraction.from_string("5")
        self.assertEqual(f.numerator, 5)
        self.assertEqual(f.denominator, 1)

    def test_from_string_negative_integer(self):
        f = Fraction.from_string("-3")
        self.assertEqual(f.numerator, -3)
        self.assertEqual(f.denominator, 1)

    def test_from_string_negative_fraction(self):
        f = Fraction.from_string("-1/2")
        self.assertEqual(f.numerator, -1)
        self.assertEqual(f.denominator, 2)

    def test_from_string_float_dot(self):
        f = Fraction.from_string("0.5")
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_from_string_float_comma(self):
        f = Fraction.from_string("0,5")
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_from_string_fraction_that_reduces(self):
        f = Fraction.from_string("4/8")
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_from_string_zero_denominator_raises_value_error(self):
        with self.assertRaises(ValueError):
            Fraction.from_string("1/0")

    # --- Arithmetic ---

    def test_add_two_fractions(self):
        self.assertEqual(str(Fraction(1, 2) + Fraction(1, 4)), "3/4")

    def test_sub_two_fractions(self):
        self.assertEqual(str(Fraction(1, 2) - Fraction(1, 4)), "1/4")

    def test_mul_two_fractions(self):
        self.assertEqual(str(Fraction(1, 2) * Fraction(1, 4)), "1/8")

    def test_div_two_fractions(self):
        self.assertEqual(str(Fraction(3, 4) / Fraction(1, 2)), "3/2")

    def test_add_fraction_and_int(self):
        self.assertEqual(str(Fraction(1, 2) + 2), "5/2")

    def test_sub_fraction_and_int(self):
        self.assertEqual(str(Fraction(1, 2) - 2), "-3/2")

    def test_mul_fraction_and_int(self):
        self.assertEqual(str(Fraction(1, 2) * 2), "1/1")

    def test_div_fraction_and_int(self):
        self.assertEqual(str(Fraction(1, 2) / 2), "1/4")

    def test_radd_int_plus_fraction(self):
        self.assertEqual(str(2 + Fraction(1, 2)), "5/2")

    def test_rsub_int_minus_fraction(self):
        self.assertEqual(str(2 - Fraction(1, 2)), "3/2")

    def test_rmul_int_times_fraction(self):
        self.assertEqual(str(2 * Fraction(1, 2)), "1/1")

    def test_rtruediv_int_divided_by_fraction(self):
        self.assertEqual(str(2 / Fraction(1, 2)), "4/1")

    def test_add_gives_negative_result(self):
        self.assertEqual(str(Fraction(-3, 4) + Fraction(1, 4)), "-1/2")

    def test_sub_gives_zero(self):
        self.assertEqual(str(Fraction(1, 2) - Fraction(1, 2)), "0/1")

    def test_mul_by_zero_fraction(self):
        self.assertEqual(str(Fraction(3, 4) * Fraction(0, 1)), "0/1")

    def test_div_by_negative_fraction(self):
        self.assertEqual(str(Fraction(1, 2) / Fraction(-1, 2)), "-1/1")

    def test_div_fraction_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Fraction(1, 2) / Fraction(0, 1)

    # --- __str__ ---

    def test_str_positive(self):
        self.assertEqual(str(Fraction(3, 4)), "3/4")

    def test_str_negative_numerator(self):
        self.assertEqual(str(Fraction(-1, 3)), "-1/3")

    def test_str_whole_number(self):
        self.assertEqual(str(Fraction(3, 1)), "3/1")

    # --- Harmonic series ---

    def test_harmonic_series_generator_yields_correct_fractions(self):
        elements = list(Fraction.harmonic_series(3))
        self.assertEqual(str(elements[0]), "1/1")
        self.assertEqual(str(elements[1]), "1/2")
        self.assertEqual(str(elements[2]), "1/3")

    def test_harmonic_series_generator_length_one(self):
        elements = list(Fraction.harmonic_series(1))
        self.assertEqual(len(elements), 1)
        self.assertEqual(str(elements[0]), "1/1")

    def test_harmonic_series_generator_zero_yields_nothing(self):
        elements = list(Fraction.harmonic_series(0))
        self.assertEqual(elements, [])

    def test_harmonic_sum_4_equals_25_over_12(self):
        result = Fraction.sum_harmonic_series(4)
        self.assertEqual(result.numerator, 25)
        self.assertEqual(result.denominator, 12)

    def test_harmonic_sum_1_equals_one(self):
        result = Fraction.sum_harmonic_series(1)
        self.assertEqual(result.numerator, 1)
        self.assertEqual(result.denominator, 1)

    def test_harmonic_sum_3_equals_11_over_6(self):
        result = Fraction.sum_harmonic_series(3)
        self.assertEqual(result.numerator, 11)
        self.assertEqual(result.denominator, 6)

    def test_harmonic_sum_0_returns_zero(self):
        result = Fraction.sum_harmonic_series(0)
        self.assertEqual(result.numerator, 0)
        self.assertEqual(result.denominator, 1)


class TestCalculator(unittest.TestCase):

    # --- evaluate: arithmetic ---

    def test_evaluate_addition(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("1/2 + 1/2")), "1/1")

    def test_evaluate_addition_with_integer_operand(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("4 + 1/4")), "17/4")

    def test_evaluate_subtraction(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("1/2 - 1/4")), "1/4")

    def test_evaluate_subtraction_gives_negative_result(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("1/16 - 1/4")), "-3/16")

    def test_evaluate_multiplication(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("1/16 * 1/4")), "1/64")

    def test_evaluate_division(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("3/4 : 1/2")), "3/2")

    def test_evaluate_float_operands(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("0.5 + 0.25")), "3/4")

    def test_evaluate_negative_float_operand(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("-0.5 * 2")), "-1/1")

    def test_evaluate_integer_operands(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("2 * 3")), "6/1")

    def test_evaluate_extra_whitespace_is_handled(self):
        k = Calculator()
        self.assertEqual(str(k.evaluate("  1/2   +    1/4  ")), "3/4")

    # --- evaluate: harmonic series ---

    def test_evaluate_szereg_4(self):
        k = Calculator()
        result = k.evaluate("szereg 4")
        self.assertEqual(result.numerator, 25)
        self.assertEqual(result.denominator, 12)

    def test_evaluate_szereg_1(self):
        k = Calculator()
        result = k.evaluate("szereg 1")
        self.assertEqual(result.numerator, 1)
        self.assertEqual(result.denominator, 1)

    def test_evaluate_szereg_3(self):
        k = Calculator()
        result = k.evaluate("szereg 3")
        self.assertEqual(result.numerator, 11)
        self.assertEqual(result.denominator, 6)

    def test_evaluate_szereg_0_returns_zero(self):
        k = Calculator()
        result = k.evaluate("szereg 0")
        self.assertEqual(result.numerator, 0)
        self.assertEqual(result.denominator, 1)

    # --- evaluate: error cases ---

    def test_evaluate_zero_denominator_raises_value_error(self):
        k = Calculator()
        with self.assertRaises(ValueError):
            k.evaluate("1/0 + 1/4")

    def test_evaluate_division_by_zero_fraction_raises_value_error(self):
        k = Calculator()
        with self.assertRaises(ValueError):
            k.evaluate("1/2 : 0")

    def test_evaluate_float_division_by_zero_raises_value_error(self):
        k = Calculator()
        with self.assertRaises(ValueError):
            k.evaluate("0.5 : 0")

    def test_evaluate_incomplete_expression_raises_value_error(self):
        k = Calculator()
        with self.assertRaises(ValueError):
            k.evaluate("1/2 +")

    def test_evaluate_empty_string_raises_value_error(self):
        k = Calculator()
        with self.assertRaises(ValueError):
            k.evaluate("")

    def test_evaluate_unknown_operator_raises_not_implemented_error(self):
        k = Calculator()
        with self.assertRaises(NotImplementedError):
            k.evaluate("1/2 ^ 1/4")

    def test_evaluate_text_garbage_raises_value_error(self):
        k = Calculator()
        with self.assertRaises((ValueError, TypeError)):
            k.evaluate("ala ma kota")

    # --- history ---

    def test_history_is_empty_at_start(self):
        k = Calculator()
        self.assertEqual(k.history, ())

    def test_err_history_is_empty_at_start(self):
        k = Calculator()
        self.assertEqual(k.err_history, ())

    def test_history_is_tuple(self):
        k = Calculator()
        k.add_to_history(Fraction(1, 2))
        self.assertIsInstance(k.history, tuple)

    def test_err_history_is_tuple(self):
        k = Calculator()
        k.add_to_err_history("something went wrong")
        self.assertIsInstance(k.err_history, tuple)

    def test_add_to_history_stores_fraction(self):
        k = Calculator()
        f = Fraction(1, 2)
        k.add_to_history(f)
        self.assertEqual(len(k.history), 1)
        self.assertEqual(str(k.history[0]), "1/2")

    def test_add_to_err_history_stores_message(self):
        k = Calculator()
        k.add_to_err_history("test error")
        self.assertEqual(k.err_history[0], "test error")

    def test_history_immutable_from_outside(self):
        k = Calculator()
        k.add_to_history(Fraction(1, 2))
        history = k.history
        with self.assertRaises((AttributeError, TypeError)):
            history[0] = Fraction(9, 9)

    def test_multiple_results_stored_in_order(self):
        k = Calculator()
        k.add_to_history(k.evaluate("1/2 + 1/2"))
        k.add_to_history(k.evaluate("3/4 - 1/4"))
        self.assertEqual(len(k.history), 2)
        self.assertEqual(str(k.history[0]), "1/1")
        self.assertEqual(str(k.history[1]), "1/2")

    def test_multiple_errors_stored_in_err_history(self):
        k = Calculator()
        k.add_to_err_history("first error")
        k.add_to_err_history("second error")
        self.assertEqual(len(k.err_history), 2)
        self.assertEqual(k.err_history[1], "second error")

    # --- internal methods ---

    def test_parse_math_expression_returns_math_tuple(self):
        k = Calculator()
        result = k._parse("1/2 + 1/4")
        self.assertEqual(result[0], "math")
        self.assertEqual(len(result), 4)

    def test_parse_szereg_returns_szereg_tuple(self):
        k = Calculator()
        result = k._parse("szereg 5")
        self.assertEqual(result[0], "szereg")
        self.assertEqual(result[1], 5)

    def test_compute_addition(self):
        k = Calculator()
        result = k._compute(Fraction(1, 2), "+", Fraction(1, 4))
        self.assertEqual(str(result), "3/4")

    def test_compute_subtraction(self):
        k = Calculator()
        result = k._compute(Fraction(3, 4), "-", Fraction(1, 4))
        self.assertEqual(str(result), "1/2")

    def test_compute_multiplication(self):
        k = Calculator()
        result = k._compute(Fraction(2, 3), "*", Fraction(3, 4))
        self.assertEqual(str(result), "1/2")

    def test_compute_division(self):
        k = Calculator()
        result = k._compute(Fraction(1, 2), ":", Fraction(1, 4))
        self.assertEqual(str(result), "2/1")

    def test_execute_unknown_command_type_raises_value_error(self):
        k = Calculator()
        with self.assertRaises(ValueError):
            k._execute(("ala ma kota",))


class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.filename = "test_tmp.txt"

    def tearDown(self):
        for name in [self.filename, "err_" + self.filename]:
            if os.path.exists(name):
                os.remove(name)

    # --- save ---

    def test_save_empty_history_raises_empty_history_error(self):
        k = Calculator()
        with self.assertRaises(EmptyHistoryError):
            FileManager.save_to_file(k, self.filename)

    def test_empty_history_error_is_subclass_of_exception(self):
        self.assertTrue(issubclass(EmptyHistoryError, Exception))

    def test_save_preserves_fraction_results(self):
        k = Calculator()
        k.add_to_history(Fraction(1, 2))
        k.add_to_history(Fraction(3, 4))
        FileManager.save_to_file(k, self.filename)
        with open(self.filename, "r") as f:
            lines = f.read().splitlines()
        self.assertEqual(lines[0], "1/2")
        self.assertEqual(lines[1], "3/4")

    def test_save_creates_result_file_when_history_present(self):
        k = Calculator()
        k.add_to_history(Fraction(1, 2))
        FileManager.save_to_file(k, self.filename)
        self.assertTrue(os.path.exists(self.filename))

    def test_save_creates_err_file_when_err_history_present(self):
        k = Calculator()
        k.add_to_err_history("some error")
        FileManager.save_to_file(k, self.filename)
        self.assertTrue(os.path.exists("err_" + self.filename))

    def test_save_does_not_create_result_file_when_only_errors(self):
        k = Calculator()
        k.add_to_err_history("only an error")
        FileManager.save_to_file(k, self.filename)
        self.assertFalse(os.path.exists(self.filename))

    def test_save_does_not_create_err_file_when_only_history(self):
        k = Calculator()
        k.add_to_history(Fraction(1, 2))
        FileManager.save_to_file(k, self.filename)
        self.assertFalse(os.path.exists("err_" + self.filename))

    def test_save_error_file_preserves_content(self):
        k = Calculator()
        k.add_to_err_history("ERROR: test error")
        FileManager.save_to_file(k, self.filename)
        with open("err_" + self.filename, "r") as f:
            content = f.read()
        self.assertIn("ERROR: test error", content)

    # --- load ---

    def test_load_computes_and_stores_results(self):
        with open(self.filename, "w") as f:
            f.write("1/4 + 1/4\n")
            f.write("1/2 + 1/4\n")
        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(len(k.history), 2)
        self.assertEqual(str(k.history[0]), "1/2")
        self.assertEqual(str(k.history[1]), "3/4")

    def test_load_invalid_line_goes_to_err_history(self):
        with open(self.filename, "w") as f:
            f.write("this is not a fraction\n")
        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(len(k.err_history), 1)

    def test_load_multiple_invalid_lines_all_go_to_err_history(self):
        with open(self.filename, "w") as f:
            f.write("bad line\n")
            f.write("another bad one\n")
            f.write("1/2 + 1/4\n")
        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(len(k.err_history), 2)
        self.assertEqual(len(k.history), 1)

    def test_load_empty_file_leaves_empty_history(self):
        with open(self.filename, "w") as f:
            f.write("")
        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(len(k.history), 0)

    def test_load_skips_blank_lines(self):
        with open(self.filename, "w") as f:
            f.write("\n\n1/2 + 1/4\n\n")
        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(len(k.history), 1)

    def test_load_preserves_result_order(self):
        with open(self.filename, "w") as f:
            f.write("1/3 + 1/3\n")
            f.write("1/4 + 1/4\n")
            f.write("1/5 + 1/5\n")
        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(str(k.history[0]), "2/3")
        self.assertEqual(str(k.history[1]), "1/2")
        self.assertEqual(str(k.history[2]), "2/5")

    def test_load_nonexistent_file_does_not_raise(self):
        k = Calculator()
        try:
            FileManager.load_from_file(k, "nonexistent_file_xyz_abc.txt")
        except Exception:
            self.fail("load_from_file raised an exception for a missing file")

    def test_load_nonexistent_file_leaves_empty_history(self):
        k = Calculator()
        FileManager.load_from_file(k, "nonexistent_file_xyz_abc.txt")
        self.assertEqual(len(k.history), 0)
        self.assertEqual(len(k.err_history), 0)


class TestComplexFractionConstructors(unittest.TestCase):

    def test_default_constructor_real_is_zero(self):
        c = ComplexFraction()
        self.assertEqual(c.real.numerator, 0)
        self.assertEqual(c.real.denominator, 1)

    def test_default_constructor_imag_is_one(self):
        c = ComplexFraction()
        self.assertEqual(c.imag.numerator, 1)
        self.assertEqual(c.imag.denominator, 1)

    def test_constructor_with_two_fractions(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(3, 4))
        self.assertEqual(c.real.numerator, 1)
        self.assertEqual(c.real.denominator, 2)
        self.assertEqual(c.imag.numerator, 3)
        self.assertEqual(c.imag.denominator, 4)

    def test_constructor_with_two_ints(self):
        c = ComplexFraction(2, 3)
        self.assertEqual(c.real.numerator, 2)
        self.assertEqual(c.real.denominator, 1)
        self.assertEqual(c.imag.numerator, 3)
        self.assertEqual(c.imag.denominator, 1)

    def test_constructor_with_zero_real(self):
        c = ComplexFraction(0, Fraction(1, 4))
        self.assertEqual(c.real.numerator, 0)
        self.assertEqual(c.imag.numerator, 1)
        self.assertEqual(c.imag.denominator, 4)

    def test_constructor_with_negative_real(self):
        c = ComplexFraction(Fraction(-1, 2), Fraction(1, 2))
        self.assertEqual(c.real.numerator, -1)
        self.assertEqual(c.real.denominator, 2)

    def test_constructor_with_negative_imag(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(-3, 4))
        self.assertEqual(c.imag.numerator, -3)
        self.assertEqual(c.imag.denominator, 4)

    def test_constructor_real_and_imag_are_fraction_instances(self):
        c = ComplexFraction(1, 2)
        self.assertIsInstance(c.real, Fraction)
        self.assertIsInstance(c.imag, Fraction)

    def test_constructor_reduces_real(self):
        c = ComplexFraction(Fraction(2, 4), Fraction(1, 2))
        self.assertEqual(c.real.numerator, 1)
        self.assertEqual(c.real.denominator, 2)

    def test_constructor_reduces_imag(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(4, 8))
        self.assertEqual(c.imag.numerator, 1)
        self.assertEqual(c.imag.denominator, 2)


class TestComplexFractionFromString(unittest.TestCase):

    def test_from_string_positive_imag(self):
        c = ComplexFraction.from_string("(1/2)+(1/4)i")
        self.assertEqual(c.real.numerator, 1)
        self.assertEqual(c.real.denominator, 2)
        self.assertEqual(c.imag.numerator, 1)
        self.assertEqual(c.imag.denominator, 4)

    def test_from_string_negative_imag(self):
        c = ComplexFraction.from_string("(1/2)-(1/4)i")
        self.assertEqual(c.real.numerator, 1)
        self.assertEqual(c.real.denominator, 2)
        self.assertEqual(c.imag.numerator, -1)
        self.assertEqual(c.imag.denominator, 4)

    def test_from_string_integer_parts(self):
        c = ComplexFraction.from_string("(3)+(2)i")
        self.assertEqual(c.real.numerator, 3)
        self.assertEqual(c.imag.numerator, 2)

    def test_from_string_zero_real(self):
        c = ComplexFraction.from_string("(0)+(1/2)i")
        self.assertEqual(c.real.numerator, 0)
        self.assertEqual(c.imag.numerator, 1)
        self.assertEqual(c.imag.denominator, 2)

    def test_from_string_returns_complex_fraction_instance(self):
        c = ComplexFraction.from_string("(1/2)+(1/4)i")
        self.assertIsInstance(c, ComplexFraction)

    def test_from_string_both_negative(self):
        c = ComplexFraction.from_string("(-1/2)-(-1/4)i")
        self.assertEqual(c.real.numerator, -1)
        self.assertEqual(c.imag.numerator, 1)

    def test_from_string_reduces_parts(self):
        c = ComplexFraction.from_string("(2/4)+(2/6)i")
        self.assertEqual(c.real.numerator, 1)
        self.assertEqual(c.real.denominator, 2)
        self.assertEqual(c.imag.numerator, 1)
        self.assertEqual(c.imag.denominator, 3)

    def test_from_string_garbage_raises_value_error(self):
        with self.assertRaises(ValueError):
            ComplexFraction.from_string("ala")

    def test_from_string_missing_parens_raises_value_error(self):
        with self.assertRaises(ValueError):
            ComplexFraction.from_string("1/2+1/4i")

    def test_from_string_empty_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            ComplexFraction.from_string("")


class TestComplexFractionStr(unittest.TestCase):

    def test_str_positive_imag(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        self.assertEqual(str(c), "(1/2)+(1/4)i")

    def test_str_negative_imag(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(-1, 4))
        self.assertEqual(str(c), "(1/2)-(1/4)i")

    def test_str_zero_real(self):
        c = ComplexFraction(Fraction(0, 1), Fraction(1, 3))
        self.assertEqual(str(c), "(0/1)+(1/3)i")

    def test_str_roundtrip_positive(self):
        c = ComplexFraction(Fraction(3, 4), Fraction(1, 2))
        c2 = ComplexFraction.from_string(str(c))
        self.assertEqual(c2.real.numerator, 3)
        self.assertEqual(c2.real.denominator, 4)
        self.assertEqual(c2.imag.numerator, 1)
        self.assertEqual(c2.imag.denominator, 2)

    def test_str_roundtrip_negative_imag(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(-3, 4))
        c2 = ComplexFraction.from_string(str(c))
        self.assertEqual(c2.imag.numerator, -3)
        self.assertEqual(c2.imag.denominator, 4)


class TestComplexFractionReduce(unittest.TestCase):

    def test_reduce_reduces_real(self):
        c = ComplexFraction(Fraction(2, 4), Fraction(1, 2))
        c.reduce()
        self.assertEqual(c.real.numerator, 1)
        self.assertEqual(c.real.denominator, 2)

    def test_reduce_reduces_imag(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(6, 9))
        c.reduce()
        self.assertEqual(c.imag.numerator, 2)
        self.assertEqual(c.imag.denominator, 3)

    def test_reduce_already_reduced_stays_same(self):
        c = ComplexFraction(Fraction(1, 3), Fraction(2, 5))
        c.reduce()
        self.assertEqual(c.real.numerator, 1)
        self.assertEqual(c.real.denominator, 3)
        self.assertEqual(c.imag.numerator, 2)
        self.assertEqual(c.imag.denominator, 5)


class TestComplexFractionAddition(unittest.TestCase):

    def test_add_two_complex_fractions(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        c2 = ComplexFraction(Fraction(1, 4), Fraction(1, 4))
        result = c1 + c2
        self.assertEqual(str(result.real), "3/4")
        self.assertEqual(str(result.imag), "1/2")

    def test_add_returns_complex_fraction(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 2))
        c2 = ComplexFraction(Fraction(1, 2), Fraction(1, 2))
        self.assertIsInstance(c1 + c2, ComplexFraction)

    def test_add_with_zero_complex(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        c2 = ComplexFraction(Fraction(0, 1), Fraction(0, 1))
        result = c1 + c2
        self.assertEqual(str(result.real), "1/2")
        self.assertEqual(str(result.imag), "1/4")

    def test_add_complex_and_int(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        result = c + 1
        self.assertEqual(str(result.real), "3/2")
        self.assertEqual(str(result.imag), "1/4")

    def test_add_complex_and_fraction(self):
        c = ComplexFraction(Fraction(1, 4), Fraction(1, 4))
        result = c + Fraction(1, 4)
        self.assertEqual(str(result.real), "1/2")
        self.assertEqual(str(result.imag), "1/4")

    def test_radd_int_plus_complex(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        result = 1 + c
        self.assertEqual(str(result.real), "3/2")

    def test_add_negative_imaginary_parts(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(-1, 4))
        c2 = ComplexFraction(Fraction(1, 4), Fraction(-1, 4))
        result = c1 + c2
        self.assertEqual(str(result.imag), "-1/2")

    def test_add_gives_zero_imag(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        c2 = ComplexFraction(Fraction(1, 4), Fraction(-1, 4))
        result = c1 + c2
        self.assertEqual(str(result.imag), "0/1")


class TestComplexFractionSubtraction(unittest.TestCase):

    def test_sub_two_complex_fractions(self):
        c1 = ComplexFraction(Fraction(3, 4), Fraction(1, 2))
        c2 = ComplexFraction(Fraction(1, 4), Fraction(1, 4))
        result = c1 - c2
        self.assertEqual(str(result.real), "1/2")
        self.assertEqual(str(result.imag), "1/4")

    def test_sub_returns_complex_fraction(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 2))
        c2 = ComplexFraction(Fraction(1, 4), Fraction(1, 4))
        self.assertIsInstance(c1 - c2, ComplexFraction)

    def test_sub_gives_zero_real(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        c2 = ComplexFraction(Fraction(1, 2), Fraction(0, 1))
        result = c1 - c2
        self.assertEqual(str(result.real), "0/1")

    def test_sub_complex_and_int(self):
        c = ComplexFraction(Fraction(3, 2), Fraction(1, 4))
        result = c - 1
        self.assertEqual(str(result.real), "1/2")
        self.assertEqual(str(result.imag), "1/4")

    def test_sub_complex_and_fraction(self):
        c = ComplexFraction(Fraction(3, 4), Fraction(1, 4))
        result = c - Fraction(1, 4)
        self.assertEqual(str(result.real), "1/2")

    def test_rsub_int_minus_complex(self):
        c = ComplexFraction(Fraction(1, 4), Fraction(1, 4))
        result = 1 - c
        self.assertEqual(str(result.real), "3/4")

    def test_rsub_negates_imag(self):
        c = ComplexFraction(Fraction(1, 4), Fraction(1, 4))
        result = 1 - c
        self.assertEqual(str(result.imag), "-1/4")

    def test_sub_same_gives_zero(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        c2 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        result = c1 - c2
        self.assertEqual(str(result.real), "0/1")
        self.assertEqual(str(result.imag), "0/1")


class TestComplexFractionMultiplication(unittest.TestCase):

    def test_mul_two_complex_fractions(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 3))
        c2 = ComplexFraction(Fraction(2, 1), Fraction(3, 1))
        result = c1 * c2
        self.assertEqual(str(result.real), "0/1")
        self.assertEqual(str(result.imag), "13/6")

    def test_mul_returns_complex_fraction(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        c2 = ComplexFraction(Fraction(2, 1), Fraction(1, 1))
        self.assertIsInstance(c1 * c2, ComplexFraction)

    def test_mul_by_one_plus_zero_i(self):
        c1 = ComplexFraction(Fraction(3, 4), Fraction(1, 2))
        c2 = ComplexFraction(Fraction(1, 1), Fraction(0, 1))
        result = c1 * c2
        self.assertEqual(str(result.real), "3/4")
        self.assertEqual(str(result.imag), "1/2")

    def test_mul_complex_and_int(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        result = c * 2
        self.assertEqual(str(result.real), "1/1")
        self.assertEqual(str(result.imag), "1/2")

    def test_mul_complex_and_fraction(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        result = c * Fraction(2, 1)
        self.assertEqual(str(result.real), "1/1")
        self.assertEqual(str(result.imag), "1/2")

    def test_rmul_int_times_complex(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        result = 2 * c
        self.assertEqual(str(result.real), "1/1")
        self.assertEqual(str(result.imag), "1/2")

    def test_mul_by_zero_gives_zero(self):
        c = ComplexFraction(Fraction(3, 4), Fraction(1, 2))
        result = c * 0
        self.assertEqual(str(result.real), "0/1")
        self.assertEqual(str(result.imag), "0/1")

    def test_mul_i_squared_gives_minus_one(self):
        c1 = ComplexFraction(Fraction(0, 1), Fraction(1, 1))
        c2 = ComplexFraction(Fraction(0, 1), Fraction(1, 1))
        result = c1 * c2
        self.assertEqual(str(result.real), "-1/1")
        self.assertEqual(str(result.imag), "0/1")


class TestComplexFractionDivision(unittest.TestCase):

    def test_div_two_complex_fractions(self):
        c1 = ComplexFraction(Fraction(1, 1), Fraction(2, 1))
        c2 = ComplexFraction(Fraction(1, 1), Fraction(1, 1))
        result = c1 / c2
        self.assertEqual(str(result.real), "3/2")
        self.assertEqual(str(result.imag), "1/2")

    def test_div_returns_complex_fraction(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        c2 = ComplexFraction(Fraction(1, 1), Fraction(0, 1))
        self.assertIsInstance(c1 / c2, ComplexFraction)

    def test_div_by_one_plus_zero_i_gives_same(self):
        c1 = ComplexFraction(Fraction(3, 4), Fraction(1, 2))
        c2 = ComplexFraction(Fraction(1, 1), Fraction(0, 1))
        result = c1 / c2
        self.assertEqual(str(result.real), "3/4")
        self.assertEqual(str(result.imag), "1/2")

    def test_div_complex_by_int(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        result = c / 2
        self.assertEqual(str(result.real), "1/4")
        self.assertEqual(str(result.imag), "1/8")

    def test_div_complex_by_fraction(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        result = c / Fraction(1, 2)
        self.assertEqual(str(result.real), "1/1")
        self.assertEqual(str(result.imag), "1/2")

    def test_rtruediv_int_by_complex(self):
        c = ComplexFraction(Fraction(1, 1), Fraction(0, 1))
        result = 1 / c
        self.assertEqual(str(result.real), "1/1")

    def test_rtruediv_negates_imag(self):
        c = ComplexFraction(Fraction(0, 1), Fraction(1, 1))
        result = 1 / c
        self.assertEqual(str(result.real), "0/1")
        self.assertEqual(str(result.imag), "-1/1")

    def test_div_by_zero_raises(self):
        c1 = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        c2 = ComplexFraction(Fraction(0, 1), Fraction(0, 1))
        with self.assertRaises((ValueError, ZeroDivisionError)):
            _ = c1 / c2


class TestMathExpression(unittest.TestCase):

    def test_math_expression_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            MathExpression()

    def test_fraction_is_math_expression(self):
        f = Fraction(1, 2)
        self.assertIsInstance(f, MathExpression)

    def test_complex_fraction_is_math_expression(self):
        c = ComplexFraction(Fraction(1, 2), Fraction(1, 4))
        self.assertIsInstance(c, MathExpression)

    def test_fraction_subclasses_math_expression(self):
        self.assertTrue(issubclass(Fraction, MathExpression))

    def test_complex_fraction_subclasses_math_expression(self):
        self.assertTrue(issubclass(ComplexFraction, MathExpression))


class TestEmptyHistoryError(unittest.TestCase):

    def test_empty_history_error_is_exception(self):
        self.assertTrue(issubclass(EmptyHistoryError, Exception))

    def test_empty_history_error_can_be_raised(self):
        with self.assertRaises(EmptyHistoryError):
            raise EmptyHistoryError

    def test_empty_history_error_can_be_raised_with_message(self):
        with self.assertRaises(EmptyHistoryError):
            raise EmptyHistoryError("ala ma kota")

    def test_empty_history_error_caught_as_exception(self):
        caught = False
        try:
            raise EmptyHistoryError("ala")
        except Exception:
            caught = True
        self.assertTrue(caught)

    def test_empty_history_error_not_caught_as_value_error(self):
        with self.assertRaises(EmptyHistoryError):
            try:
                raise EmptyHistoryError("ala")
            except ValueError:
                pass


class TestCalculatorWithComplexFractions(unittest.TestCase):

    def test_evaluate_complex_addition(self):
        k = Calculator()
        result = k.evaluate("(1/2)+(1/4)i + (1/4)+(1/4)i")
        self.assertEqual(str(result.real), "3/4")
        self.assertEqual(str(result.imag), "1/2")

    def test_evaluate_complex_subtraction(self):
        k = Calculator()
        result = k.evaluate("(3/4)+(1/2)i - (1/4)+(1/4)i")
        self.assertEqual(str(result.real), "1/2")
        self.assertEqual(str(result.imag), "1/4")

    def test_evaluate_complex_multiplication(self):
        k = Calculator()
        result = k.evaluate("(0/1)+(1/1)i * (0/1)+(1/1)i")
        self.assertEqual(str(result.real), "-1/1")

    def test_evaluate_complex_division(self):
        k = Calculator()
        result = k.evaluate("(1/1)+(2/1)i : (1/1)+(1/1)i")
        self.assertEqual(str(result.real), "3/2")
        self.assertEqual(str(result.imag), "1/2")

    def test_evaluate_complex_result_is_complex_fraction(self):
        k = Calculator()
        result = k.evaluate("(1/2)+(1/4)i + (1/4)+(1/4)i")
        self.assertIsInstance(result, ComplexFraction)

    def test_history_stores_complex_fraction(self):
        k = Calculator()
        result = k.evaluate("(1/2)+(1/4)i + (1/4)+(1/4)i")
        k.add_to_history(result)
        self.assertIsInstance(k.history[0], ComplexFraction)

    def test_parse_operand_with_i_returns_complex_fraction(self):
        k = Calculator()
        result = k._parse_operand("(1/2)+(1/4)i")
        self.assertIsInstance(result, ComplexFraction)

    def test_parse_operand_without_i_returns_fraction(self):
        k = Calculator()
        result = k._parse_operand("1/2")
        self.assertIsInstance(result, Fraction)


if __name__ == "__main__":
    unittest.main()
