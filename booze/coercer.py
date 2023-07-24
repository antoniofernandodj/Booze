from booze.errors import *
import re
from booze import validators
import typing as t
import uuid


class Coerce:
    """
    The Coerce class provides a set of validation methods to parse and validate data types.
    Call `parse(value)` after setting the validation rules to parse the value. If the value
    passes all validations, the parsed value is returned; otherwise, a ParsingError is raised.

    Attributes:
        name (str): A unique name for the Coerce instance (default is a UUID4 string).
        value (Any): The current value being parsed and validated.
        first_value (Any): The initial value provided before parsing and validation.
        validations (List[Validator]): A list to store validation rules.

    Example:
        # Create a Coerce instance and set validation rules
        coercer = Coerce().integer().min(10).max(100)

        # Parse and validate a value
        parsed_value = coercer.parse("50")
        print(parsed_value)  # Output: 50

    """
    def __init__(self, name:str=str(uuid.uuid4())) -> None:
        from booze.validators import Validator
        self.name = name
        self.value = None
        self.first_value = None
        self.validations: t.List[Validator] = []

    def __repr__(self):
        if self.value:
            return f"Coerce(name='{self.name}', value={self.value})"
        return f"Coerce(name='{self.name})"

    def __str__(self):
        if self.value:
            return f"Coerce({self.name}={self.value})"
        return f"Coerce({self.name})"

    def integer(self) -> 'Coerce':
        """
        Add an Integer validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Integer(coercer=self)
        self.validations.append(validator)
        return self
    
    def date(self) -> 'Coerce':
        """
        Add a Date validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Date(coercer=self)
        self.validations.append(validator)
        return self
    
    def datetime(self) -> 'Coerce':
        """
        Parse and validate the given value based on the registered validation rules.

        Args:
            value (Any): The value to be parsed and validated.

        Returns:
            Any: The parsed and validated value.

        Raises:
            ParsingError: If the value fails validation according to any registered validator.
        """
        validator = validators.DateTime(coercer=self)
        self.validations.append(validator)
        return self
    
    def strict(self) -> 'Coerce':
        """
        Add a Strict validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Strict(coercer=self)
        self.validations.append(validator)
        return self
    
    def format_date(self, format_string) -> 'Coerce':
        """
        Add a FormatDate validator to the Coerce instance.

        Args:
            format_string (str): The format string to validate date format.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.FormatDate( coercer=self, format_string=format_string)
        
        self.validations.append(validator)
        return self

    def float(self) -> 'Coerce':
        """
        Add a Float validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Float(coercer=self)
        self.validations.append(validator)
        return self

    def boolean(self) -> 'Coerce':
        """
        Add a Boolean validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Boolean(coercer=self)
        self.validations.append(validator)
        return self

    def string(self) -> 'Coerce':
        """
        Add a String validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.String(coercer=self)
        self.validations.append(validator)
        return self

    def list(self) -> 'Coerce':
        """
        Add a List validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.List(coercer=self)
        self.validations.append(validator)
        return self

    def dictionary(
            self, required_keys: t.Optional[t.List[str]]=None,
            optional_keys: t.Optional[t.List[str]]=None
        ) -> 'Coerce':
        """
        Add a Dictionary validator to the Coerce instance.

        Args:
            required_keys (Optional[List[str]]): A list of required keys in the dictionary (default is None).
            optional_keys (Optional[List[str]]): A list of optional keys in the dictionary (default is None).

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Dictionary(
            coercer=self,
            required_keys=required_keys,
            optional_keys=optional_keys
        )
        self.validations.append(validator)
        return self

    def required_keys(self, required_keys: t.Optional[t.List[str]]=None) -> 'Coerce':
        """
        Add a RequiredKeys validator to the Coerce instance.

        Args:
            required_keys (List[str]): A list of required keys in the dictionary.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.RequiredKeys(coercer=self, required_keys=required_keys)
        self.validations.append(validator)
        return self

    def dict(
            self,
            required_keys: t.Optional[t.List[str]]=None,
            optional_keys: t.Optional[t.List[str]]=None
        ) -> 'Coerce':
        """
        Add a Dictionary validator to the Coerce instance.

        Args:
            required_keys (Optional[List[str]]): A list of required keys in the dictionary (default is None).
            optional_keys (Optional[List[str]]): A list of optional keys in the dictionary (default is None).

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Dictionary(
            coercer=self,
            required_keys=required_keys,
            optional_keys=optional_keys
        )
        self.validations.append(validator)
        return self
    
    def numeric(self) -> 'Coerce':
        """
        Add a Numeric validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Numeric(coercer=self)
        self.validations.append(validator)
        return self

    def min(self, minimum: int) -> 'Coerce':
        """
        Add a Min validator to the Coerce instance.

        Args:
            minimum (int): The minimum value allowed.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Min(coercer=self, value=minimum)
        self.validations.append(validator)
        return self

    def max(self, maximum: int) -> 'Coerce':
        """
        Add a Max validator to the Coerce instance.

        Args:
            maximum (int): The maximum value allowed.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Max(coercer=self, value=maximum)
        self.validations.append(validator)
        return self
    
    def min_length(self, min: int) -> 'Coerce':
        """
        Add a MinLength validator to the Coerce instance.

        Args:
            min (int): The minimum length allowed.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.MinLength(coercer=self, length_min=min)
        self.validations.append(validator)
        return self
    
    def max_length(self, maximum: int) -> 'Coerce':
        """
        Add a MaxLength validator to the Coerce instance.

        Args:
            maximum (int): The maximum length allowed.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.MaxLength(coercer=self, length_max=maximum)
        self.validations.append(validator)
        return self

    def length(self, *args) -> 'Coerce':
        """
        Add a Length validator to the Coerce instance.

        Args:
            *args (Union[int, Tuple[int, int]]): Accepts either one or two parameters.
                If one parameter is provided, it's considered as the maximum length.
                If two parameters are provided, they are considered as (minimum, maximum) lengths.

        Returns:
            Coerce: The updated Coerce instance.

        Raises:
            ValueError: If the `length` validator is provided with an invalid number of parameters.
        """
        if len(args) == 1:
            length_min = 0
            length_max = args[0]
        elif len(args) == 2:
            length_min = args[0]
            length_max = args[1]
        else:
            raise ValueError('The `length` validator only accepts 1 or 2 parameters.')
        
        validator = validators.Length(coercer=self, length_min=length_min, length_max=length_max)
        self.validations.append(validator)
        return self

    def contains(self, element: any) -> 'Coerce':
        """
        Add a Contains validator to the Coerce instance.

        Args:
            element (Any): The element that the value must contain.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Contains(coercer=self, value=element)
        self.validations.append(validator)
        return self

    def email(self) -> 'Coerce':
        """
        Add an Email validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Email(coercer=self)
        self.validations.append(validator)
        return self
    
    def lowercase(self) -> 'Coerce':
        """
        Add a Lowercase validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Lowercase(coercer=self)
        self.validations.append(validator)
        return self

    def parse(self, value: t.Any) -> 'Coerce':
        """
        Parse and validate the given value based on the registered validation rules.

        Args:
            value (Any): The value to be parsed and validated.

        Returns:
            Any: The parsed and validated value.

        Raises:
            ParsingError: If the value fails validation according to any registered validator.
        """
        self.value = value
        self.first_value = value
        for validation in self.validations:
            result = validation(value)
            self.value = validation.coercer.value
            if result == False:
                raise ParsingError(
                    f'Error in validating data for value {value}',
                    f'validator: {type(validation).__name__}',
                    f'Coercer {self}'
                )
                
        return self.value
