import flask as fk
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from database import SessionLocal
from models import Usuario, Aluno, Professor
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from auth import login_required, role_required

from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
    redirect,
    session,
    url_for,
    flash
)

from servicos import (
    cadastrar_aluno,
    cadastrar_professor,
    cadastrar_curso,
    cadastrar_disciplina,
    cadastrar_matricula,
    cadastrar_nota,
    cadastrar_presenca,
    cadastrar_telefone,
    cadastrar_email,
    cadastrar_endereco,

    listar_alunos,
    listar_professores,
    listar_cursos,
    listar_disciplinas,
    listar_matriculas,
    listar_notas,
    listar_presencas,
    listar_telefones,
    listar_emails,
    listar_enderecos,
    
    atualizar_professor,
    excluir_professor,
    atualizar_aluno,
    excluir_aluno,
    atualizar_curso,
    excluir_curso,
    atualizar_disciplina,
    excluir_disciplina,
    atualizar_matricula,
    excluir_matricula,
    atualizar_nota,
    excluir_nota,
    atualizar_presenca,
    excluir_presenca,
    atualizar_telefone,
    excluir_telefone,
    atualizar_email,
    excluir_email,
    atualizar_endereco,
    excluir_endereco,
)


bp = fk.Blueprint("api", __name__, url_prefix="/api")


def _erro(mensagem, status=400):
    return fk.jsonify({"erro": mensagem}), status


# ==================================================
# PROFESSORES
# ==================================================

@bp.get("/professores")
@login_required
@role_required("admin")
def professores():
    return fk.jsonify(listar_professores())


