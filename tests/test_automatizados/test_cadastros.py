import pytest

from servicos import cadastrar_professor


def test_cadastrar_professor_sem_nome():

    dados = {
        "nome": "",
        "email": "teste@email.com"
    }

    with pytest.raises(ValueError) as erro:
        cadastrar_professor(dados)

    assert str(erro.value) == "Nome é obrigatório."
    
