
import random
from dataclasses import asdict

from sqlalchemy import select

from the_wicker_man.models import Doente


def test_create_doente(session, mock_db_time):
    numero_processo = random.randint(10_000_000, 99_999_999)
    with mock_db_time(model=Doente) as fixed_time:
        doente_data = Doente(
            numero_processo=numero_processo,
            nome="João Silva",
            data_nascimento="1980-01-01",
            sexo="M",
            morada="Rua Exemplo, 123"
        )
        session.add(doente_data)
        session.commit()

    doente_in_db = session.scalar(
        select(Doente).where(Doente.numero_processo == numero_processo)
    )
    assert asdict(doente_in_db) == {
        "id": 1,
        "numero_processo": numero_processo,
        "nome": "João Silva",
        "data_nascimento": "1980-01-01",
        "sexo": "M",
        "morada": "Rua Exemplo, 123",
        "created_at": fixed_time
    }
