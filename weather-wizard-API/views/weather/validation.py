import re
from config import MIN_DAYS_FORECAST, MAX_DAYS_FORECAST


class Validator:
    @classmethod
    def validate_coords(cls, lat, lon):
        if lat is None or lon is None:
            raise ValueError("Please enter 'lat' and 'lon' arguments")

        if cls.__is_valid_lat(lat) and cls.__is_valid_lon(lon):
            return float(lat), float(lon)
        else:
            raise ValueError("Invalid coordinates provided")

    @staticmethod
    def __is_valid_lat(lat):
        pattern = r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$'
        return bool(re.match(pattern, lat))

    @staticmethod
    def __is_valid_lon(lon):
        pattern = r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$'
        return bool(re.match(pattern, lon))

    @classmethod
    def validate_days(cls, days):
        if days is None:
            return MAX_DAYS_FORECAST
        else:
            try:
                number = int(days)
                if MIN_DAYS_FORECAST <= number <= MAX_DAYS_FORECAST:
                    return number
                else:
                    raise ValueError
            except ValueError:
                raise ValueError("Invalid value for 'days' argument")
