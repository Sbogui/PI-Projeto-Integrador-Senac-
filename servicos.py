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
    Turma,
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


def listar_turmas():
    return listar_generico(
        Turma,
        Turma.nome_turma
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


PERIODOS_VALIDOS = {
    "Manhã - 1º período", "Manhã - 2º período", "Manhã - 3º período",
    "Tarde - 1º período", "Tarde - 2º período", "Tarde - 3º período",
    "Noite - 1º período", "Noite - 2º período", "Noite - 3º período",
}

SITUACOES_PRESENCA_VALIDAS = {"P", "F", "A", "J"}


def validar_periodo(periodo):

    if periodo not in PERIODOS_VALIDOS:
        raise ValueError(
            "Período inválido. Selecione um turno e período válidos."
        )


def validar_situacao_presenca(situacao):

    if situacao not in SITUACOES_PRESENCA_VALIDAS:
        raise ValueError(
            "Situação inválida. Use Presente, Ausente, Atestado ou Justificado."
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

    session = SessionLocal()

    try:

        disciplinas_ids = dados.pop("disciplinas", [])

        curso = Curso(**dados)

        session.add(curso)

        session.commit()

        session.refresh(curso)

        for id_disciplina in disciplinas_ids:

            disciplina = session.get(
                Disciplina,
                int(id_disciplina)
            )

            if disciplina:
                disciplina.id_curso = curso.id_curso

        session.commit()

        session.refresh(curso)

        return curso.to_dict()

    except Exception as e:

        session.rollback()

        raise e

    finally:

        session.close()

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


def cadastrar_turma(dados):

    validar_texto(
        dados.get("nome_turma"),
        "Turma"
    )

    return salvar(Turma, dados)


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

    session = SessionLocal()

    try:

        curso = session.get(Curso, id_obj)

        if not curso:
            return None

        if "nome_curso" in dados:
            validar_texto(
                dados["nome_curso"],
                "Curso"
            )

        disciplinas_ids = dados.pop("disciplinas", [])

        for chave, valor in dados.items():
            setattr(curso, chave, valor)

        disciplinas_atuais = list(curso.disciplinas)

        for disciplina in disciplinas_atuais:

            if str(disciplina.id_disciplina) not in disciplinas_ids:
                disciplina.id_curso = None

        for id_disciplina in disciplinas_ids:

            disciplina = session.get(
                Disciplina,
                int(id_disciplina)
            )

            if disciplina:
                disciplina.id_curso = curso.id_curso

        session.commit()

        session.refresh(curso)

        return curso.to_dict()

    except Exception as e:

        session.rollback()

        print(e)

        raise e

    finally:

        session.close()

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


# ==================================================
# TURMAS (cadastro administrativo simples)
# ==================================================

def atualizar_turma(id_obj, dados):

    if "nome_turma" in dados:
        validar_texto(
            dados["nome_turma"],
            "Turma"
        )

    return atualizar(Turma, id_obj, dados)


def excluir_turma(id_obj):
    return excluir(Turma, id_obj)


# ==================================================
# ÁREA DO PROFESSOR
# ==================================================
#
# Todas as funções abaixo resolvem o Professor a partir do id_usuario
# da sessão logada — nunca a partir de um id vindo do cliente. Isso
# garante que um professor nunca acesse dados de outro.

class AcessoNegadoError(Exception):
    """Levantada quando um professor tenta acessar um recurso que não é seu."""
    pass


def _media_aluno(notas):

    notas_validas = [n.nota for n in notas if n.nota is not None]

    if not notas_validas:
        return None

    return round(sum(notas_validas) / len(notas_validas), 1)


def _frequencia_aluno(presencas):

    if not presencas:
        return None

    total = len(presencas)
    presentes = len([p for p in presencas if p.presente == "P"])

    return round((presentes / total) * 100, 1)


def _obter_professor_por_usuario(session, id_usuario):

    professor = session.scalar(
        select(Professor).where(Professor.id_usuario == id_usuario)
    )

    if not professor:
        raise AcessoNegadoError(
            "Nenhum professor vinculado a este usuário."
        )

    return professor


def _validar_turma_do_professor(session, id_usuario, id_turma):

    professor = _obter_professor_por_usuario(session, id_usuario)

    turma = session.get(Turma, id_turma)

    if not turma or turma.id_professor != professor.id:
        raise AcessoNegadoError(
            "Esta turma não pertence a este professor."
        )

    return professor, turma


def _validar_aluno_na_turma(session, turma, id_aluno):

    matricula = session.scalar(
        select(Matricula).where(
            Matricula.id_turma == turma.id_turma,
            Matricula.id_aluno == id_aluno,
        )
    )

    if not matricula:
        raise AcessoNegadoError(
            "Este aluno não está matriculado nesta turma."
        )

    return matricula


def obter_dashboard_professor(id_usuario):

    session = SessionLocal()

    try:
        professor = session.scalar(
            select(Professor)
            .options(
                selectinload(Professor.turmas).selectinload(Turma.matriculas),
                selectinload(Professor.disciplinas),
                selectinload(Professor.cursos),
            )
            .where(Professor.id_usuario == id_usuario)
        )

        if not professor:
            raise AcessoNegadoError(
                "Nenhum professor vinculado a este usuário."
            )

        resumo_turmas = [
            {
                "id_turma": turma.id_turma,
                "nome_turma": turma.nome_turma,
                "disciplina": turma.disciplina.nome_disciplina if turma.disciplina else "—",
                "curso": turma.curso.nome_curso if turma.curso else "—",
                "quantidade_alunos": len(turma.matriculas),
            }
            for turma in professor.turmas
        ]

        return {
            "nome": professor.nome,
            "quantidade_disciplinas": len(professor.disciplinas),
            "quantidade_cursos": len(professor.cursos),
            "quantidade_turmas": len(resumo_turmas),
            "total_alunos": sum(item["quantidade_alunos"] for item in resumo_turmas),
            "turmas": resumo_turmas,
        }

    finally:
        session.close()


def listar_turmas_professor(id_usuario):

    session = SessionLocal()

    try:
        professor = _obter_professor_por_usuario(session, id_usuario)

        turmas = session.scalars(
            select(Turma)
            .options(selectinload(Turma.matriculas))
            .where(Turma.id_professor == professor.id)
            .order_by(Turma.nome_turma)
        ).unique().all()

        return [turma.to_dict() for turma in turmas]

    finally:
        session.close()


def obter_turma_detalhe(id_usuario, id_turma):

    session = SessionLocal()

    try:
        professor, turma = _validar_turma_do_professor(session, id_usuario, id_turma)

        turma = session.scalar(
            select(Turma)
            .options(
                selectinload(Turma.matriculas)
                .selectinload(Matricula.aluno)
                .selectinload(Aluno.notas),
                selectinload(Turma.matriculas)
                .selectinload(Matricula.aluno)
                .selectinload(Aluno.presencas),
                selectinload(Turma.curso),
                selectinload(Turma.disciplina),
            )
            .where(Turma.id_turma == id_turma)
        )

        alunos = []

        for matricula in turma.matriculas:

            aluno = matricula.aluno

            if not aluno:
                continue

            notas_disciplina = [
                n for n in aluno.notas
                if n.id_disciplina == turma.id_disciplina
            ]

            presencas_disciplina = [
                p for p in aluno.presencas
                if p.id_disciplina == turma.id_disciplina
            ]

            alunos.append({
                "id_aluno": aluno.id,
                "nome": aluno.nome,
                "situacao": matricula.situacao or "—",
                "media_atual": _media_aluno(notas_disciplina),
                "frequencia": _frequencia_aluno(presencas_disciplina),
            })

        return {
            "id_turma": turma.id_turma,
            "nome_turma": turma.nome_turma,
            "turno": turma.turno,
            "ano_letivo": turma.ano_letivo,
            "curso": turma.curso.nome_curso if turma.curso else "—",
            "disciplina": turma.disciplina.nome_disciplina if turma.disciplina else "—",
            "alunos": alunos,
        }

    finally:
        session.close()


def cadastrar_nota_professor(id_usuario, dados):

    id_turma = dados.get("id_turma")
    id_aluno = dados.get("id_aluno")

    validar_nota(dados.get("nota"))
    validar_texto(dados.get("tipo_avaliacao"), "Avaliação")

    session = SessionLocal()

    try:
        professor, turma = _validar_turma_do_professor(session, id_usuario, id_turma)

        _validar_aluno_na_turma(session, turma, id_aluno)

        nota = Nota(
            nota=dados.get("nota"),
            tipo_avaliacao=dados.get("tipo_avaliacao"),
            observacoes=dados.get("observacoes"),
            id_aluno=id_aluno,
            id_disciplina=turma.id_disciplina,
            id_professor=professor.id,
            id_turma=turma.id_turma,
        )

        session.add(nota)

        session.commit()

        session.refresh(nota)

        return nota.to_dict()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def registrar_presencas_turma(id_usuario, dados):
    """
    Registra presença de uma turma inteira em uma aula.

    dados esperado:
    {
        "id_turma": 1,
        "data_aula": "2026-07-22",
        "periodo": "Manhã - 1º período",
        "presencas": [
            {"id_aluno": 1, "situacao": "P"},
            {"id_aluno": 2, "situacao": "F"},
        ]
    }
    """

    id_turma = dados.get("id_turma")

    validar_data(dados.get("data_aula"))
    validar_periodo(dados.get("periodo"))

    lista_presencas = dados.get("presencas") or []

    if not lista_presencas:
        raise ValueError(
            "Informe ao menos um aluno para registrar presença."
        )

    for item in lista_presencas:
        validar_situacao_presenca(item.get("situacao"))

    session = SessionLocal()

    try:
        professor, turma = _validar_turma_do_professor(session, id_usuario, id_turma)

        registros_criados = []

        for item in lista_presencas:

            id_aluno = item.get("id_aluno")

            matricula = _validar_aluno_na_turma(session, turma, id_aluno)

            presenca = Presenca(
                data_aula=dados.get("data_aula"),
                presente=item.get("situacao"),
                periodo=dados.get("periodo"),
                id_matricula=matricula.id_matricula,
                id_aluno=id_aluno,
                id_disciplina=turma.id_disciplina,
                id_professor=professor.id,
                id_turma=turma.id_turma,
            )

            session.add(presenca)
            registros_criados.append(presenca)

        session.commit()

        for presenca in registros_criados:
            session.refresh(presenca)

        return [presenca.to_dict() for presenca in registros_criados]

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def historico_notas_aluno(id_usuario, id_turma, id_aluno):

    session = SessionLocal()

    try:
        professor, turma = _validar_turma_do_professor(session, id_usuario, id_turma)

        _validar_aluno_na_turma(session, turma, id_aluno)

        notas = session.scalars(
            select(Nota)
            .where(
                Nota.id_aluno == id_aluno,
                Nota.id_disciplina == turma.id_disciplina,
            )
            .order_by(Nota.id_nota)
        ).all()

        return {
            "media": _media_aluno(notas),
            "notas": [
                {
                    "id_nota": n.id_nota,
                    "tipo_avaliacao": n.tipo_avaliacao,
                    "nota": n.nota,
                    "observacoes": n.observacoes,
                }
                for n in notas
            ],
        }

    finally:
        session.close()


def historico_presencas_aluno(id_usuario, id_turma, id_aluno):

    session = SessionLocal()

    try:
        professor, turma = _validar_turma_do_professor(session, id_usuario, id_turma)

        _validar_aluno_na_turma(session, turma, id_aluno)

        presencas = session.scalars(
            select(Presenca)
            .where(
                Presenca.id_aluno == id_aluno,
                Presenca.id_disciplina == turma.id_disciplina,
            )
            .order_by(Presenca.data_aula)
        ).all()

        total_presencas = len([p for p in presencas if p.presente == "P"])
        total_faltas = len([p for p in presencas if p.presente == "F"])

        return {
            "percentual_frequencia": _frequencia_aluno(presencas),
            "total_presencas": total_presencas,
            "total_faltas": total_faltas,
            "registros": [
                {
                    "data_aula": p.data_aula,
                    "periodo": p.periodo,
                    "status": p.presente,
                }
                for p in presencas
            ],
        }

    finally:
        session.close()