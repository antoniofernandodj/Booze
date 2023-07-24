import re
from abc import ABC, abstractmethod
from booze.errors import *
from booze.helpers import check_numeric
from contextlib import suppress
import datetime
with suppress(ImportError):
    from booze.coercer import Coerce

from typing import Optional
import datetime
import re


class Validator:
    """
    Base class for Validators. Subclasses of Validator are registered in the Coercer class and are called
    via the method `__call__(self, value)` to validate a value according to specific validation rules.
    If the value does not pass the validation, a negative value is returned so that the Coercer class
    raises a ParsingError during the analysis process.
    """

    def __str__(self):
        """
        Return a string representation of the Validator object.

        Returns:
            str (str): A string representation of the Validator.
        """
        return f'<Validator: {type(self).__name__}, args:({self.__dict__})>'


class Integer(Validator):
    """
    A Validator class for validating integer values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is successfully converted to an integer, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        try:
            self.coercer.value = int(value)
            return True
        except (TypeError, ValueError):
            return False


class Float(Validator):
    """
    A Validator class for validating float values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is successfully converted to a float, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        try:
            self.coercer.value = float(value)
            return True
        except (TypeError, ValueError):
            return False


class Date(Validator):
    """
    A Validator class for validating date values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is successfully validated as a date, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        from booze.consts import date_formats
        self.coercer = coercer
        self.handler = date_formats

    def __call__(self, value: any) -> bool:
        if isinstance(value, datetime.date):
            return True

        try:
            if isinstance(value, str):
                datetime.datetime.strptime(value, "%Y-%m-%d")
                return True
        except:
            pass

        try:
            if isinstance(value, str):
                datetime.datetime.strptime(value, "%d-%m-%Y")
                return True
        except:
            pass

        try:
            if isinstance(value, str):
                result = value.split('/')
                if len(result) == 3:
                    f, s, t = result
                    if len(f) <= 4 and len(s) <= 4 and len(t) <= 4:
                        return True
        except:
            pass

        try:
            if isinstance(value, (int, float)):
                datetime.date.fromtimestamp(value)
                return True
        except:
            pass

        return False


class DateTime(Validator):
    """
    A Validator class for validating datetime values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is successfully validated as a datetime, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        from booze.consts import date_formats
        self.coercer = coercer
        self.handler = date_formats

    def __call__(self, value: any) -> bool:
        if isinstance(value, datetime.datetime):
            return True

        try:
            if isinstance(value, str):
                for fmt in self.handler.values():
                    datetime.datetime.strptime(value, fmt)
                    return True
        except:
            pass

        try:
            if isinstance(value, (int, float)):
                datetime.datetime.fromtimestamp(value)
                return True
        except:
            pass

        return False


class FormatDate(Validator):
    """
    A Validator class for validating date values with a specific format.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        format_string (str): The format string for the date.

    Returns:
        bool (bool): True if the value is successfully validated as a date with the specified format, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', format_string: str):
        from booze.consts import date_formats
        self.coercer = coercer
        self.format_string = format_string
        self.handler = date_formats

    def __call__(self, value: any) -> bool:
        if isinstance(value, datetime.date):
            self.coercer.value = value.strftime(self.format_string)
            return True
        try:
            if isinstance(value, str):
                format = self.handler[self.format_string]
                date_obj = datetime.datetime.strptime(value, format).date()
                self.coercer.value = date_obj
                return True
        except (TypeError, ValueError):
            pass

        try:
            if isinstance(value, (int, float)):
                # Consider numeric values as timestamps and try to convert them to date
                date_obj = datetime.date.fromtimestamp(value)
                self.coercer.value = date_obj
                return True
        except (TypeError, ValueError):
            pass

        return False


class Boolean(Validator):
    """
    A Validator class for validating boolean values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is successfully validated as a boolean, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        if self.coercer.value is None:
            return False
        if isinstance(value, bool):
            return True
        elif value == 1:
            self.coercer.value = True
            return True
        elif value == 0:
            self.coercer.value = False
            return True
        if value == "True":
            self.coercer.value = True
            return True
        if value == "False":
            self.coercer.value = False
            return True
        return False


class String(Validator):
    """
    A Validator class for validating string values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is successfully converted to a string, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        self.coercer.value = str(value)
        return isinstance(value, str)


class Strict(Validator):
    """
    A Validator class for strict value checking.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is strictly equal to the expected value, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        return self.coercer.value == value


