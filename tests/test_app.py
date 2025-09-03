import random
from http import HTTPStatus


def _unique_numero_processo() -> int:
    # Generate an 8-digit random number to avoid unique constraint collisions
    return random.randint(10_000_000, 99_999_999)


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_doente(client):
    doente_data = {
        "numero_processo": _unique_numero_processo(),
        "nome": "João Palo Silva",
        "data_nascimento": "1980-01-01",
        "sexo": "M",
        "morada": "Rua Testis, 123"
    }
    response = client.post('/doentes', json=doente_data)
    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json()
    assert response_data["numero_processo"] == doente_data["numero_processo"]
    assert response_data["nome"] == doente_data["nome"]


def test_read_doentes(client):
    response = client.get('/doentes')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert "doentes" in response_data
    assert isinstance(response_data["doentes"], list)


def test_read_doente_not_found(client):
    response = client.get('/doentes/9999')  # Assuming 9999 does not exist
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"error": "Doente not found"}


def test_read_doente(client):
    # First, create a doente to ensure there is one to read
    doente_data = {
        "numero_processo": _unique_numero_processo(),
        "nome": "Maria Silva",
        "data_nascimento": "1990-02-02",
        "sexo": "F",
        "morada": "Avenida Exemplo, 456"
    }
    create_response = client.post('/doentes', json=doente_data)
    assert create_response.status_code == HTTPStatus.CREATED
    created_doente = create_response.json()
    doente_id = created_doente["id"]

    # Now, read the created doente
    read_response = client.get(f'/doentes/{doente_id}')
    assert read_response.status_code == HTTPStatus.OK
    read_doente = read_response.json()
    assert read_doente["numero_processo"] == doente_data["numero_processo"]
    assert read_doente["nome"] == doente_data["nome"]


def test_update_doente(client):
    # First, create a doente to ensure there is one to update
    numero = _unique_numero_processo()
    doente_data = {
        "numero_processo": numero,
        "nome": "Carlos Pereira",
        "data_nascimento": "1975-03-03",
        "sexo": "M",
        "morada": "Praça Exemplo, 789"
    }
    create_response = client.post('/doentes', json=doente_data)
    assert create_response.status_code == HTTPStatus.CREATED
    created_doente = create_response.json()
    doente_id = created_doente["id"]

    # Now, update the created doente
    updated_data = {
        "numero_processo": numero,
        "nome": "Carlos Pereira Updated",
        "data_nascimento": "1975-03-03",
        "sexo": "M",
        "morada": "Praça Exemplo, 789 Updated"
    }
    update_response = client.put(f'/doentes/{doente_id}', json=updated_data)
    assert update_response.status_code == HTTPStatus.OK
    updated_doente = update_response.json()
    assert updated_doente["nome"] == updated_data["nome"]
    assert updated_doente["numero_processo"] == updated_data["numero_processo"]

    # Verify the update by reading the doente again
    read_response = client.get(f'/doentes/{doente_id}')
    assert read_response.status_code == HTTPStatus.OK
    read_doente = read_response.json()
    assert read_doente["nome"] == updated_data["nome"]
    assert read_doente["numero_processo"] == updated_data["numero_processo"]


def test_update_doente_not_found(client):
    updated_data = {
        "numero_processo": _unique_numero_processo(),
        "nome": "Nonexistent Doente",
        "data_nascimento": "2000-04-04",
        "sexo": "F",
        "morada": "Rua Nowhere, 000"
    }
    # Assuming 9999 does not exist
    response = client.put('/doentes/9999', json=updated_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"error": "Doente not found"}


def test_delete_doente(client):
    # First, create a doente to ensure there is one to delete
    doente_data = {
        "numero_processo": _unique_numero_processo(),
        "nome": "Ana Costa",
        "data_nascimento": "1985-05-05",
        "sexo": "F",
        "morada": "Rua Sample, 101"
    }
    create_response = client.post('/doentes', json=doente_data)
    assert create_response.status_code == HTTPStatus.CREATED
    created_doente = create_response.json()
    doente_id = created_doente["id"]

    # Now, delete the created doente
    delete_response = client.delete(f'/users/{doente_id}')
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json() == {'message': 'User deleted'}

    # Verify the deletion by attempting to read the doente again
    read_response = client.get(f'/doentes/{doente_id}')
    assert read_response.status_code == HTTPStatus.OK
    assert read_response.json() == {"error": "Doente not found"}


def test_delete_doente_not_found(client):
    # Assuming 9999 does not exist
    response = client.delete('/users/9999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_create_doente_conflict(client):
    # Create a doente
    numero = _unique_numero_processo()
    payload = {
        "numero_processo": numero,
        "nome": "Duplicado",
        "data_nascimento": "1999-09-09",
        "sexo": "M",
        "morada": "Rua Duplicada, 1"
    }

    r1 = client.post('/doentes', json=payload)
    assert r1.status_code == HTTPStatus.CREATED

    # Try to create another doente with the same numero_processo
    r2 = client.post('/doentes', json=payload)
    assert r2.status_code == HTTPStatus.CONFLICT
    assert r2.json() == {
        'detail': 'Doente with this numero_processo already exists'
    }
