import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from database import Base
import servicos
from servicos import (
    obter_dashboard_professor,
    listar_turmas_professor,
    obter_turma_detalhe,
    cadastrar_nota_professor,
    registrar_presencas_turma,
    historico_notas_aluno,
    historico_presencas_aluno,
    validar_periodo,
    validar_situacao_presenca,
    AcessoNegadoError,
)
from models import Usuario, Professor, Curso, Disciplina, Turma, Aluno, Matricula


@pytest.fixture
def banco_teste(monkeypatch):
    """
    Banco SQLite em memória, isolado do banco real do projeto.
    Substitui o SessionLocal usado por servicos.py apenas durante o teste.
    """

    engine_teste = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine_teste)

    SessionTeste = sessionmaker(bind=engine_teste)

    monkeypatch.setattr(servicos, "SessionLocal", SessionTeste)

    yield SessionTeste


@pytest.fixture
def cenario(banco_teste):
    """
    Popula um cenário simples:
    - 2 professores (um dono da turma, outro sem nenhuma turma)
    - 1 turma vinculada ao primeiro professor
    - 2 alunos (1 matriculado na turma, 1 sem matrícula nenhuma)
    """

    session = banco_teste()

    usuario_prof = Usuario(
        nome="Maria Silva", email="maria@escola.example",
        senha=generate_password_hash("123"), tipo="professor",
    )
    usuario_outro_prof = Usuario(
        nome="João Santos", email="joao@escola.example",
        senha=generate_password_hash("123"), tipo="professor",
    )
    session.add_all([usuario_prof, usuario_outro_prof])
    session.flush()

    professor = Professor(nome="Maria Silva", email="maria@escola.example", id_usuario=usuario_prof.id)
    outro_professor = Professor(nome="João Santos", email="joao@escola.example", id_usuario=usuario_outro_prof.id)
    session.add_all([professor, outro_professor])
    session.flush()

    curso = Curso(nome_curso="Curso de Matemática", carga_horaria=120, id_professor=professor.id)
    session.add(curso)
    session.flush()

    disciplina = Disciplina(
        nome_disciplina="Álgebra", carga_horaria=60,
        id_curso=curso.id_curso, id_professor=professor.id,
    )
    session.add(disciplina)
    session.flush()

    turma = Turma(
        nome_turma="Álgebra - Manhã 2026/1", turno="Manhã", ano_letivo="2026/1",
        id_curso=curso.id_curso, id_disciplina=disciplina.id_disciplina, id_professor=professor.id,
    )
    session.add(turma)
    session.flush()

    aluno_matriculado = Aluno(nome="Ana Costa", email="ana@escola.example")
    aluno_sem_matricula = Aluno(nome="Bruno Lima", email="bruno@escola.example")
    session.add_all([aluno_matriculado, aluno_sem_matricula])
    session.flush()

    matricula = Matricula(
        data_matricula="2026-01-10", situacao="Ativa",
        id_aluno=aluno_matriculado.id, id_curso=curso.id_curso, id_turma=turma.id_turma,
    )
    session.add(matricula)
    session.commit()

    dados = {
        "id_usuario_professor": usuario_prof.id,
        "id_usuario_outro_professor": usuario_outro_prof.id,
        "id_turma": turma.id_turma,
        "id_aluno_matriculado": aluno_matriculado.id,
        "id_aluno_sem_matricula": aluno_sem_matricula.id,
    }

    session.close()

    return dados


# ==================================================
# DASHBOARD
# ==================================================

def test_dashboard_professor_retorna_resumo_correto(cenario):

    resultado = obter_dashboard_professor(cenario["id_usuario_professor"])

    assert resultado["nome"] == "Maria Silva"
    assert resultado["quantidade_turmas"] == 1
    assert resultado["total_alunos"] == 1


def test_dashboard_usuario_sem_professor_vinculado_nega_acesso(banco_teste):

    with pytest.raises(AcessoNegadoError):
        obter_dashboard_professor(9999)


# ==================================================
# MINHAS TURMAS
# ==================================================

def test_listar_turmas_retorna_apenas_do_professor_logado(cenario):

    turmas = listar_turmas_professor(cenario["id_usuario_professor"])

    assert len(turmas) == 1
    assert turmas[0]["nome_turma"] == "Álgebra - Manhã 2026/1"


def test_professor_sem_turmas_recebe_lista_vazia(cenario):

    turmas = listar_turmas_professor(cenario["id_usuario_outro_professor"])

    assert turmas == []


# ==================================================
# DETALHE DA TURMA
# ==================================================

def test_detalhe_turma_traz_alunos_matriculados(cenario):

    detalhe = obter_turma_detalhe(cenario["id_usuario_professor"], cenario["id_turma"])

    assert detalhe["nome_turma"] == "Álgebra - Manhã 2026/1"
    assert len(detalhe["alunos"]) == 1
    assert detalhe["alunos"][0]["nome"] == "Ana Costa"


def test_detalhe_turma_de_outro_professor_nega_acesso(cenario):

    with pytest.raises(AcessoNegadoError):
        obter_turma_detalhe(cenario["id_usuario_outro_professor"], cenario["id_turma"])


# ==================================================
# CADASTRO DE NOTA
# ==================================================

def test_cadastrar_nota_com_sucesso(cenario):

    resultado = cadastrar_nota_professor(cenario["id_usuario_professor"], {
        "id_turma": cenario["id_turma"],
        "id_aluno": cenario["id_aluno_matriculado"],
        "tipo_avaliacao": "Prova 1",
        "nota": 8.5,
    })

    assert resultado["nota"] == 8.5
    assert resultado["tipo_avaliacao"] == "Prova 1"


