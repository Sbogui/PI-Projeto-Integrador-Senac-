import pytest
from unittest.mock import patch

from servicos import cadastrar_matricula


@patch("servicos.salvar")
def test_cadastrar_matricula_sucesso(mock_salvar):

    retorno = {
        "id_matricula": 1
    }

    mock_salvar.return_value = retorno

    resultado = cadastrar_matricula({
        "data_matricula": "2026-06-18"
    })

    assert resultado == retorno


def test_cadastrar_matricula_data_invalida():

    with pytest.raises(ValueError):

        cadastrar_matricula({
            "data_matricula": "18/06/2026"
        })