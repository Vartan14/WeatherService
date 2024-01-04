from unittest import TestCase, main
from views.weather.validation import Validator


class TestValidator(TestCase):

    def test_valid(self):
        self.assertEqual(Validator.validate_days("5"), 5)

    def test_min(self):
        self.assertEqual(Validator.validate_days("1"), 1)

    def test_max(self):
        self.assertEqual(Validator.validate_days("7"), 7)

    def test_min_border(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_days("0")

        self.assertEqual(str(e.exception.args[0]), "Invalid value for 'days' argument")

    def test_max_border(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_days("8")

        self.assertEqual(str(e.exception.args[0]), "Invalid value for 'days' argument")

    def test_none(self):
        self.assertEqual(Validator.validate_days(None), 7)

    def test_out_of_range(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_days("10")

        self.assertEqual(str(e.exception.args[0]), "Invalid value for 'days' argument")

    def test_out_of_range2(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_days("-1")

        self.assertEqual(str(e.exception.args[0]), "Invalid value for 'days' argument")

    def test_not_a_number(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_days("qqq")

        self.assertEqual(str(e.exception.args[0]), "Invalid value for 'days' argument")

    def test_empty_str(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_days("")

        self.assertEqual(str(e.exception.args[0]), "Invalid value for 'days' argument")


if __name__ == '__main__':
    main()
