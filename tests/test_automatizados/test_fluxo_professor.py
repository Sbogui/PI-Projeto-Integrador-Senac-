import pytest
from werkzeug.security import generate_password_hash

from database import SessionLocal
from models import Usuario, Professor, Curso, Disciplina, Turma, Aluno, Matricula


EMAIL_PROFESSOR_TESTE = "professor.teste.classflow@escola.example"
SENHA_PROFESSOR_TESTE = "senha-teste-123"


@pytest.fixture
def cenario_professor():
    """
    Cria, no banco real do projeto, um professor de teste com uma turma
    e um aluno matriculado — e remove tudo ao final, sem afetar os
    dados já existentes.
    """

    session = SessionLocal()

    usuario = Usuario(
        nome="Professor Teste",
        email=EMAIL_PROFESSOR_TESTE,
        senha=generate_password_hash(SENHA_PROFESSOR_TESTE),
        tipo="professor",
    )
    session.add(usuario)
    session.flush()

    professor = Professor(
        nome="Professor Teste",
        email=EMAIL_PROFESSOR_TESTE,
        id_usuario=usuario.id,
    )
    session.add(professor)
    session.flush()

    curso = Curso(nome_curso="Curso Teste ClassFlow", carga_horaria=40, id_professor=professor.id)
    session.add(curso)
    session.flush()

    disciplina = Disciplina(
        nome_disciplina="Disciplina Teste", carga_horaria=20,
        id_curso=curso.id_curso, id_professor=professor.id,
    )
    session.add(disciplina)
    session.flush()

    turma = Turma(
        nome_turma="Turma Teste 2026/1", turno="Manhã", ano_letivo="2026/1",
        id_curso=curso.id_curso, id_disciplina=disciplina.id_disciplina, id_professor=professor.id,
    )
    session.add(turma)
    session.flush()

    aluno = Aluno(nome="Aluno Teste ClassFlow", email="aluno.teste.classflow@escola.example")
    session.add(aluno)
    session.flush()

    matricula = Matricula(
        data_matricula="2026-01-10", situacao="Ativa",
        id_aluno=aluno.id, id_curso=curso.id_curso, id_turma=turma.id_turma,
    )
    session.add(matricula)
    session.commit()

    ids = {
        "id_turma": turma.id_turma,
        "id_aluno": aluno.id,
    }

    session.close()

    yield ids

    # ===== Limpeza (ordem respeitando as dependências) =====
    session = SessionLocal()
    try:
        for modelo, id_obj in [
            (Matricula, matricula.id_matricula),
            (Turma, turma.id_turma),
            (Disciplina, disciplina.id_disciplina),
            (Curso, curso.id_curso),
            (Aluno, aluno.id),
            (Professor, professor.id),
            (Usuario, usuario.id),
        ]:
            obj = session.get(modelo, id_obj)
            if obj:
                session.delete(obj)
        session.commit()
    finally:
        session.close()


def login_professor(client):
    return client.post(
        "/login",
        data={"email": EMAIL_PROFESSOR_TESTE, "senha": SENHA_PROFESSOR_TESTE},
        follow_redirects=True,
    )


# ==================================================
# LOGIN
# ==================================================

def test_login_professor_acessa_o_painel(client, cenario_professor):

    resposta = login_professor(client)

    assert resposta.status_code == 200
    assert b"Painel do Professor" in resposta.data


def test_sem_login_nao_acessa_area_do_professor(client):

    resposta = client.get("/api/professor/dashboard", follow_redirects=False)

    assert resposta.status_code in (302, 401, 403)


# ==================================================
# DASHBOARD E TURMAS
# ==================================================

def test_dashboard_do_professor_logado(client, cenario_professor):

    login_professor(client)

    resposta = client.get("/api/professor/dashboard")

    assert resposta.status_code == 200
    assert resposta.json["nome"] == "Professor Teste"
    assert resposta.json["quantidade_turmas"] == 1