def test_cadastrar_nota_fora_da_faixa_gera_erro(cenario):

    with pytest.raises(ValueError):
        cadastrar_nota_professor(cenario["id_usuario_professor"], {
            "id_turma": cenario["id_turma"],
            "id_aluno": cenario["id_aluno_matriculado"],
            "tipo_avaliacao": "Prova 1",
            "nota": 15,
        })


def test_cadastrar_nota_aluno_nao_matriculado_nega_acesso(cenario):

    with pytest.raises(AcessoNegadoError):
        cadastrar_nota_professor(cenario["id_usuario_professor"], {
            "id_turma": cenario["id_turma"],
            "id_aluno": cenario["id_aluno_sem_matricula"],
            "tipo_avaliacao": "Prova 1",
            "nota": 8,
        })


def test_cadastrar_nota_em_turma_de_outro_professor_nega_acesso(cenario):

    with pytest.raises(AcessoNegadoError):
        cadastrar_nota_professor(cenario["id_usuario_outro_professor"], {
            "id_turma": cenario["id_turma"],
            "id_aluno": cenario["id_aluno_matriculado"],
            "tipo_avaliacao": "Prova 1",
            "nota": 8,
        })


# ==================================================
# REGISTRO DE PRESENÇA
# ==================================================

def test_registrar_presencas_com_sucesso(cenario):

    resultado = registrar_presencas_turma(cenario["id_usuario_professor"], {
        "id_turma": cenario["id_turma"],
        "data_aula": "2026-07-22",
        "periodo": "Manhã - 1º período",
        "presencas": [
            {"id_aluno": cenario["id_aluno_matriculado"], "situacao": "P"},
        ],
    })

    assert len(resultado) == 1
    assert resultado[0]["presente"] == "P"


def test_registrar_presencas_periodo_invalido_gera_erro(cenario):

    with pytest.raises(ValueError):
        registrar_presencas_turma(cenario["id_usuario_professor"], {
            "id_turma": cenario["id_turma"],
            "data_aula": "2026-07-22",
            "periodo": "Madrugada",
            "presencas": [
                {"id_aluno": cenario["id_aluno_matriculado"], "situacao": "P"},
            ],
        })


def test_registrar_presencas_situacao_invalida_gera_erro(cenario):

    with pytest.raises(ValueError):
        registrar_presencas_turma(cenario["id_usuario_professor"], {
            "id_turma": cenario["id_turma"],
            "data_aula": "2026-07-22",
            "periodo": "Manhã - 1º período",
            "presencas": [
                {"id_aluno": cenario["id_aluno_matriculado"], "situacao": "Z"},
            ],
        })


def test_registrar_presencas_lista_vazia_gera_erro(cenario):

    with pytest.raises(ValueError):
        registrar_presencas_turma(cenario["id_usuario_professor"], {
            "id_turma": cenario["id_turma"],
            "data_aula": "2026-07-22",
            "periodo": "Manhã - 1º período",
            "presencas": [],
        })


# ==================================================
# HISTÓRICOS
# ==================================================

def test_historico_de_notas_calcula_media(cenario):

    cadastrar_nota_professor(cenario["id_usuario_professor"], {
        "id_turma": cenario["id_turma"], "id_aluno": cenario["id_aluno_matriculado"],
        "tipo_avaliacao": "Prova 1", "nota": 7,
    })
    cadastrar_nota_professor(cenario["id_usuario_professor"], {
        "id_turma": cenario["id_turma"], "id_aluno": cenario["id_aluno_matriculado"],
        "tipo_avaliacao": "Prova 2", "nota": 9,
    })

    historico = historico_notas_aluno(
        cenario["id_usuario_professor"], cenario["id_turma"], cenario["id_aluno_matriculado"]
    )

    assert historico["media"] == 8.0
    assert len(historico["notas"]) == 2


def test_historico_de_presencas_calcula_frequencia(cenario):

    registrar_presencas_turma(cenario["id_usuario_professor"], {
        "id_turma": cenario["id_turma"], "data_aula": "2026-07-20",
        "periodo": "Manhã - 1º período",
        "presencas": [{"id_aluno": cenario["id_aluno_matriculado"], "situacao": "P"}],
    })
    registrar_presencas_turma(cenario["id_usuario_professor"], {
        "id_turma": cenario["id_turma"], "data_aula": "2026-07-21",
        "periodo": "Manhã - 1º período",
        "presencas": [{"id_aluno": cenario["id_aluno_matriculado"], "situacao": "F"}],
    })

    historico = historico_presencas_aluno(
        cenario["id_usuario_professor"], cenario["id_turma"], cenario["id_aluno_matriculado"]
    )

    assert historico["total_presencas"] == 1
    assert historico["total_faltas"] == 1
    assert historico["percentual_frequencia"] == 50.0


# ==================================================
# VALIDAÇÕES NOVAS
# ==================================================

def test_validar_periodo_valido_nao_gera_erro():
    validar_periodo("Manhã - 1º período")


def test_validar_periodo_invalido_gera_erro():
    with pytest.raises(ValueError):
        validar_periodo("Madrugada")


def test_validar_situacao_presenca_valida_nao_gera_erro():
    validar_situacao_presenca("P")


def test_validar_situacao_presenca_invalida_gera_erro():
    with pytest.raises(ValueError):
        validar_situacao_presenca("Z")