@bp.post("/professores")
@login_required
@role_required("admin")
def criar_professor():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_professor(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Já existe um professor com este e-mail.", 409)

@bp.put("/professores/<int:id>")
@login_required
@role_required("admin")
def put_professor(id):

    dados = fk.request.get_json()

    professor = atualizar_professor(id, dados)

    if not professor:
        return _erro("Professor não encontrado", 404)

    return fk.jsonify(professor)


@bp.delete("/professores/<int:id>")
@login_required
@role_required("admin")
def delete_professor(id):

    sucesso = excluir_professor(id)

    if not sucesso:
        return _erro("Professor não encontrado", 404)

    return fk.jsonify({
        "mensagem": "Professor excluído"
    })
# ==================================================
# ALUNOS
# ==================================================

@bp.get("/alunos")
@login_required
@role_required("admin", "professor")
def alunos():
    return fk.jsonify(listar_alunos())


@bp.post("/alunos")
@login_required
@role_required("admin")
def criar_aluno():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_aluno(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Já existe um aluno com este e-mail.", 409)

@bp.put("/alunos/<int:id>")
@login_required
@role_required("admin")
def put_aluno(id):

    dados = fk.request.get_json()

    aluno = atualizar_aluno(id, dados)

    if not aluno:
        return _erro("Aluno não encontrado", 404)

    return fk.jsonify(aluno)


@bp.delete("/alunos/<int:id>")
@login_required
@role_required("admin")
def delete_aluno(id):

    sucesso = excluir_aluno(id)

    if not sucesso:
        return _erro("Aluno não encontrado", 404)

    return fk.jsonify({
        "mensagem": "Aluno excluído"
    })
# ==================================================
# CURSOS
# ==================================================

@bp.get("/cursos")
@login_required
def cursos():
    return fk.jsonify(listar_cursos())


@bp.post("/cursos")
@login_required
@role_required("admin")
def criar_curso():

    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_curso(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Erro ao cadastrar curso.", 409)
    
@bp.put("/cursos/<int:id>")
@login_required
@role_required("admin")
def put_curso(id):

    dados = fk.request.get_json()

    curso = atualizar_curso(id, dados)

    if not curso:
        return _erro("Curso não encontrado", 404)

    return fk.jsonify(curso)

@bp.delete("/cursos/<int:id>")
@login_required
@role_required("admin")
def delete_curso(id):

    sucesso = excluir_curso(id)

    if not sucesso:
        return _erro("Curso não encontrado", 404)

    return fk.jsonify({
        "mensagem": "Curso excluído"
    })
# ==================================================
# DISCIPLINAS
# ==================================================

@bp.get("/disciplinas")
@login_required
def disciplinas():
    return fk.jsonify(listar_disciplinas())


@bp.post("/disciplinas")
@login_required
@role_required("admin")
def criar_disciplina():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_disciplina(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Erro ao cadastrar disciplina.", 409)

@bp.put("/disciplinas/<int:id>")
@login_required
@role_required("admin")
def put_disciplina(id):

    dados = fk.request.get_json()

    disciplina = atualizar_disciplina(id, dados)

    if not disciplina:
        return _erro("Disciplina não encontrada", 404)

    return fk.jsonify(disciplina)


@bp.delete("/disciplinas/<int:id>")
@login_required
@role_required("admin")
def delete_disciplina(id):

    sucesso = excluir_disciplina(id)

    if not sucesso:
        return _erro("Disciplina não encontrada", 404)

    return fk.jsonify({
        "mensagem": "Disciplina excluída"
    })
# ==================================================
# MATRICULAS
# ==================================================

@bp.get("/matriculas")
@login_required
@role_required("admin", "professor")
def matriculas():
    return fk.jsonify(listar_matriculas())


@bp.post("/matriculas")
@login_required
@role_required("admin")
def criar_matricula():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_matricula(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Erro ao cadastrar matrícula.", 409)


@bp.put("/matriculas/<int:id>")
@login_required
@role_required("admin")
def put_matricula(id):

    dados = fk.request.get_json()

    matricula = atualizar_matricula(id, dados)

    if not matricula:
        return _erro("Matrícula não encontrada", 404)

    return fk.jsonify(matricula)


@bp.delete("/matriculas/<int:id>")
@login_required
@role_required("admin")
def delete_matricula(id):

    sucesso = excluir_matricula(id)

    if not sucesso:
        return _erro("Matrícula não encontrada", 404)

    return fk.jsonify({
        "mensagem": "Matrícula excluída"
    })

# ==================================================
# NOTAS
# ==================================================

@bp.get("/notas")
@login_required
@role_required("admin", "professor")
def notas():
    return fk.jsonify(listar_notas())


@bp.post("/notas")
@login_required
@role_required("admin", "professor")
def criar_nota():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_nota(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Erro ao cadastrar nota.", 409)

@bp.put("/notas/<int:id>")
@login_required
@role_required("admin", "professor")
def put_nota(id):

    dados = fk.request.get_json()

    nota = atualizar_nota(id, dados)

    if not nota:
        return _erro("Nota não encontrada", 404)

    return fk.jsonify(nota)


@bp.delete("/notas/<int:id>")
@login_required
@role_required("admin")
def delete_nota(id):

    sucesso = excluir_nota(id)

    if not sucesso:
        return _erro("Nota não encontrada", 404)

    return fk.jsonify({
        "mensagem": "Nota excluída"
    })
# ==================================================
# PRESENCAS
# ==================================================

@bp.get("/presencas")
@login_required
@role_required("admin", "professor")
def presencas():
    return fk.jsonify(listar_presencas())

@bp.post("/presencas")
@login_required
@role_required("admin", "professor")
def criar_presenca():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_presenca(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Erro ao cadastrar presença.", 409)

@bp.put("/presencas/<int:id>")
@login_required
@role_required("admin", "professor")
def put_presenca(id):

    dados = fk.request.get_json()

    presenca = atualizar_presenca(id, dados)

    if not presenca:
        return _erro("Presença não encontrada", 404)

    return fk.jsonify(presenca)


@bp.delete("/presencas/<int:id>")
@login_required
@role_required("admin")
def delete_presenca(id):

    sucesso = excluir_presenca(id)

    if not sucesso:
        return _erro("Presença não encontrada", 404)

    return fk.jsonify({
        "mensagem": "Presença excluída"
    })
# ==================================================
# TELEFONES
# ==================================================

@bp.get("/telefones")
@login_required
@role_required("admin")
def telefones():
    return fk.jsonify(listar_telefones())


@bp.post("/telefones")
@login_required
@role_required("admin")
def criar_telefone():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_telefone(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Erro ao cadastrar telefone.", 409)


@bp.put("/telefones/<int:id>")
@login_required
@role_required("admin")
def put_telefone(id):

    dados = fk.request.get_json()

    telefone = atualizar_telefone(id, dados)

    if not telefone:
        return _erro("Telefone não encontrado", 404)

    return fk.jsonify(telefone)


@bp.delete("/telefones/<int:id>")
@login_required
@role_required("admin")
def delete_telefone(id):

    sucesso = excluir_telefone(id)

    if not sucesso:
        return _erro("Telefone não encontrado", 404)

    return fk.jsonify({
        "mensagem": "Telefone excluído"
    })
# ==================================================
# EMAILS
# ==================================================

@bp.get("/emails")
@login_required
@role_required("admin")
def emails():
    return fk.jsonify(listar_emails())


@bp.post("/emails")
@login_required
@role_required("admin")
def criar_email():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_email(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Erro ao cadastrar email.", 409)
    
@bp.put("/emails/<int:id>")
@login_required
@role_required("admin")
def put_email(id):

    dados = fk.request.get_json()

    email = atualizar_email(id, dados)

    if not email:
        return _erro("Email não encontrado", 404)

    return fk.jsonify(email)


@bp.delete("/emails/<int:id>")
@login_required
@role_required("admin")
def delete_email(id):

    sucesso = excluir_email(id)

    if not sucesso:
        return _erro("Email não encontrado", 404)

    return fk.jsonify({
        "mensagem": "Email excluído"
    })

# ==================================================
# ENDERECOS
# ==================================================

@bp.get("/enderecos")
@login_required
@role_required("admin")
def enderecos():
    return fk.jsonify(listar_enderecos())


@bp.post("/enderecos")
@login_required
@role_required("admin")
def criar_endereco():
    dados = fk.request.get_json(silent=True) or {}

    try:
        return fk.jsonify(cadastrar_endereco(dados)), 201

    except ValueError as exc:
        return _erro(str(exc))

    except IntegrityError:
        return _erro("Erro ao cadastrar endereço.", 409)


@bp.put("/enderecos/<int:id>")
@login_required
@role_required("admin")
def put_endereco(id):

    dados = fk.request.get_json()

    endereco = atualizar_endereco(id, dados)

    if not endereco:
        return _erro("Endereço não encontrado", 404)

    return fk.jsonify(endereco)


@bp.delete("/enderecos/<int:id>")
@login_required
@role_required("admin")
def delete_endereco(id):

    sucesso = excluir_endereco(id)

    if not sucesso:
        return _erro("Endereço não encontrado", 404)

    return fk.jsonify({
        "mensagem": "Endereço excluído"
    })
# ==================================================
# PAGINAS
# ==================================================

paginas = fk.Blueprint("paginas", __name__)

@paginas.route("/")
@login_required
def home():

    if "usuario" not in session:
        return redirect(url_for("paginas.login"))

    return render_template("index.html")


@paginas.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        session.clear()

        email = request.form.get("email")
        senha = request.form.get("senha")

        db = SessionLocal()

        usuario = db.scalar(
        select(Usuario).where(
         Usuario.email == email
        )
    )

        db.close()

        if usuario and check_password_hash(usuario.senha, senha):
            
            session["usuario_id"] = usuario.id
            session["usuario"] = usuario.nome
            session["tipo"] = usuario.tipo

            if usuario.tipo == "admin":
                return redirect(url_for("paginas.home"))

            elif usuario.tipo == "professor":
                return redirect(url_for("paginas.professor"))

            elif usuario.tipo == "aluno":
                return redirect(url_for("paginas.aluno"))

        flash("Email ou senha inválidos")

    return render_template("login.html")

@paginas.route("/admin")
@login_required
@role_required("admin")
def admin():

    if "usuario" not in session:
        return redirect(url_for("paginas.login"))

    if session["tipo"] != "admin":
        return "Acesso negado"

    return render_template("admin.html")

@paginas.route("/professor")
@login_required
@role_required("professor")
def professor():

    if "usuario" not in session:
        return redirect(url_for("paginas.login"))

    if session["tipo"] != "professor":
        return "Acesso negado"

    return render_template("professor.html")


@paginas.route("/aluno")
@login_required
@role_required("aluno")
def aluno():

    if "usuario" not in session:
        return redirect(url_for("paginas.login"))

    if session["tipo"] != "aluno":
        return "Acesso negado"

    return render_template("aluno.html")


@paginas.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("paginas.login"))


@paginas.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")
        tipo = request.form.get("tipo")

        if not nome or not email or not senha or not tipo:
            flash("Preencha todos os campos")
            return redirect(url_for("paginas.cadastro"))

        if senha != confirmar_senha:
            flash("As senhas não conferem")
            return redirect(url_for("paginas.cadastro"))

        db = SessionLocal()

        try:
            usuario_existente = db.scalar(
                select(Usuario).where(Usuario.email == email)
            )

            if usuario_existente:
                flash("Email já cadastrado")
                return redirect(url_for("paginas.cadastro"))

            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha=generate_password_hash(senha),
                tipo=tipo
            )

            db.add(novo_usuario)
            db.flush()

            if tipo == "aluno":
                db.add(Aluno(nome=nome, email=email, id_usuario=novo_usuario.id))

            elif tipo == "professor":
                db.add(Professor(nome=nome, email=email, id_usuario=novo_usuario.id))

            db.commit()

            flash("Usuário criado com sucesso")
            return redirect(url_for("paginas.login"))

        except Exception as e:
            db.rollback()
            flash("Erro ao criar usuário")
            print("ERRO CADASTRO:", e)

        finally:
            db.close()

    return render_template("cadastro.html")

@paginas.route("/recuperar-senha")
def recuperar_senha():

    return "Página de recuperação de senha em desenvolvimento"

