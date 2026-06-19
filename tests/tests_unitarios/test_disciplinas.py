import pytest
from unittest.mock import patch

from servicos import cadastrar_disciplina


@patch("servicos.salvar")
def test_cadastrar_disciplina_sucesso(mock_salvar):

    retorno = {
        "id_disciplina": 1,
        "nome_disciplina": "Python"
    }

    mock_salvar.return_value = retorno

    resultado = cadastrar_disciplina({
        "nome_disciplina": "Python"
    })

    assert resultado == retorno


def test_cadastrar_disciplina_sem_nome():

    with pytest.raises(ValueError):

        cadastrar_disciplina({
            "nome_disciplina": ""
        })