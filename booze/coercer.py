from booze.errors import *
import re
from booze import validators
import typing as t
import uuid


class Coerce:
    """
    Coerce class provides a set of validation methods to parse and validate data types.
    Call `parse(value)` after setting the validation rules to parse the value. If the value
    passes all validations, the parsed value is returned; otherwise, a ParsingError is raised.
    """
    def __init__(self, name=str(uuid.uuid4())):
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

    def integer(self):
        validator = validators.Integer(coercer=self)
        self.validations.append(validator)
        return self
    
    def date(self):
        validator = validators.Date(coercer=self)
        self.validations.append(validator)
        return self
    
    
    def datetime(self):
        validator = validators.DateTime(coercer=self)
        self.validations.append(validator)
        return self
    
    def strict(self):
        validator = validators.Strict(coercer=self)
        self.validations.append(validator)
        return self
    
    def format_date(self, format_string):
        validator = validators.FormatDate(coercer=self, format_string=format_string)
        self.validations.append(validator)
        return self

    def float(self):
        validator = validators.Float(coercer=self)
        self.validations.append(validator)
        return self

    def boolean(self):
        validator = validators.Boolean(coercer=self)
        self.validations.append(validator)
        return self

    def string(self):
        validator = validators.String(coercer=self)
        self.validations.append(validator)
        return self

    def list(self):
        validator = validators.List(coercer=self)
        self.validations.append(validator)
        return self

    def dictionary(self, required_keys=None, optional_keys=None):
        validator = validators.Dictionary(
            coercer=self,
            required_keys=required_keys,
            optional_keys=optional_keys
        )
        self.validations.append(validator)
        return self
    


    def required_keys(self, required_keys):
        validator = validators.RequiredKeys(coercer=self, required_keys=required_keys)
        self.validations.append(validator)
        return self


    def dict(self, *, required_keys=None, optional_keys=None):
        validator = validators.Dictionary(
            coercer=self,
            required_keys=required_keys,
            optional_keys=optional_keys
        )
        self.validations.append(validator)
        return self
    
    
    def numeric(self):
        validator = validators.Numeric(coercer=self)
        self.validations.append(validator)
        return self

    def min(self, minimum):
        validator = validators.Min(coercer=self, value=minimum)
        self.validations.append(validator)
        return self

    def max(self, maximum):
        validator = validators.Max(coercer=self, value=maximum)
        self.validations.append(validator)
        return self
    
    def min_length(self, min):
        validator = validators.MinLength(coercer=self, length_min=min)
        self.validations.append(validator)
        return self
    
    def max_length(self, maximum):
        validator = validators.MaxLength(coercer=self, length_max=maximum)
        self.validations.append(validator)
        return self

    def length(self, *args):
        if len(args) == 1:
            length_min = 0
            length_max = args[0]
        elif len(args) == 2:
            length_min = args[0]
            length_max = args[1]
        else:
            raise ValueError('O Validador lenght só aceita 1 ou 2 parametros.')
        
        validator = validators.Length(coercer=self, length_min=length_min, length_max=length_max)
        self.validations.append(validator)
        return self

    def contains(self, element):
        validator = validators.Contains(coercer=self, value=element)
        self.validations.append(validator)
        return self

    def email(self):
        validator = validators.Email(coercer=self)
        self.validations.append(validator)
        return self
    
    def lowercase(self):
        validator = validators.Lowercase(coercer=self)
        self.validations.append(validator)
        return self

    def parse(self, value):
        self.value = value
        self.first_value = value
        for validation in self.validations:
            print(validation)
            result = validation(value)
            self.value = validation.coercer.value
            if result == False:
                raise ParsingError(
                    f'Erro na validação dos dados do valor {value}',
                    f'validator: {type(validation).__name__}',
                    f'Coercer {self}'
                )
                
        return self.value

