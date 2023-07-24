import re
from abc import ABC, abstractmethod
from booze.errors import *
from contextlib import suppress
import datetime
with suppress(ImportError):
    from booze.coercer import Coerce
    


def check_numeric(value):
    test = []
    try:
        float(value)
        test.append(True)
    except:
        test.append(False)
        
    try:
        int(value)
        test.append(True)
    except:
        test.append(False)
        
    return any(test)


class Validator(ABC):
    def __str__(self):
        return f'<Validator: {type(self).__name__}, args:({self.__dict__})>'


class Integer(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    
    def __call__(self, value):
        try:
            self.coercer.value = int(value)
            return True
        except (TypeError, ValueError):
            return False
    
    def __str__(self):
        return f'<Validator: {type(self).__name__}, args:({self.__dict__})>'


class Float(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
        
    def __call__(self, value):
        try:
            self.coercer.value = float(value)
            return True
        except (TypeError, ValueError):
            return False



class Date(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
        self.handler = {
            'MM/DD/YYYY': "%m/%d/%Y",
            'DD-MM-YYYY': "%d-%m-%Y",
            'MM-DD-YYYY': "%m-%d-%Y",
            'YYYY-MM-DD': "%Y-%m-%d",
            'YYYY-DD-MM': "%Y-%d-%m",
            'MM/YYYY/DD': "%m/%Y/%d",
            'DD-Mon-YYYY': "%d-%b-%Y",
            'Mon-DD-YYYY': "%b-%d-%Y",
            'YYYY-Mon-DD': "%Y-%b-%d",
            'YYYY/DD/MM': "%Y/%d/%m",
            'Mon/DD/YYYY': "%b/%d/%Y",
            'YYYY/MM/DD': "%Y/%m/%d",
            'DD.MM.YYYY': "%d.%m.%Y",
            'MM.DD.YYYY': "%m.%d.%Y",
            'YYYY.MM.DD': "%Y.%m.%d",
            'YYYY.DD.MM': "%Y.%d.%m",
            'MM/YYYY/DD': "%m/%Y/%d",
            'DD-Mon-YY': "%d-%b-%y",
            'Mon-DD-YY': "%b-%d-%y",
            'YY-Mon-DD': "%y-%b-%d",
            'YY/DD/MM': "%y/%d/%m",
            'Mon/DD/YY': "%b/%d/%y",
            'YY/MM/DD': "%y/%m/%d",
            'DDMMYYYY': "%d%m%Y",
            'MMDDYYYY': "%m%d%Y",
            'YYYYMMDD': "%Y%m%d",
            'YYYYDDMM': "%Y%d%m",
            'MMYYYYDD': "%m%Y%d",
            'DDMonYY': "%d%b%y",
            'MonDDYY': "%b%d%y",
            'YYMonDD': "%y%b%d",
            'YYDDMM': "%y%d%m",
            'MonDDYY': "%b%d%y",
            'YYMMDD': "%y%m%d",
        }
    
    def __call__(self, value):
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
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
        self.handler = {
            'MM/DD/YYYY HH:mm:ss': "%m/%d/%Y %H:%M:%S",
            'DD-MM-YYYY HH:mm:ss': "%d-%m-%Y %H:%M:%S",
            'MM-DD-YYYY HH:mm:ss': "%m-%d-%Y %H:%M:%S",
            'YYYY-MM-DD HH:mm:ss': "%Y-%m-%d %H:%M:%S",
            'YYYY-DD-MM HH:mm:ss': "%Y-%d-%m %H:%M:%S",
            'MM/YYYY/DD HH:mm:ss': "%m/%Y/%d %H:%M:%S",
            'DD-Mon-YYYY HH:mm:ss': "%d-%b-%Y %H:%M:%S",
            'Mon-DD-YYYY HH:mm:ss': "%b-%d-%Y %H:%M:%S",
            'YYYY-Mon-DD HH:mm:ss': "%Y-%b-%d %H:%M:%S",
            'YYYY/DD/MM HH:mm:ss': "%Y/%d/%m %H:%M:%S",
            'Mon/DD/YYYY HH:mm:ss': "%b/%d/%Y %H:%M:%S",
            'YYYY/MM/DD HH:mm:ss': "%Y/%m/%d %H:%M:%S",
            'DD.MM.YYYY HH:mm:ss': "%d.%m.%Y %H:%M:%S",
            'MM.DD.YYYY HH:mm:ss': "%m.%d.%Y %H:%M:%S",
            'YYYY.MM.DD HH:mm:ss': "%Y.%m.%d %H:%M:%S",
            'YYYY.DD.MM HH:mm:ss': "%Y.%d.%m %H:%M:%S",
            'MM/YYYY/DD HH:mm:ss': "%m/%Y/%d %H:%M:%S",
            'DD-Mon-YY HH:mm:ss': "%d-%b-%y %H:%M:%S",
            'Mon-DD-YY HH:mm:ss': "%b-%d-%y %H:%M:%S",
            'YY-Mon-DD HH:mm:ss': "%y-%b-%d %H:%M:%S",
            'YY/DD/MM HH:mm:ss': "%y/%d/%m %H:%M:%S",
            'Mon/DD/YY HH:mm:ss': "%b/%d/%y %H:%M:%S",
            'YY/MM/DD HH:mm:ss': "%y/%m/%d %H:%M:%S",
            'DDMMYYYY HH:mm:ss': "%d%m%Y %H:%M:%S",
            'MMDDYYYY HH:mm:ss': "%m%d%Y %H:%M:%S",
            'YYYYMMDD HH:mm:ss': "%Y%m%d %H:%M:%S",
            'YYYYDDMM HH:mm:ss': "%Y%d%m %H:%M:%S",
            'MMYYYYDD HH:mm:ss': "%m%Y%d %H:%M:%S",
            'DDMonYY HH:mm:ss': "%d%b%y %H:%M:%S",
            'MonDDYY HH:mm:ss': "%b%d%y %H:%M:%S",
            'YYMonDD HH:mm:ss': "%y%b%d %H:%M:%S",
            'YYDDMM HH:mm:ss': "%y%d%m %H:%M:%S",
            'MonDDYY HH:mm:ss': "%b%d%y %H:%M:%S",
            'YYMMDD HH:mm:ss': "%y%m%d %H:%M:%S",
        }
    
    def __call__(self, value):
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
    def __init__(self, coercer: 'Coerce', format_string):
        self.coercer = coercer
        self.format_string = format_string
        self.handler = {
            'MM/DD/YYYY': "%m/%d/%Y",
            'DD-MM-YYYY': "%d-%m-%Y",
            'MM-DD-YYYY': "%m-%d-%Y",
            'YYYY-MM-DD': "%Y-%m-%d",
            'YYYY-DD-MM': "%Y-%d-%m",
            'MM/YYYY/DD': "%m/%Y/%d",
            'DD-Mon-YYYY': "%d-%b-%Y",
            'Mon-DD-YYYY': "%b-%d-%Y",
            'YYYY-Mon-DD': "%Y-%b-%d",
            'YYYY/DD/MM': "%Y/%d/%m",
            'Mon/DD/YYYY': "%b/%d/%Y",
            'YYYY/MM/DD': "%Y/%m/%d",
            'DD.MM.YYYY': "%d.%m.%Y",
            'MM.DD.YYYY': "%m.%d.%Y",
            'YYYY.MM.DD': "%Y.%m.%d",
            'YYYY.DD.MM': "%Y.%d.%m",
            'MM/YYYY/DD': "%m/%Y/%d",
            'DD-Mon-YY': "%d-%b-%y",
            'Mon-DD-YY': "%b-%d-%y",
            'YY-Mon-DD': "%y-%b-%d",
            'YY/DD/MM': "%y/%d/%m",
            'Mon/DD/YY': "%b/%d/%y",
            'YY/MM/DD': "%y/%m/%d",
            'DDMMYYYY': "%d%m%Y",
            'MMDDYYYY': "%m%d%Y",
            'YYYYMMDD': "%Y%m%d",
            'YYYYDDMM': "%Y%d%m",
            'MMYYYYDD': "%m%Y%d",
            'DDMonYY': "%d%b%y",
            'MonDDYY': "%b%d%y",
            'YYMonDD': "%y%b%d",
            'YYDDMM': "%y%d%m",
            'MonDDYY': "%b%d%y",
            'YYMMDD': "%y%m%d",
        }
    
    def __call__(self, value):
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
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value):
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
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
        
    def __call__(self, value):
        self.coercer.value = str(value)
        return isinstance(value, str)


class Strict(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
        
    def __call__(self, value):
        return self.coercer.value == value
    

class List(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    def __call__(self, value):
        return isinstance(value, list)


class Dictionary(Validator):
    def __init__(self, coercer: 'Coerce', required_keys, optional_keys):
        self.coercer = coercer
        self.required_keys = required_keys
        self.optional_keys = optional_keys
        
    def __call__(self, value):
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
    def __init__(self, coercer: 'Coerce', required_keys):
        self.coercer = coercer
        self.required_keys = required_keys
        
    def __call__(self, value):
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
    def __init__(self, coercer: 'Coerce', value):
        self.coercer = coercer
        self.min = value
        
    def __call__(self, value):
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
    def __init__(self, coercer: 'Coerce', value):
        self.coercer = coercer
        self.max = value
        
    def __call__(self, value):
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
    def __init__(self, coercer: 'Coerce', length_min, length_max):
        self.coercer = coercer
        self.length_min = length_min
        self.length_max = length_max
        
    def __call__(self, value):
        test = self.length_min <= len(value) <= self.length_max
        return test


class MinLength(Validator):
    def __init__(self, coercer: 'Coerce', length_min):
        self.coercer = coercer
        self.length_min = length_min
        
    def __call__(self, value):
        test = self.length_min <= len(value)
        return test


class MaxLength(Validator):
    def __init__(self, coercer: 'Coerce', length_max):
        self.coercer = coercer
        self.length_max = length_max
        
    def __call__(self, value):
        test = len(value) <= self.length_max
        return test


class Contains(Validator):
    def __init__(self, coercer: 'Coerce', value):
        self.coercer = coercer
        self.value = value
    def __call__(self, value):
        return self.value in value


class Email(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    def __call__(self, value):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, value) is not None


class Lowercase(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    def __call__(self, value):
        try:
            self.coercer.value = value.lower()
            return True
        except:
            return False



class Numeric(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    def __call__(self, value: any):
        return check_numeric(value)
