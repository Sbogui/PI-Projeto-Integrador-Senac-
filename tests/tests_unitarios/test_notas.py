import pytest
from unittest.mock import patch

from servicos import cadastrar_nota


@patch("servicos.salvar")
def test_cadastrar_nota_sucesso(mock_salvar):

    retorno = {
        "id_nota": 1,
        "nota": 10
    }

    mock_salvar.return_value = retorno

    resultado = cadastrar_nota({
        "nota": 10
    })

    assert resultado == retorno


def test_cadastrar_nota_invalida():

    with pytest.raises(ValueError):

        cadastrar_nota({
            "nota": 15
        })