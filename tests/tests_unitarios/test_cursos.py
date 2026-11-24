import pytest

from servicos import cadastrar_curso


def test_cadastrar_curso_sucesso():
    # cadastrar_curso usa a sessão direto (não chama salvar),
    # por isso roda contra o banco temporário do conftest.
    resultado = cadastrar_curso({"nome_curso": "ADS"})

    assert resultado["nome_curso"] == "ADS"
    assert resultado["id_curso"] is not None


def test_cadastrar_curso_sem_nome():
    with pytest.raises(ValueError):
        cadastrar_curso({"nome_curso": ""})