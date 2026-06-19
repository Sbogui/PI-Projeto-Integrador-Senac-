import pytest
from unittest.mock import patch

from servicos import cadastrar_curso


@patch("servicos.salvar")
def test_cadastrar_curso_sucesso(mock_salvar):

    retorno = {
        "id_curso": 1,
        "nome_curso": "ADS"
    }

    mock_salvar.return_value = retorno

    resultado = cadastrar_curso({
        "nome_curso": "ADS"
    })

    assert resultado == retorno


def test_cadastrar_curso_sem_nome():

    with pytest.raises(ValueError):

        cadastrar_curso({
            "nome_curso": ""
        })