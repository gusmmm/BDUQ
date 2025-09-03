from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str

class DoenteSchema(BaseModel):
    numero_processo: int
    nome: str
    data_nascimento: str
    sexo: str
    morada: str