class List(Validator):
    """
    A Validator class for validating list values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is a list, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        return isinstance(value, list)


class Dictionary(Validator):
    """
    A Validator class for validating dictionary values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        required_keys (Optional[list]): A list of required keys in the dictionary.
        optional_keys (Optional[list]): A list of optional keys in the dictionary.

    Returns:
        bool (bool): True if the value is a dictionary with all the required keys present, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', required_keys: Optional[list], optional_keys: Optional[list]):
        self.coercer = coercer
        self.required_keys = required_keys
        self.optional_keys = optional_keys

    def __call__(self, value: any) -> bool:
        if not isinstance(value, dict):
            return False
        items = []
        if self.required_keys and isinstance(self.required_keys, list):
            for key in self.required_keys:
                item = value.get(key)
                items.append(item)
        if None in items:
            return False

        return True


class RequiredKeys(Validator):
    """
    A Validator class for validating the presence of required keys in a dictionary.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        required_keys (list): A list of required keys in the dictionary.

    Returns:
        bool (bool): True if all the required keys are present in the dictionary, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', required_keys: list):
        self.coercer = coercer
        self.required_keys = required_keys

    def __call__(self, value: any) -> bool:
        if not isinstance(value, dict):
            return False
        items = []
        if isinstance(self.required_keys, list):
            for key in self.required_keys:
                item = value.get(key)
                items.append(item)
        else:
            return False
        if None in items:
            return False

        return True


class Min(Validator):
    """
    A Validator class for validating numeric values with a minimum value.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        value (float or int): The minimum value allowed.

    Returns:
        bool (bool): True if the value is greater than or equal to the minimum value, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', value: float or int):
        self.coercer = coercer
        self.min = value

    def __call__(self, value: any) -> bool:
        try:
            if self.min is None:
                return False

            if not check_numeric(value):
                return False

            if float(self.min) < float(value):
                return True
            else:
                return False

        except (TypeError, ValueError) as e:
            return False


class Max(Validator):
    """
    A Validator class for validating numeric values with a maximum value.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        value (float or int): The maximum value allowed.

    Returns:
        bool (bool): True if the value is less than or equal to the maximum value, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', value: float or int):
        self.coercer = coercer
        self.max = value

    def __call__(self, value: any) -> bool:
        try:
            if not check_numeric(value):
                return False
            if float(value) > float(self.max):
                return False
            else:
                return True
        except (TypeError, ValueError):
            return False


class Length(Validator):
    """
    A Validator class for validating the length of a value.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        length_min (int): The minimum length allowed.
        length_max (int): The maximum length allowed.

    Returns:
        bool (bool): True if the length of the value is within the specified range, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', length_min: int, length_max: int):
        self.coercer = coercer
        self.length_min = length_min
        self.length_max = length_max

    def __call__(self, value: any) -> bool:
        test = self.length_min <= len(value) <= self.length_max
        return test


class MinLength(Validator):
    """
    A Validator class for validating the minimum length of a value.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        length_min (int): The minimum length allowed.

    Returns:
        bool (bool): True if the length of the value is greater than or equal to the minimum length, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', length_min: int):
        self.coercer = coercer
        self.length_min = length_min

    def __call__(self, value: any) -> bool:
        test = self.length_min <= len(value)
        return test


class MaxLength(Validator):
    """
    A Validator class for validating the maximum length of a value.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        length_max (int): The maximum length allowed.

    Returns:
        bool (bool): True if the length of the value is less than or equal to the maximum length, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', length_max: int):
        self.coercer = coercer
        self.length_max = length_max

    def __call__(self, value: any) -> bool:
        test = len(value) <= self.length_max
        return test


class Contains(Validator):
    """
    A Validator class for validating the presence of a value in a list.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.
        value: The value to be checked for existence in the list.

    Returns:
        bool (bool): True if the value is found in the list, False otherwise.
    """

    def __init__(self, coercer: 'Coerce', value: any):
        self.coercer = coercer
        self.value = value

    def __call__(self, value: any) -> bool:
        return self.value in value


class Email(Validator):
    """
    A Validator class for validating email addresses.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is a valid email address, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, value) is not None


class Lowercase(Validator):
    """
    A Validator class for converting a value to lowercase.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is successfully converted to lowercase, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        try:
            self.coercer.value = value.lower()
            return True
        except:
            return False


class Numeric(Validator):
    """
    A Validator class for validating numeric values.

    Args:
        coercer (Coerce): The Coerce object to store the coerced value.

    Returns:
        bool (bool): True if the value is numeric, False otherwise.
    """

    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value: any) -> bool:
        return check_numeric(value)
