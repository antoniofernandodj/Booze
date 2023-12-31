from booze import Coerce, ParsingError, Base
from pprint import pprint


msg1 = "O usuário deve ser maior de idade!"
msg2 = "O usúário deve ter no máximo 30 anos de idade"
class Pessoa(Base):
    nome = Coerce().string().length(3, 15)
    idade = Coerce().min(18).max(30)
    email = Coerce().string().email()
    
try:
    p1 = Pessoa(nome='luiza', idade=15, email='analufavacho@gmail.com')
except ParsingError as e:
    pprint(e.dict())
