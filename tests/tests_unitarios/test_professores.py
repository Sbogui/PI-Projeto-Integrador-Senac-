import pytest
from unittest.mock import patch

from servicos import cadastrar_professor


def test_cadastrar_professor_sem_nome():

    dados = {
        "nome": "",
        "email": "teste@email.com"
    }

    with pytest.raises(ValueError):
        cadastrar_professor(dados)


def test_cadastrar_professor_email_invalido():

    dados = {
        "nome": "João",
        "email": "email_invalido"
    }

    with pytest.raises(ValueError):
        cadastrar_professor(dados)


@patch("servicos.salvar")
def test_cadastrar_professor_sem_email(mock_salvar):

    retorno = {
        "id": 1,
        "nome": "João"
    }

    mock_salvar.return_value = retorno

    resultado = cadastrar_professor({
        "nome": "João"
    })

    assert resultado == retorno