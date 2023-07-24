from booze import Coerce, ParsingError
import pytest
import datetime
from datetime import date


def test_integer_validation():
    coerce = Coerce('integer').integer()
    assert coerce.parse(42) == 42
    assert coerce.parse("42") == 42

    with pytest.raises(ParsingError):
        coerce.parse("not_an_integer")


def test_float_validation():
    coerce = Coerce('float').float()

    assert coerce.parse(3.14) == 3.14
    assert coerce.parse("3.14") == 3.14

    with pytest.raises(ParsingError):
        coerce.parse("not_a_float")


def test_boolean_validation():
    coerce = Coerce('boolean').boolean()

    assert coerce.parse(True) is True
    assert coerce.parse(1) is True
    assert coerce.parse(False) is False
    assert coerce.parse(0) is False

    with pytest.raises(ParsingError):
        coerce.parse("not_a_boolean")

def test_string_validation():
    coerce = Coerce().string()
    
    assert coerce.parse("Hello, World!") == "Hello, World!"
    with pytest.raises(ParsingError):
        coerce.parse(42)

def test_list_validation():
    coerce = Coerce().list()

    assert coerce.parse([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ParsingError):
        coerce.parse("not_a_list")

def test_dictionary_validation():
    coerce = Coerce().dictionary()
    
    assert coerce.parse({"key": "value", "number": 42}) == {"key": "value", "number": 42}

    with pytest.raises(ParsingError):
        coerce.parse("not_a_dict")

def test_min_validation():
    coerce = Coerce().integer().min(5)
    
    assert coerce.parse(10) == 10

    with pytest.raises(ParsingError):
        coerce.parse(3)

def test_max_validation():
    coerce = Coerce().float().max(10.0)
    
    assert coerce.parse(5.5) == 5.5

    with pytest.raises(ParsingError):
        coerce.parse(15.0)

def test_length_validation():
    coerce = Coerce().string().length(5)
    
    assert coerce.parse("hello") == "hello"

    with pytest.raises(ParsingError):
        coerce.parse("hello world")

def test_contains_validation():
    coerce = Coerce().list().contains(42)
    
    assert coerce.parse([1, 2, 42, 3]) == [1, 2, 42, 3]

    with pytest.raises(ParsingError):
        coerce.parse([1, 2, 3])

def test_email_validation():
    coerce = Coerce()
    coerce.email()
    assert coerce.parse("test@example.com") == "test@example.com"

    with pytest.raises(ParsingError):
        coerce.parse("invalid_email")

def test_numeric_validation_1():
    coerce = Coerce().numeric().float()
    
    assert coerce.parse('3.14') == 3.14

    with pytest.raises(ParsingError):
        coerce.parse("not_a_numeric_value")


def test_numeric_validation_2():
    coerce = Coerce().numeric().integer()
    
    assert coerce.parse('3') == 3

    with pytest.raises(ParsingError):
        coerce.parse("not_a_numeric_value")
        

def test_numeric_validation_3():
    coerce = Coerce().numeric().integer().max(10).min(1)
    
    assert coerce.parse('5') == 5

    with pytest.raises(ParsingError):
        coerce.parse("not_a_numeric_value")
        
        
def test_numeric_validation_4():
    coerce = Coerce().numeric().max(10).min(1).integer()
    
    assert coerce.parse(3.14) == 3

    with pytest.raises(ParsingError):
        coerce.parse("not_a_numeric_value")
        
        
def test_numeric_validation_5():
    coerce = Coerce().float().numeric()
    
    assert coerce.parse('3.14') == 3.14

    with pytest.raises(ParsingError):
        coerce.parse("not_a_numeric_value")
        

def test_date_validation_1():
    coerce = Coerce().date().format_date("YYYY-MM-DD")
    
    assert coerce.parse('2023-07-23') == datetime.date(2023, 7, 23)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_date")


def test_date_validation_2():
    coerce = Coerce().date().format_date("MM/DD/YYYY")
    
    value = coerce.parse('07/23/2023')
    assert value == datetime.date(2023, 7, 23)
    with pytest.raises(ParsingError):
        coerce.parse("not_a_date")
        

def test_date_validation_3():
    coerce = Coerce().date().format_date("DD-MM-YYYY")
    
    assert coerce.parse('23-07-2023') == datetime.date(2023, 7, 23)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_date")

        
def test_bool_validation_2():
    coerce = Coerce().boolean()
    assert coerce.parse('True') is True
    assert coerce.parse('False') is False


def test_bool_validation_3():
    coerce = Coerce().boolean().strict()

    with pytest.raises(ParsingError):
        coerce.parse("True")

        
def test_email_validation_1():
    coerce = Coerce().email()
    
    assert coerce.parse('test@example.com') == 'test@example.com'

    with pytest.raises(ParsingError):
        coerce.parse("not_an_email")
        
        
def test_email_validation_2():
    coerce = Coerce().email().lowercase()
    result1 = coerce.parse('Test@Example.com')
    assert result1 == 'test@example.com'
    
    result2 = coerce.parse('another.EMAIL@EXAMPLE.com')
    assert result2 == 'another.email@example.com'

        
# Add more test functions for other validation rules as needed...

# Example of a test case for an unknown validation rule
def test_unknown_validation_rule():
    coerce = Coerce()
    with pytest.raises(AttributeError):
        coerce.unknown_rule()


def test_list_validation_1():
    coerce = Coerce().list()
    
    assert coerce.parse([1, 2, 3]) == [1, 2, 3]
    assert coerce.parse((4, 5, 6)) == [4, 5, 6]  # Expecting a list, converting tuple to list
    
    with pytest.raises(ParsingError):
        coerce.parse("Not a list")


def test_list_validation_2():
    coerce = Coerce().list().min_length(3)
    
    assert coerce.parse([1, 2, 3]) == [1, 2, 3]
    
    with pytest.raises(ParsingError):
        coerce.parse([1, 2])  # Minimum length requirement not met


def test_list_validation_3():
    coerce = Coerce().list().max_length(5)
    
    assert coerce.parse([1, 2, 3]) == [1, 2, 3]
    
    with pytest.raises(ParsingError):
        coerce.parse([1, 2, 3, 4, 5, 6])  # Maximum length exceeded


def test_dict_validation_1():
    coerce = Coerce().dict()
    
    assert coerce.parse({"name": "John", "age": 30}) == {"name": "John", "age": 30}
    
    with pytest.raises(ParsingError):
        coerce.parse("Not a dictionary")


def test_dict_validation_2():
    coerce = Coerce().dict().required_keys(["name", "age"])
    
    assert coerce.parse({"name": "John", "age": 30}) == {"name": "John", "age": 30}
    
    with pytest.raises(ParsingError):
        coerce.parse({"name": "Alice"})  # Missing required "age" key


def test_dict_validation_3():
    coerce = Coerce().dict().optional_keys("email", "address")
    
    assert coerce.parse({"name": "John", "age": 30}) == {"name": "John", "age": 30}
    assert coerce.parse({"name": "Alice", "age": 25, "email": "alice@example.com"}) == {"name": "Alice", "age": 25, "email": "alice@example.com"}
    
    with pytest.raises(ParsingError):
        coerce.parse({"name": "Bob", "age": 40, "phone": "1234567890"})  # "phone" key is not allowed
        
def test_date_validation_11():
    coerce = Coerce().date()
    
    assert coerce.parse('2023-07-23') == date(2023, 7, 23)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_date_value")


def test_date_validation_12():
    coerce = Coerce().date(format="%m/%d/%Y")
    
    assert coerce.parse('07/23/2023') == date(2023, 7, 23)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_date_value")

def test_date_validation_13():
    coerce = Coerce().date(format="%d.%m.%Y")
    
    assert coerce.parse('23.07.2023') == date(2023, 7, 23)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_date_value")

def test_date_validation_14():
    coerce = Coerce().date(separator='.', year_format='YY')
    
    assert coerce.parse('23.07.23') == date(2023, 7, 23)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_date_value")


def test_date_validation_15():
    coerce = Coerce().date(separator='/', year_format='YYYY')
    
    assert coerce.parse('07/23/2023') == date(2023, 7, 23)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_date_value")


def test_date_validation_16():
    coerce = Coerce().date(separator='-', year_format='YY')
    
    assert coerce.parse('23-07-23') == date(2023, 7, 23)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_date_value")


def test_datetime_validation_17():
    coerce = Coerce().datetime()
    
    assert coerce.parse('2023-07-23 12:34:56') == datetime(2023, 7, 23, 12, 34, 56)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")


def test_datetime_validation_18():
    coerce = Coerce().datetime(format="%m/%d/%Y %H:%M")
    
    assert coerce.parse('07/23/2023 12:34') == datetime(2023, 7, 23, 12, 34)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")


def test_datetime_validation_19():
    coerce = Coerce().datetime(format="%d.%m.%Y %H:%M")
    
    assert coerce.parse('23.07.2023 12:34') == datetime(2023, 7, 23, 12, 34)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")


def test_datetime_validation_20():
    coerce = Coerce().datetime(separator=' / ')
    
    assert coerce.parse('2023-07-23 / 12:34:56') == datetime(2023, 7, 23, 12, 34, 56)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")


def test_datetime_validation_21():
    coerce = Coerce().datetime(separator=' @ ')
    
    assert coerce.parse('2023-07-23 @ 12:34:56') == datetime(2023, 7, 23, 12, 34, 56)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")


def test_datetime_validation_22():
    coerce = Coerce().datetime(separator='/', time_format='12h')
    
    assert coerce.parse('2023-07-23/12:34:56 PM') == datetime(2023, 7, 23, 12, 34, 56)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")


def test_datetime_validation_23():
    coerce = Coerce().datetime(separator='-', time_format='12h')
    
    assert coerce.parse('2023-07-23-12:34:56 PM') == datetime(2023, 7, 23, 12, 34, 56)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")


def test_datetime_validation_24():
    coerce = Coerce().datetime(separator='/', time_format='12h', include_seconds=False)
    
    assert coerce.parse('2023-07-23/12:34 PM') == datetime(2023, 7, 23, 12, 34)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")


def test_datetime_validation_25():
    coerce = Coerce().datetime(separator='-', time_format='12h', include_seconds=False)
    
    assert coerce.parse('2023-07-23-12:34 PM') == datetime(2023, 7, 23, 12, 34)

    with pytest.raises(ParsingError):
        coerce.parse("not_a_datetime_value")
