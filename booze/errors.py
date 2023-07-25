from typing import Optional
from contextlib import suppress
from typing import Union
with suppress(ImportError):
    from booze.coercer import Coerce

class ParsingError(Exception):
    """
    A custom exception class that can be raised during the parsing process if a value
    fails to pass validation by a specific validator.

    Args:
        message (str): The error message describing the reason for the parsing error.
        validation_func (str, optional): The name of the validation function that raised the error. Default is 'Initializing'.
        coercer (Optional[Coerce], optional): The Coerce object associated with the parsing error. Default is None.

    Attributes:
        message (str): The error message describing the reason for the parsing error.
        validation_func (str): The name of the validation function that raised the error.
        coercer (Optional[Coerce]): The Coerce object associated with the parsing error.

    Methods:
        dict(): Returns a dictionary representation of the ParsingError.

    Example:
        >>> try:
        >>>     p = Person(name='Sponge Bob', idade=2, email='spongebob@squarerpants.com')
        >>> except SomeValidationException as e:
        >>>     raise ParsingError("Invalid value for 'attribute'.", >>> validation_func='validate_attribute', coercer=coercer_instance) from e

    """

    def __init__(
            self, msg: str,
            validation_func: str = 'Initializing',
            coercer: Optional['Coerce'] = None
        ):
        str_msg = str(msg)
        super().__init__(str_msg)
        self.msg = msg
        self.validation_func = validation_func
        self.coercer = coercer

    def dict(self) -> dict:
        """
        Returns a dictionary representation of the ParsingError.

        Returns:
            dict: A dictionary containing the error message, validation function name, and Coerce object.
        """
        if self.coercer is not None:
            return {
                'Error': self.msg,
                'ValidationFunction': self.validation_func,
                'Field': self.coercer.name
            }
        else:
            return {
                'Error Messages': self.msg,
                'Validation': self.validation_func
            }
        

    def __str__(self) -> str:
        """
        Returns a string representation of the ParsingError.

        Returns:
            str: A string containing the error message, validation function name, and Coerce object.
        """
        return f"ParsingError: {self.msg}, ValidationFunction: {self.validation_func}, Coercer: {self.coercer}"
