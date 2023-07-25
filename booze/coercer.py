from __future__ import annotations
from booze.errors import *
import re
from booze import validators
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
        validations (list[Validator]): A list to store validation rules.

    Example:
        # Create a Coerce instance and set validation rules
        coercer = Coerce().integer().min(10).max(100)

        # Parse and validate a value
        parsed_value = coercer.parse("50")
        print(parsed_value)  # Output: 50

    """
    def __init__(self, name:str=None, message:Optional[str]=None) -> None:
        from booze.validators import Validator
        self.name = name
        self.value = None
        self.first_value = None
        self.message = message
        self.validations: list[Validator] = []

    def __repr__(self):
        if self.value:
            return f"Coerce(name='{self.name}', value={self.value})"
        return f"Coerce(name='{self.name})"

    def __str__(self):
        if self.value:
            return f"Coerce({self.name}={self.value})"
        return f"Coerce({self.name})"

    def integer(self, message: Optional[str]=None) -> 'Coerce':
        """
        Add an Integer validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Integer(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self
    
    def date(self, message: Optional[str]=None) -> 'Coerce':
        """
        Add a Date validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Date(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self
    
    def datetime(self, message: Optional[str]=None) -> 'Coerce':
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
        if message:
            validator.message = message
        self.validations.append(validator)
        return self
    
    def strict(self, message: Optional[str]=None) -> 'Coerce':
        """
        Add a Strict validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Strict(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self
    
    def format_date(self, format_string, message: Optional[str]=None) -> 'Coerce':
        """
        Add a FormatDate validator to the Coerce instance.

        Args:
            format_string (str): The format string to validate date format.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.FormatDate( coercer=self, format_string=format_string)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def float(self, message: Optional[str]=None) -> 'Coerce':
        """
        Add a Float validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Float(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def boolean(self, message: Optional[str]=None) -> 'Coerce':
        """
        Add a Boolean validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Boolean(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def string(self, message: Optional[str]=None) -> 'Coerce':
        """
        Add a String validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.String(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def list(self, message: Optional[str]=None) -> 'Coerce':
        """
        Add a List validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.List(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def dictionary(
            self, required_keys: Optional[list[str]]=None,
            optional_keys: Optional[list[str]]=None,
            message: Optional[str]=None
        ) -> 'Coerce':
        """
        Add a Dictionary validator to the Coerce instance.

        Args:
            required_keys (Optional[list[str]]): A list of required keys in the dictionary (default is None).
            optional_keys (Optional[list[str]]): A list of optional keys in the dictionary (default is None).

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Dictionary(
            coercer=self,
            required_keys=required_keys,
            optional_keys=optional_keys
        )
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def required_keys(
            self,
            required_keys: Optional[list[str]]=None,
            message:Optional[str]=None) -> 'Coerce':
        """
        Add a RequiredKeys validator to the Coerce instance.

        Args:
            required_keys (list[str]): A list of required keys in the dictionary.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.RequiredKeys(coercer=self, required_keys=required_keys)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def dict(
            self,
            required_keys: Optional[list[str]]=None,
            optional_keys: Optional[list[str]]=None,
            message: Optional[str]=None
        ) -> 'Coerce':
        """
        Add a Dictionary validator to the Coerce instance.

        Args:
            required_keys (Optional[list[str]]): A list of required keys in the dictionary (default is None).
            optional_keys (Optional[list[str]]): A list of optional keys in the dictionary (default is None).

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Dictionary(
            coercer=self,
            required_keys=required_keys,
            optional_keys=optional_keys
        )
        if message:
            validator.message = message
        self.validations.append(validator)
        return self
    
    def numeric(self, message: Optional[str]=None) -> 'Coerce':
        """
        Add a Numeric validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Numeric(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def min(self, minimum: int, message: Optional[str]=None) -> 'Coerce':
        """
        Add a Min validator to the Coerce instance.

        Args:
            minimum (int): The minimum value allowed.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Min(coercer=self, value=minimum)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def max(self, maximum: int, message: Optional[str]=None) -> 'Coerce':
        """
        Add a Max validator to the Coerce instance.

        Args:
            maximum (int): The maximum value allowed.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Max(coercer=self, value=maximum)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self
    
    def min_length(self, min: int, message: Optional[str]=None) -> 'Coerce':
        """
        Add a MinLength validator to the Coerce instance.

        Args:
            min (int): The minimum length allowed.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.MinLength(coercer=self, length_min=min)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self
    
    def max_length(self, maximum: int, message: Optional[str]=None) -> 'Coerce':
        """
        Add a MaxLength validator to the Coerce instance.

        Args:
            maximum (int): The maximum length allowed.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.MaxLength(coercer=self, length_max=maximum)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def length(self, *args, message:Optional[str]=None) -> 'Coerce':
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
        
        validator = validators.Length(
            coercer=self, length_min=length_min, length_max=length_max
        )
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def url(self, message:Optional[str]=None): ...
    
    def startswith(self, message:Optional[str]=None): ...
    
    def endswith(self, message:Optional[str]=None): ...
    
    def trim(self, message:Optional[str]=None): ...
    
    def lower(self, message:Optional[str]=None): ...
    
    def upper(self, message:Optional[str]=None): ...

    def contains(self, element: any, message:Optional[str]=None) -> 'Coerce':
        """
        Add a Contains validator to the Coerce instance.

        Args:
            element (Any): The element that the value must contain.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Contains(coercer=self, value=element)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def email(self, message:Optional[str]=None) -> 'Coerce':
        """
        Add an Email validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Email(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self
    
    def lowercase(self, message:Optional[str]=None) -> 'Coerce':
        """
        Add a Lowercase validator to the Coerce instance.

        Returns:
            Coerce: The updated Coerce instance.
        """
        validator = validators.Lowercase(coercer=self)
        if message:
            validator.message = message
        self.validations.append(validator)
        return self

    def parse(self, value: any, message:Optional[str]=None) -> 'Coerce':
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
                msg = f'Error in validating data for value {value}'
                if self.message:
                    msg = self.message
                    
                try:
                    if validation.message:
                        msg = validation.message
                except:
                    pass
                
                raise ParsingError(
                    msg, type(validation).__name__,
                    self
                )
                
        return self.value
