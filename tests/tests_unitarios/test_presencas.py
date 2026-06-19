import pytest
from unittest.mock import patch

from servicos import cadastrar_presenca


@patch("servicos.salvar")
def test_cadastrar_presenca_sucesso(mock_salvar):

    retorno = {
        "id_presenca": 1
    }

    mock_salvar.return_value = retorno

    resultado = cadastrar_presenca({
        "data_aula": "2026-06-18"
    })

    assert resultado == retorno


def test_cadastrar_presenca_data_invalida():

    with pytest.raises(ValueError):

        cadastrar_presenca({
            "data_aula": "18/06/2026"
        })