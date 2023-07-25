from booze import Coerce, ParsingError, Base
from pprint import pprint


msg1 = "O usuário deve ser maior de idade!"
msg2 = "O usúário deve ter no máximo 30 anos de idade"
class Pessoa(Base):
    nome = Coerce('nome').string().length(3, 15)
    idade = Coerce('idade').min(18, message=msg1).max(30, message=msg2)
    email = Coerce('email').string().email()
    
try:
    p1 = Pessoa(nome='luiza', idade=15, email='analufavacho@gmail.com')
except ParsingError as e:
    pprint(e.dict())