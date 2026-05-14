from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import SessionLocal

import re
from datetime import datetime

from models import (
    Professor,
    Aluno,
    Curso,
    Disciplina,
    Matricula,
    Nota,
    Presenca,
    Telefone,
    Email,
    Endereco,
)

# ==================================================
# LISTAGENS
# ==================================================

def listar_generico(modelo, campo):
    session = SessionLocal()

    try:
        query = select(modelo).order_by(campo)

        linhas = session.scalars(query).unique().all()

        return [x.to_dict() for x in linhas]

    finally:
        session.close()


def listar_professores():
    return listar_generico(
        Professor,
        Professor.nome
    )


def listar_alunos():
    return listar_generico(
        Aluno,
        Aluno.nome
    )


def listar_cursos():
    return listar_generico(
        Curso,
        Curso.nome_curso
    )


def listar_disciplinas():
    return listar_generico(
        Disciplina,
        Disciplina.nome_disciplina
    )


def listar_matriculas():
    return listar_generico(
        Matricula,
        Matricula.id_matricula
    )


def listar_notas():
    return listar_generico(
        Nota,
        Nota.id_nota
    )


def listar_presencas():
    return listar_generico(
        Presenca,
        Presenca.id_presenca
    )


def listar_telefones():
    return listar_generico(
        Telefone,
        Telefone.id_telefone
    )


def listar_emails():
    return listar_generico(
        Email,
        Email.id_email
    )


def listar_enderecos():
    return listar_generico(
        Endereco,
        Endereco.id_endereco
    )


# ==================================================
# SALVAR
# ==================================================

def salvar(modelo, dados):
    session = SessionLocal()

    try:
        obj = modelo(**dados)

        session.add(obj)

        session.commit()

        session.refresh(obj)

        return obj.to_dict()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


# ==================================================
# VALIDACOES
# ==================================================

def validar_email(email):

    if not email:
        return

    padrao = r"^[^@]+@[^@]+\.[^@]+$"

    if not re.match(padrao, email):
        raise ValueError("Email inválido.")


def validar_nota(nota):

    try:
        nota = float(nota)

    except:
        raise ValueError("Nota inválida.")

    if nota < 0 or nota > 10:
        raise ValueError(
            "A nota deve ser entre 0 e 10."
        )


def validar_data(data_texto):

    try:
        datetime.strptime(
            data_texto,
            "%Y-%m-%d"
        )

    except:
        raise ValueError(
            "Data inválida. Use YYYY-MM-DD."
        )


def validar_texto(valor, campo):

    if not valor or not str(valor).strip():
        raise ValueError(
            f"{campo} é obrigatório."
        )


# ==================================================
# CADASTROS
# ==================================================

def cadastrar_professor(dados):

    validar_texto(
        dados.get("nome"),
        "Nome"
    )

    validar_email(
        dados.get("email")
    )

    return salvar(Professor, dados)


def cadastrar_aluno(dados):

    validar_texto(
        dados.get("nome"),
        "Nome"
    )

    validar_email(
        dados.get("email")
    )

    return salvar(Aluno, dados)


def cadastrar_curso(dados):

    validar_texto(
        dados.get("nome_curso"),
        "Curso"
    )

    return salvar(Curso, dados)


def cadastrar_disciplina(dados):

    validar_texto(
        dados.get("nome_disciplina"),
        "Disciplina"
    )

    return salvar(Disciplina, dados)


def cadastrar_matricula(dados):

    validar_data(
        dados.get("data_matricula")
    )

    return salvar(Matricula, dados)


def cadastrar_nota(dados):

    validar_nota(
        dados.get("nota")
    )

    return salvar(Nota, dados)


def cadastrar_presenca(dados):

    validar_data(
        dados.get("data_aula")
    )

    return salvar(Presenca, dados)


def cadastrar_telefone(dados):

    validar_texto(
        dados.get("numero_pessoal"),
        "Telefone pessoal"
    )

    return salvar(Telefone, dados)


def cadastrar_email(dados):

    validar_email(
        dados.get("email_pessoal")
    )

    if dados.get("email_profissional"):
        validar_email(
            dados.get("email_profissional")
        )

    return salvar(Email, dados)


def cadastrar_endereco(dados):

    validar_texto(
        dados.get("rua"),
        "Rua"
    )

    validar_texto(
        dados.get("cidade"),
        "Cidade"
    )

    validar_texto(
        dados.get("estado"),
        "Estado"
    )

    return salvar(Endereco, dados)


