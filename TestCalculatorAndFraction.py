import unittest
import os
from Fraction import Fraction
from Calculator import Calculator
from FileManager import FileManager


class TestFraction(unittest.TestCase):
    def test_creation_reduces(self):
        f = Fraction(2, 4)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_negative_denominator_moves_sign(self):
        f = Fraction(1, -2)
        self.assertEqual(f.numerator, -1)
        self.assertEqual(f.denominator, 2)

    def test_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            Fraction(1, 0)

    def test_property_setter_zero_raises(self):
        f = Fraction(1, 2)
        with self.assertRaises(ValueError):
            f.denominator = 0

    def test_init_invalid_type_raises(self):
        with self.assertRaises(TypeError):
            Fraction("ala ma kota")

    def test_from_string(self):
        f = Fraction.from_string("3/4")
        self.assertEqual(f.numerator, 3)
        self.assertEqual(f.denominator, 4)

    def test_from_string_integer(self):
        f = Fraction.from_string("5")
        self.assertEqual(f.numerator, 5)
        self.assertEqual(f.denominator, 1)

    def test_copy_constructor(self):
        f1 = Fraction(1, 3)
        f2 = Fraction(f1)
        self.assertEqual(f2.numerator, 1)
        self.assertEqual(f2.denominator, 3)

    def test_float_constructor(self):
        f = Fraction(0.5)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_add(self):
        self.assertEqual(str(Fraction(1, 2) + Fraction(1, 4)), "3/4")

    def test_sub(self):
        self.assertEqual(str(Fraction(1, 2) - Fraction(1, 4)), "1/4")

    def test_mul(self):
        self.assertEqual(str(Fraction(1, 2) * Fraction(1, 4)), "1/8")

    def test_div(self):
        self.assertEqual(str(Fraction(3, 4) / Fraction(1, 2)), "3/2")

    def test_add_int(self):
        self.assertEqual(str(Fraction(1, 2) + 2), "5/2")

    def test_sub_int(self):
        self.assertEqual(str(Fraction(1, 2) - 2), "-3/2")

    def test_mul_int(self):
        self.assertEqual(str(Fraction(1, 2) * 2), "1/1")

    def test_div_int(self):
        self.assertEqual(str(Fraction(1, 2) / 2), "1/4")

    def test_radd_int(self):
        self.assertEqual(str(2 + Fraction(1, 2)), "5/2")

    def test_rsub_int(self):
        self.assertEqual(str(2 - Fraction(1, 2)), "3/2")

    def test_rmul_int(self):
        self.assertEqual(str(2 * Fraction(1, 2)), "1/1")

    def test_rtruediv_int(self):
        self.assertEqual(str(2 / Fraction(1, 2)), "4/1")

    def test_harmonic_series(self):
        series = list(Fraction.harmonic_series(3))
        self.assertEqual(str(series[0]), "1/1")
        self.assertEqual(str(series[1]), "1/2")
        self.assertEqual(str(series[2]), "1/3")


class TestCalculator(unittest.TestCase):
    def test_parse_add(self):
        k = Calculator()
        self.assertEqual(str(k.parse_and_compute("1/2 + 1/2")), "1/1")
        self.assertEqual(str(k.parse_and_compute("4 + 1/4")), "17/4")

    def test_parse_sub_rsub(self):
        k = Calculator()
        self.assertEqual(str(k.parse_and_compute("1/16 - 1/4")), "-3/16")
        self.assertEqual(str(k.parse_and_compute("4 - 1/4")), "15/4")

    def test_parse_mul(self):
        k = Calculator()
        self.assertEqual(str(k.parse_and_compute("1/16 * 1/4")), "1/64")

    def test_parse_div(self):
        k = Calculator()
        self.assertEqual(str(k.parse_and_compute("3/4 : 1/2")), "3/2")

    def test_parse_error_zero_denominator(self):
        k = Calculator()
        with self.assertRaises(ZeroDivisionError):
            k.parse_and_compute("1/0 + 1/4")

    def test_parse_invalid_format(self):
        k = Calculator()
        with self.assertRaises(ValueError):
            k.parse_and_compute("1/2 +")

    def test_harmonic_sum(self):
        k = Calculator()
        result = k.parse_and_compute("szereg 4")
        self.assertEqual(result.numerator, 25)
        self.assertEqual(result.denominator, 12)

    def test_history_empty_at_start(self):
        k = Calculator()
        self.assertEqual(k.history, [])

    def test_err_history_empty_at_start(self):
        k = Calculator()
        self.assertEqual(k.err_history, [])

    def test_add_to_history(self):
        k = Calculator()
        f = Fraction(1, 2)
        k.add_to_history(f)
        self.assertEqual(len(k.history), 1)
        self.assertEqual(str(k.history[0]), "1/2")

    def test_add_error(self):
        k = Calculator()
        k.add_error("test error")
        self.assertEqual(k.err_history[0], "test error")

    def test_unknown_operator_raises(self):
        k = Calculator()
        with self.assertRaises(NotImplementedError):
            k.parse_and_compute("1/2 ^ 1/4")

    def test_parse_float_fractions(self):
        k = Calculator()
        self.assertEqual(str(k.parse_and_compute("0.5 + 0.25")), "3/4")

    def test_parse_integer_operands(self):
        k = Calculator()
        self.assertEqual(str(k.parse_and_compute("2 * 3")), "6/1")

    def test_harmonic_sum_1(self):
        k = Calculator()
        result = k.parse_and_compute("szereg 1")
        self.assertEqual(result.numerator, 1)
        self.assertEqual(result.denominator, 1)

    def test_parse_div_by_zero_raises(self):
        k = Calculator()
        with self.assertRaises(ZeroDivisionError):
            k.parse_and_compute("1/2 : 0")

    def test_parse_empty_string_raises(self):
        k = Calculator()
        with self.assertRaises(ValueError):
            k.parse_and_compute("")


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.filename = "test_tmp.txt"

    def tearDown(self):
        for name in [self.filename, "err_" + self.filename]:
            if os.path.exists(name):
                os.remove(name)

    def test_save_and_load(self):
        with open(self.filename, "w") as f:
            f.write("1/4 + 1/4\n")
            f.write("1/2 + 1/4\n")

        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(len(k.history), 2)
        self.assertEqual(str(k.history[0]), "1/2")
        self.assertEqual(str(k.history[1]), "3/4")

    def test_save_creates_error_file(self):
        k = Calculator()
        k.add_error("jakis blad")
        FileManager.save_to_file(k, self.filename)
        self.assertTrue(os.path.exists("err_" + self.filename))

    def test_load_invalid_line_goes_to_err_history(self):
        with open(self.filename, "w") as f:
            f.write("to nie jest ulamek\n")
        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(len(k.err_history), 1)

    def test_load_empty_file(self):
        with open(self.filename, "w") as f:
            f.write("")
        k = Calculator()
        FileManager.load_from_file(k, self.filename)
        self.assertEqual(len(k.history), 0)

    def test_save_empty_history(self):
        k = Calculator()
        FileManager.save_to_file(k, self.filename)
        self.assertTrue(os.path.exists(self.filename))

if __name__ == "__main__":
    unittest.main()