from sqlalchemy import select

from the_wicker_man.models import Doente

NUMERO_PROCESSO = 12345


def test_create_doente(session):
    doente_data = Doente(
        numero_processo=NUMERO_PROCESSO,
        nome="João Silva",
        data_nascimento="1980-01-01",
        sexo="M",
        morada="Rua Exemplo, 123"
    )
    session.add(doente_data)
    session.commit()

    doente_in_db = session.scalar(
        select(Doente).where(Doente.numero_processo == NUMERO_PROCESSO)
    )
    assert doente_in_db is not None
    assert doente_in_db.nome == "João Silva"
    assert doente_in_db.numero_processo == NUMERO_PROCESSO
    assert doente_in_db.sexo == "M"
    assert doente_in_db.morada == "Rua Exemplo, 123"
    assert doente_in_db.data_nascimento == "1980-01-01"
