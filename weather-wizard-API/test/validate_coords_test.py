from unittest import TestCase, main
from validation import Validator


class TestValidateCoords(TestCase):

    def test_valid(self):
        self.assertEqual(Validator.validate_coords("54.3245", "30.5232"), (54.3245, 30.5232))

    def test_none_lat(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords(None, "34.123")
        self.assertEqual(str(e.exception.args[0]), "Please enter 'lat' and 'lon' arguments")

    def test_none_lon(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords(None, "34.123")
        self.assertEqual(str(e.exception.args[0]), "Please enter 'lat' and 'lon' arguments")

    def test_too_long_lat(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords("56.1234567", "34.123")
        self.assertEqual(str(e.exception.args[0]), "Invalid coordinates provided")

    def test_too_long_lon(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords("56.123", "56.1234567")
        self.assertEqual(str(e.exception.args[0]), "Invalid coordinates provided")

    def test_wrong_lat(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords("91", "34.123")
        self.assertEqual(str(e.exception.args[0]), "Invalid coordinates provided")

    def test_wrong_lat_2(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords("-100", "34.123")
        self.assertEqual(str(e.exception.args[0]), "Invalid coordinates provided")

    def test_wrong_lon(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords("50.41", "181")
        self.assertEqual(str(e.exception.args[0]), "Invalid coordinates provided")

    def test_wrong_lon_2(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords("50.41", "-200")
        self.assertEqual(str(e.exception.args[0]), "Invalid coordinates provided")

    def test_invalid_str_lat(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords("aaa", "56")
        self.assertEqual(str(e.exception.args[0]), "Invalid coordinates provided")

    def test_invalid_str_lon(self):
        with self.assertRaises(ValueError) as e:
            Validator.validate_coords("34", "3t")
        self.assertEqual(str(e.exception.args[0]), "Invalid coordinates provided")



if __name__ == '__main__':
    main()
