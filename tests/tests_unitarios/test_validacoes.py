import pytest

from servicos import (
    validar_email,
    validar_nota,
    validar_data,
    validar_texto
)


def test_validar_email_valido():

    validar_email("teste@email.com")


def test_validar_email_invalido():

    with pytest.raises(ValueError):
        validar_email("email")


def test_validar_nota_valida():

    validar_nota(10)


def test_validar_nota_menor_que_zero():

    with pytest.raises(ValueError):
        validar_nota(-1)


def test_validar_nota_maior_que_dez():

    with pytest.raises(ValueError):
        validar_nota(11)


def test_validar_nota_texto():

    with pytest.raises(ValueError):
        validar_nota("abc")


def test_validar_data_valida():

    validar_data("2026-06-18")


def test_validar_data_invalida():

    with pytest.raises(ValueError):
        validar_data("18/06/2026")


def test_validar_texto_valido():

    validar_texto("Lucas", "Nome")


def test_validar_texto_vazio():

    with pytest.raises(ValueError):
        validar_texto("", "Nome")


def test_validar_texto_espacos():

    with pytest.raises(ValueError):
        validar_texto("   ", "Nome")