def test_professor_ve_apenas_suas_turmas(client, cenario_professor):

    login_professor(client)

    resposta = client.get("/api/professor/turmas")

    assert resposta.status_code == 200
    assert len(resposta.json) == 1
    assert resposta.json[0]["id_turma"] == cenario_professor["id_turma"]


def test_professor_abre_turma_e_ve_aluno_matriculado(client, cenario_professor):

    login_professor(client)

    resposta = client.get(f"/api/professor/turmas/{cenario_professor['id_turma']}")

    assert resposta.status_code == 200
    assert len(resposta.json["alunos"]) == 1
    assert resposta.json["alunos"][0]["nome"] == "Aluno Teste ClassFlow"


# ==================================================
# NOTAS
# ==================================================

def test_cadastro_de_nota_pelo_professor(client, cenario_professor):

    login_professor(client)

    resposta = client.post(
        "/api/professor/notas",
        json={
            "id_turma": cenario_professor["id_turma"],
            "id_aluno": cenario_professor["id_aluno"],
            "tipo_avaliacao": "Prova 1",
            "nota": 9,
        },
    )

    assert resposta.status_code == 201
    assert resposta.json["nota"] == 9


def test_cadastro_de_nota_invalida_retorna_mensagem_amigavel(client, cenario_professor):

    login_professor(client)

    resposta = client.post(
        "/api/professor/notas",
        json={
            "id_turma": cenario_professor["id_turma"],
            "id_aluno": cenario_professor["id_aluno"],
            "tipo_avaliacao": "Prova 1",
            "nota": 20,
        },
    )

    assert resposta.status_code == 400
    assert "0 e 10" in resposta.json["erro"]


def test_historico_de_notas_do_aluno(client, cenario_professor):

    login_professor(client)

    client.post(
        "/api/professor/notas",
        json={
            "id_turma": cenario_professor["id_turma"],
            "id_aluno": cenario_professor["id_aluno"],
            "tipo_avaliacao": "Prova 1",
            "nota": 8,
        },
    )

    resposta = client.get(
        f"/api/professor/turmas/{cenario_professor['id_turma']}"
        f"/alunos/{cenario_professor['id_aluno']}/notas"
    )

    assert resposta.status_code == 200
    assert resposta.json["media"] == 8.0


# ==================================================
# PRESENÇAS
# ==================================================

def test_cadastro_de_presenca_pelo_professor(client, cenario_professor):

    login_professor(client)

    resposta = client.post(
        "/api/professor/presencas",
        json={
            "id_turma": cenario_professor["id_turma"],
            "data_aula": "2026-07-22",
            "periodo": "Manhã - 1º período",
            "presencas": [
                {"id_aluno": cenario_professor["id_aluno"], "situacao": "P"},
            ],
        },
    )

    assert resposta.status_code == 201
    assert resposta.json[0]["presente"] == "P"


def test_cadastro_de_presenca_com_periodo_invalido(client, cenario_professor):

    login_professor(client)

    resposta = client.post(
        "/api/professor/presencas",
        json={
            "id_turma": cenario_professor["id_turma"],
            "data_aula": "2026-07-22",
            "periodo": "Madrugada",
            "presencas": [
                {"id_aluno": cenario_professor["id_aluno"], "situacao": "P"},
            ],
        },
    )

    assert resposta.status_code == 400


def test_historico_de_presencas_do_aluno(client, cenario_professor):

    login_professor(client)

    client.post(
        "/api/professor/presencas",
        json={
            "id_turma": cenario_professor["id_turma"],
            "data_aula": "2026-07-22",
            "periodo": "Manhã - 1º período",
            "presencas": [
                {"id_aluno": cenario_professor["id_aluno"], "situacao": "F"},
            ],
        },
    )

    resposta = client.get(
        f"/api/professor/turmas/{cenario_professor['id_turma']}"
        f"/alunos/{cenario_professor['id_aluno']}/presencas"
    )

    assert resposta.status_code == 200
    assert resposta.json["total_faltas"] == 1