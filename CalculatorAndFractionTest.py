import unittest
import os
from Fraction import Fraction
from Calculator import Calculator


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

    def test_save_and_load_file(self):
        filename = "test_output.txt"
        with open(filename, "w") as f:
            f.write("1/2 + 1/4\n")
            f.write("szereg 4\n")

        k = Calculator()
        k.load_from_file(filename)

        self.assertEqual(str(k.history[0]), "3/4")
        self.assertEqual(str(k.history[1]), "25/12")

        save_filename = "test_save.txt"
        k.save_to_file(save_filename)
        self.assertTrue(os.path.exists(save_filename))

        os.remove(filename)
        os.remove(save_filename)

    def test_load_file_with_error_line(self):
        filename = "test_errors.txt"
        with open(filename, "w") as f:
            f.write("ala ma kota\n")
            f.write("1/2 + 1/4\n")

        k = Calculator()
        k.load_from_file(filename)
        self.assertEqual(k.history[0], "BLAD")
        self.assertEqual(str(k.history[1]), "3/4")
        os.remove(filename)


if __name__ == "__main__":
    unittest.main()