from booze import Coerce, ParsingError, Base

class Pessoa(Base):
    nome = Coerce('nome').string().length(3, 15)
    idade = Coerce('idade').min(18).max(30)
    email = Coerce('email').string().email()
    
try:
    p1 = Pessoa(nome='luiza',idade=17,email='analufavacho@gmail.com')
except ParsingError as erro:
    print(erro.json())
