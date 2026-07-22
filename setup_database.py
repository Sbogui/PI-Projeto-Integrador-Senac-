"""
Script didático: DDL (create/drop tables) + DML (inserts) com sessão explícita.
Execute na raiz do projeto: python setup_database.py
"""

from sqlalchemy import func, select

from database import Base, SessionLocal, engine
import models  # noqa: F401 — registra tabelas no metadata
from models import Usuario
from werkzeug.security import generate_password_hash


def populate_database():
    print("=" * 50)
    print("Limpando e criando tabelas...")
    print("=" * 50)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    


    admin = Usuario(
    nome="Administrador",
    email="admin@gmail.com",
    senha=generate_password_hash("123"),
    tipo="admin"
    )

    professor_usuario = Usuario(
    nome="Professor",
    email="prof@gmail.com",
    senha=generate_password_hash("123"),
    tipo="professor"
    )

    aluno = Usuario(
    nome="Aluno",
    email="aluno@gmail.com",
    senha=generate_password_hash("123"),
    tipo="aluno"
    )

    session.add_all([
    admin,
    professor_usuario,
    aluno
])

    session.flush()

    try:

        # ==================================================
        # PROFESSORES
        # ==================================================

        print("Inserindo professores...")

        professores = [
            models.Professor(
                nome="Maria Silva",
                email="maria@escola.example",
                disciplina="Matemática",
                # Vinculado ao usuário de login "Professor" (prof@gmail.com),
                # para que o login de demonstração acesse a Área do Professor
                # já com turmas, alunos e histórico populados.
                id_usuario=professor_usuario.id,
            ),
            models.Professor(
                nome="João Santos",
                email="joao.santos@escola.example",
                disciplina="Português",
            ),
            models.Professor(
                nome="Fernanda Oliveira",
                email="fernanda@escola.example",
                disciplina="Física",
            ),
            
        ]
        

        session.add_all(professores)
        session.flush()


        # ==================================================
        # CURSOS
        # ==================================================

        print("Inserindo cursos...")

        cursos = [
            models.Curso(
                nome_curso="Curso de Matemática",
                carga_horaria=120,
            ),
            models.Curso(
                nome_curso="Curso de Física",
                carga_horaria=100,
            ),
            models.Curso(
                nome_curso="Curso de Português",
                carga_horaria=80,
            ),
        ]

        session.add_all(cursos)
        session.flush()

        # ==================================================
        # DISCIPLINAS
        # ==================================================

        print("Inserindo disciplinas...")

        disciplinas = [
            models.Disciplina(
                nome_disciplina="Álgebra",
                carga_horaria=60,
                id_curso=cursos[0].id_curso,
                id_professor=professores[0].id,
            ),

            models.Disciplina(
                nome_disciplina="Mecânica",
                carga_horaria=50,
                id_curso=cursos[1].id_curso,
                id_professor=professores[2].id,
            ),

            models.Disciplina(
                nome_disciplina="Gramática",
                carga_horaria=40,
                id_curso=cursos[2].id_curso,
                id_professor=professores[1].id,
            ),
        ]

        session.add_all(disciplinas)
        session.flush() 

        # ==================================================
        # TURMAS
        # ==================================================

        print("Inserindo turmas...")

        turmas = [
            models.Turma(
                nome_turma="Álgebra - Manhã 2026/1",
                turno="Manhã",
                ano_letivo="2026/1",
                id_curso=cursos[0].id_curso,
                id_disciplina=disciplinas[0].id_disciplina,
                id_professor=professores[0].id,
            ),
            models.Turma(
                nome_turma="Mecânica - Tarde 2026/1",
                turno="Tarde",
                ano_letivo="2026/1",
                id_curso=cursos[1].id_curso,
                id_disciplina=disciplinas[1].id_disciplina,
                id_professor=professores[2].id,
            ),
            models.Turma(
                nome_turma="Gramática - Noite 2026/1",
                turno="Noite",
                ano_letivo="2026/1",
                id_curso=cursos[2].id_curso,
                id_disciplina=disciplinas[2].id_disciplina,
                id_professor=professores[1].id,
            ),
        ]

        session.add_all(turmas)
        session.flush()
        
        # ==================================================
        # ALUNOS
        # ==================================================

        print("Inserindo alunos...")

        alunos = [
            models.Aluno(
                nome="Ana Costa",
                email="ana@escola.example",
                data_nascimento="2005-03-10",
                telefone="51999990001",
               
            ),
            models.Aluno(
                nome="Bruno Lima",
                email="bruno@escola.example",
                data_nascimento="2004-07-21",
                telefone="51999990002",
                
            ),
            models.Aluno(
                nome="Carla Dias",
                email="carla@escola.example",
                data_nascimento="2005-01-15",
                telefone="51999990003",
                
            ),
            models.Aluno(
                nome="Diego Rocha",
                email="diego@escola.example",
                data_nascimento="2004-11-02",
                telefone="51999990004",
                
            ),
        ]

        session.add_all(alunos)
        session.flush()
        
        # ==================================================
        # MATRÍCULAS
        # ==================================================

        print("Inserindo matrículas...")

        matriculas = [
            models.Matricula(
                data_matricula="2026-01-10",
                situacao="Ativa",
                id_aluno=alunos[0].id,
                id_curso=cursos[0].id_curso,
                id_turma=turmas[0].id_turma,
            ),
            models.Matricula(
                data_matricula="2026-01-12",
                situacao="Ativa",
                id_aluno=alunos[2].id,
                id_curso=cursos[1].id_curso,
                id_turma=turmas[1].id_turma,
            ),
        ]

        session.add_all(matriculas)
        session.flush()

        # ==================================================
        # EMAILS
        # ==================================================

        print("Inserindo emails...")

        emails = [
            models.Email(
                email_pessoal="ana@gmail.com",
                email_profissional="ana@empresa.com",
                id_aluno=alunos[0].id,
                id_professor=professores[0].id,
            ),

            models.Email(
                email_pessoal="bruno@gmail.com",
                email_profissional="bruno@empresa.com",
                id_aluno=alunos[1].id,
                id_professor=professores[1].id,
            ),

            models.Email(
                email_pessoal="carla@gmail.com",
                email_profissional="carla@empresa.com",
                id_aluno=alunos[2].id,
                id_professor=professores[2].id,
            ),

            models.Email(
                email_pessoal="diego@gmail.com",
                email_profissional="diego@empresa.com",
                id_aluno=alunos[3].id,
                id_professor=professores[0].id,
            ),
        ]

        session.add_all(emails)

        # ==================================================
        # ENDEREÇOS
        # ==================================================

        print("Inserindo endereços...")

        enderecos = [
            models.Endereco(
                rua="Rua A",
                numero="100",
                bairro="Centro",
                cidade="Santa Cruz do Sul",
                cep="96800-000",
                estado="RS",
                complemento="Apto 101",
                id_aluno=alunos[0].id,
                id_professor=professores[0].id,
            ),
            models.Endereco(
                rua="Rua B",
                numero="200",
                bairro="Universitário",
                cidade="Santa Cruz do Sul",
                cep="96815-000",
                estado="RS",
                complemento="Casa",
                id_aluno=alunos[1].id,
                id_professor=professores[1].id,
            ),
        ]

        session.add_all(enderecos)


        # ==================================================
        # NOTAS
        # ==================================================

        print("Inserindo notas...")

        notas = [
            models.Nota(
                nota=9,
                tipo_avaliacao="Prova",
                id_aluno=alunos[0].id,
                id_disciplina=disciplinas[0].id_disciplina,
                id_professor=professores[0].id,
                id_turma=turmas[0].id_turma,
            ),
            models.Nota(
                nota=8,
                tipo_avaliacao="Trabalho",
                id_aluno=alunos[2].id,
                id_disciplina=disciplinas[1].id_disciplina,
                id_professor=professores[2].id,
                id_turma=turmas[1].id_turma,
            ),
        ]

        session.add_all(notas)

        # ==================================================
        # PRESENÇAS
        # ==================================================

        print("Inserindo presenças...")

        presencas = [
            models.Presenca(
                data_aula="2026-03-01",
                presente="S",
                periodo="Manhã - 1º período",
                id_matricula=matriculas[0].id_matricula,
                id_aluno=alunos[0].id,
                id_disciplina=disciplinas[0].id_disciplina,
                id_professor=professores[0].id,
                id_turma=turmas[0].id_turma,
            ),
            models.Presenca(
                data_aula="2026-03-02",
                presente="N",
                periodo="Tarde - 1º período",
                id_matricula=matriculas[1].id_matricula,
                id_aluno=alunos[2].id,
                id_disciplina=disciplinas[1].id_disciplina,
                id_professor=professores[2].id,
                id_turma=turmas[1].id_turma,
            ),
        ]

        session.add_all(presencas)

        # ==================================================
        # TELEFONES
        # ==================================================

        print("Inserindo telefones...")

        telefones = [
            models.Telefone(
                numero_pessoal="51999990001",
                numero_profissional="5133334444",
                id_aluno=alunos[0].id,
                id_professor=professores[0].id,
            ),

            models.Telefone(
                numero_pessoal="51999990002",
                numero_profissional="5133335555",
                id_aluno=alunos[1].id,
                id_professor=professores[1].id,
            ),

            models.Telefone(
                numero_pessoal="51999990003",
                numero_profissional="5133336666",
                id_aluno=alunos[2].id,
                id_professor=professores[2].id,
            ),

            models.Telefone(
                numero_pessoal="51999990004",
                numero_profissional="5133337777",
                id_aluno=alunos[3].id,
                id_professor=professores[0].id,
            ),
        ]

        session.add_all(telefones)

        # ==================================================
        # COMMIT
        # ==================================================

        session.commit()

        print("\nBanco populado com sucesso!")
        print("=" * 50)

        np = session.scalar(
            select(func.count()).select_from(models.Professor)
        )

        na = session.scalar(
            select(func.count()).select_from(models.Aluno)
        )

        nc = session.scalar(
            select(func.count()).select_from(models.Curso)
        )

        nd = session.scalar(
            select(func.count()).select_from(models.Disciplina)
        )

        nt = session.scalar(
            select(func.count()).select_from(models.Turma)
        )

        print(f"Professores : {np}")
        print(f"Alunos      : {na}")
        print(f"Cursos      : {nc}")
        print(f"Disciplinas : {nd}")
        print(f"Turmas      : {nt}")

        print("=" * 50)

    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    populate_database()