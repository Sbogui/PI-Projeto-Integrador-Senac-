import pytest
from unittest.mock import patch

from servicos import cadastrar_aluno


@patch("servicos.salvar")
def test_cadastrar_aluno_sucesso(mock_salvar):

    retorno = {
        "id": 1,
        "nome": "Lucas"
    }

    mock_salvar.return_value = retorno

    resultado = cadastrar_aluno({
        "nome": "Lucas",
        "email": "lucas@email.com"
    })

    assert resultado == retorno


def test_cadastrar_aluno_sem_nome():

    with pytest.raises(ValueError):

        cadastrar_aluno({
            "nome": "",
            "email": "lucas@email.com"
        })


def test_cadastrar_aluno_email_invalido():

    with pytest.raises(ValueError):

        cadastrar_aluno({
            "nome": "Lucas",
            "email": "abc"
        })