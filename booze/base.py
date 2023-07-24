import inspect
from booze.errors import ParsingError


class Base:
    """
    Eng: The Base class is a metaprogramming-based class that allows automatic parsing and validation of keyword arguments
    passed during object creation. It provides a convenient way to create objects with pre-defined validation rules
    for attributes.

    PT-BR: A classe Base é uma classe baseada em metaprogramação que permite validação e
    parsing automático para os validadores durante a criação do objeto.
    Ela promove uma forma conveniente para criar objetos com regras predefinidas de
    validação passadas de forma encadeada.

    Examples:
    
        >>> # Example 1: Valid input data
        >>> obj1 = MyClass1(name="John", age=30, is_active=True)
        >>> obj1.name == "John" -> True
        >>> obj1.age == 30 -> True \n
        >>> obj1.is_active is True -> True
        >>> obj1.to_dict() == {'name': 'John', 'age': 30, 'is_active': True} -> True

        >>> # Example 2: Invalid input data for name attribute
        >>> with pytest.raises(ParsingError):
        >>>     MyClass1(name="Jo", age=30, is_active=True)

        >>> # Example 3: Invalid input data for age attribute (non-integer)
        >>> with pytest.raises(ParsingError):
        >>>     MyClass1(name="John", age="30", is_active=True)

        >>> # Example 4: Invalid input data for name attribute (length out of range)
        >>> with pytest.raises(ParsingError):
        >>>     MyClass1(name="J", age=30, is_active=True)

        >>> # Example 5: Invalid input data for age attribute (below minimum)
        >>> with pytest.raises(ParsingError):
        >>>     MyClass1(name="John", age=16, is_active=True)
            
        >>> # Example 6: Valid input data
        >>> obj2 = MyClass2(email="test@example.com", height=1.75, favorite_numbers=[42, 7, 15])
        >>> obj2.email == "test@example.com" -> True
        >>> obj2.height == 1.75 -> True
        >>> obj2.favorite_numbers == [42, 7, 15] -> True
        >>> obj2.to_dict() == {'email': 'test@example.com', 'height': 1.75, 'favorite_numbers': [42, 7, 15]} -> True

        >>> # Example 7: Invalid input data for email attribute (invalid email format)
        >>> with pytest.raises(ParsingError):
        >>>    MyClass2(email="invalid_email", height=1.75, favorite_numbers=[42, 7, 15])

        >>> # Example 8: Invalid input data for height attribute (below minimum)
        >>> with pytest.raises(ParsingError):
        >>>     MyClass2(email="test@example.com", height=-1.5, favorite_numbers=[42, 7, 15])

        >>> # Example 9: Invalid input data for height attribute (above maximum)
        >>> with pytest.raises(ParsingError):
        >>>     MyClass2(email="test@example.com", height=3.0, favorite_numbers=[42, 7, 15])

        >>> # Example 10: Invalid input data for favorite_numbers attribute (does not contain 42)
        >>> with pytest.raises(ParsingError):
        >>>     MyClass2(email="test@example.com", height=1.75, favorite_numbers=[7, 15])

    """

    def __new__(cls, **kwargs):
        """
        Creates a new instance of the class with the given keyword arguments, and automatically parses and validates them
        based on the predefined rules.

        Args:
            **kwargs (dict): Keyword arguments representing the attributes of the object.

        Returns:
            object (object): An instance of the class with the parsed and validated attributes.

        Raises:
            ParsingError: If an attribute is not registered with a Coercer, or if the parsing/validation fails.

        Examples:
            >>> "See class-level examples for usage."
        """
        parsers = {}
        for key, item in cls.__dict__.items():
            if not str(key).startswith('_'):
                parsers[key] = item

        def repr(self):
            """
            Return a string representation of the object.

            Returns:
                str: A string representation of the object in the format '<Class(attr1=value1, attr2=value2, ...)>'
            """
            string = '<'
            string += type(self).__name__
            string += '(' + ', '.join([
                f"{key}='{item}'" if isinstance(item, str) else f"{key}={item}"
                for key, item in self.__dict__.items()
            ])
            string += ')>'
            return string

        def to_dict(self):
            """
            Convert the object to a dictionary containing its attributes.

            Returns:
                dict: A dictionary containing the object's attributes and their values.
            """
            return {
                key: getattr(self, key) for key in parsers
                if not inspect.ismethod(getattr(self, key))
            }

        cls.__repr__ = repr
        cls.__str__ = repr
        cls.to_dict = to_dict

        obj = object.__new__(cls)
        for key, value in kwargs.items():
            try:
                parser = parsers[key]
            except KeyError:
                raise ParsingError('Erro na atribuição do valor. '
                                    'Você lembrou de cadastrar um Coercer para ela?')

            parsed = parser.parse(value)

            obj.__setattr__(key, parsed)

        return obj
