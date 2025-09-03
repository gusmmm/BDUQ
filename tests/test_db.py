from the_wicker_man.models import Doente

NUMERO_PROCESSO = 12345


def test_create_doente(client):
    doente_data = Doente(
        numero_processo=NUMERO_PROCESSO,
        nome="João Silva",
        data_nascimento="1980-01-01",
        sexo="M",
        morada="Rua Exemplo, 123"
    )

    assert doente_data.numero_processo == NUMERO_PROCESSO
    assert doente_data.nome == "João Silva"
    assert doente_data.data_nascimento == "1980-01-01"
    assert doente_data.sexo == "M"
    assert doente_data.morada == "Rua Exemplo, 123"
    # ID should be None before being set by the database
    assert doente_data.id is None
    # created_at should be None before being
    assert doente_data.created_at is None