# ==================================================
# ATUALIZAR
# ==================================================

def atualizar(modelo, id_obj, dados):
    session = SessionLocal()

    try:
        obj = session.get(modelo, id_obj)

        if not obj:
            return None

        for chave, valor in dados.items():
            setattr(obj, chave, valor)

        session.commit()

        session.refresh(obj)

        return obj.to_dict()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


# ==================================================
# EXCLUIR
# ==================================================

def excluir(modelo, id_obj):
    session = SessionLocal()

    try:
        obj = session.get(modelo, id_obj)

        if not obj:
            return False

        session.delete(obj)

        session.commit()

        return True

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


# ==================================================
# CURSOS
# ==================================================

def atualizar_curso(id_obj, dados):

    if "nome_curso" in dados:
        validar_texto(
            dados["nome_curso"],
            "Curso"
        )

    return atualizar(Curso, id_obj, dados)


def excluir_curso(id_obj):
    return excluir(Curso, id_obj)


# ==================================================
# PROFESSORES
# ==================================================

def atualizar_professor(id_obj, dados):

    if "nome" in dados:
        validar_texto(
            dados["nome"],
            "Nome"
        )

    if "email" in dados:
        validar_email(
            dados["email"]
        )

    return atualizar(Professor, id_obj, dados)


def excluir_professor(id_obj):
    return excluir(Professor, id_obj)


# ==================================================
# ALUNOS
# ==================================================

def atualizar_aluno(id_obj, dados):

    if "nome" in dados:
        validar_texto(
            dados["nome"],
            "Nome"
        )

    if "email" in dados:
        validar_email(
            dados["email"]
        )

    return atualizar(Aluno, id_obj, dados)


def excluir_aluno(id_obj):
    return excluir(Aluno, id_obj)


# ==================================================
# DISCIPLINAS
# ==================================================

def atualizar_disciplina(id_obj, dados):

    if "nome_disciplina" in dados:
        validar_texto(
            dados["nome_disciplina"],
            "Disciplina"
        )

    return atualizar(Disciplina, id_obj, dados)


def excluir_disciplina(id_obj):
    return excluir(Disciplina, id_obj)


# ==================================================
# MATRICULAS
# ==================================================

def atualizar_matricula(id_obj, dados):

    if "data_matricula" in dados:
        validar_data(
            dados["data_matricula"]
        )

    return atualizar(Matricula, id_obj, dados)


def excluir_matricula(id_obj):
    return excluir(Matricula, id_obj)


# ==================================================
# NOTAS
# ==================================================

def atualizar_nota(id_obj, dados):

    if "nota" in dados:
        validar_nota(
            dados["nota"]
        )

    return atualizar(Nota, id_obj, dados)


def excluir_nota(id_obj):
    return excluir(Nota, id_obj)


# ==================================================
# PRESENCAS
# ==================================================

def atualizar_presenca(id_obj, dados):

    if "data_aula" in dados:
        validar_data(
            dados["data_aula"]
        )

    return atualizar(Presenca, id_obj, dados)


def excluir_presenca(id_obj):
    return excluir(Presenca, id_obj)


# ==================================================
# TELEFONES
# ==================================================

def atualizar_telefone(id_obj, dados):

    if "numero_pessoal" in dados:
        validar_texto(
            dados["numero_pessoal"],
            "Telefone pessoal"
        )

    return atualizar(Telefone, id_obj, dados)


def excluir_telefone(id_obj):
    return excluir(Telefone, id_obj)


# ==================================================
# EMAILS
# ==================================================

def atualizar_email(id_obj, dados):

    if "email_pessoal" in dados:
        validar_email(
            dados["email_pessoal"]
        )

    if "email_profissional" in dados:
        validar_email(
            dados["email_profissional"]
        )

    return atualizar(Email, id_obj, dados)


def excluir_email(id_obj):
    return excluir(Email, id_obj)


# ==================================================
# ENDERECOS
# ==================================================

def atualizar_endereco(id_obj, dados):

    if "rua" in dados:
        validar_texto(
            dados["rua"],
            "Rua"
        )

    if "cidade" in dados:
        validar_texto(
            dados["cidade"],
            "Cidade"
        )

    if "estado" in dados:
        validar_texto(
            dados["estado"],
            "Estado"
        )

    return atualizar(Endereco, id_obj, dados)


def excluir_endereco(id_obj):
    return excluir(Endereco, id_obj)