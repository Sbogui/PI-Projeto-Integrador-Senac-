from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base




class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)

    nome = Column(String(100), nullable=False)

    email = Column(String(120), unique=True, nullable=False)

    senha = Column(String(120), nullable=False)

    tipo = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo
        }

class Professor(Base):
    __tablename__ = "professores"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True)
    disciplina = Column(String(100))

    telefones = relationship(
        "Telefone",
        cascade="all, delete-orphan",
        back_populates="professor",
         passive_deletes=True
    )
    emails = relationship(
        "Email",
        cascade="all, delete-orphan",
        back_populates="professor",
         passive_deletes=True
    )
    enderecos = relationship(
        "Endereco",
        cascade="all, delete-orphan",
        back_populates="professor",
         passive_deletes=True
    )
    disciplinas = relationship(
        "Disciplina",
        back_populates="professor",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    cursos = relationship(
    "Curso",
    back_populates="professor"
)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "disciplina": self.disciplina,
        }


class Aluno(Base):
    __tablename__ = "alunos"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True)
    data_nascimento = Column(String(10))
    telefone = Column(String(15))
    curso_id = Column(Integer, ForeignKey("cursos.id_curso", ondelete="CASCADE"))

    curso = relationship("Curso", back_populates="alunos")

    telefones = relationship(
        "Telefone",
        cascade="all, delete-orphan",
        back_populates="aluno",
         passive_deletes=True
    )
    emails = relationship(
        "Email",
        cascade="all, delete-orphan",
        back_populates="aluno",
        passive_deletes=True
    )
    enderecos = relationship(
        "Endereco",
        cascade="all, delete-orphan",
        back_populates="aluno",
         passive_deletes=True
    )
    matriculas = relationship(
        "Matricula",
        back_populates="aluno",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    notas = relationship(
        "Nota",
        back_populates="aluno",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    presencas = relationship(
        "Presenca",
        back_populates="aluno",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "data_nascimento": self.data_nascimento,
            "telefone": self.telefone,
            "curso": (
                self.curso.nome_curso
                if self.curso else "—"
            ),
        }


class Curso(Base):
    __tablename__ = "cursos"
    __table_args__ = {"sqlite_autoincrement": True}

    id_curso = Column(Integer, primary_key=True, autoincrement=True)
    nome_curso = Column(String(100))
    carga_horaria = Column(Integer)
    id_professor = Column(Integer, ForeignKey("professores.id"))

    professor = relationship(
        "Professor",
        back_populates="cursos"
    )
    alunos = relationship(
        "Aluno",
        back_populates="curso",
        cascade="all, delete"
    )
    disciplinas = relationship(
        "Disciplina",
        back_populates="curso",
        cascade="all, delete"
    )
    matriculas = relationship(
        "Matricula",
        back_populates="curso",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def to_dict(self):
        return {
            "id_curso": self.id_curso,
            "nome_curso": self.nome_curso,
            "carga_horaria": self.carga_horaria,

            "professor": (
                self.professor.nome
                if self.professor else "—"
            ),

            "disciplinas": ", ".join(
                [
                    disciplina.nome_disciplina
                    for disciplina in self.disciplinas
                ]
            ) if self.disciplinas else "—",
        }


class Disciplina(Base):
    __tablename__ = "disciplinas"
    __table_args__ = {"sqlite_autoincrement": True}

    id_disciplina = Column(Integer, primary_key=True, autoincrement=True)
    nome_disciplina = Column(String(40))
    carga_horaria = Column(Integer)

    id_curso = Column(Integer, ForeignKey("cursos.id_curso", ondelete="CASCADE"))
    id_professor = Column(Integer, ForeignKey("professores.id", ondelete="CASCADE"))

    curso = relationship("Curso", back_populates="disciplinas")

    professor = relationship(
        "Professor",
        back_populates="disciplinas", 
        passive_deletes=True
    )

    notas = relationship(
        "Nota",
        back_populates="disciplina",
        cascade="all, delete-orphan", 
        passive_deletes=True
    )

    presencas = relationship(
        "Presenca",
        back_populates="disciplina",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
   

    def to_dict(self):
        return {
            "id_disciplina": self.id_disciplina,
            "nome_disciplina": self.nome_disciplina,
            "carga_horaria": self.carga_horaria,

            "curso": (
                self.curso.nome_curso
                if self.curso else "—"
            ),

            "professor": (
                self.professor.nome
                if self.professor else "—"
            ),
        }


class Email(Base):
    __tablename__ = "email"
    __table_args__ = {"sqlite_autoincrement": True}

    id_email = Column(Integer, primary_key=True, autoincrement=True)
    email_pessoal = Column(String(50), nullable=False)
    email_profissional = Column(String(50), nullable=False)

    id_aluno = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"))
    id_professor = Column(Integer, ForeignKey("professores.id", ondelete="CASCADE"))

    aluno = relationship("Aluno", back_populates="emails", passive_deletes=True)
    professor = relationship("Professor", back_populates="emails", passive_deletes=True)

    def to_dict(self):
        return {
            "id_email": self.id_email,
            "email_pessoal": self.email_pessoal,
            "email_profissional": self.email_profissional,
            "id_aluno": self.id_aluno,
            "id_professor": self.id_professor,
        }


class Endereco(Base):
    __tablename__ = "endereco"
    __table_args__ = {"sqlite_autoincrement": True}

    id_endereco = Column(Integer, primary_key=True, autoincrement=True)

    rua = Column(String(100))
    numero = Column(String(10))
    bairro = Column(String(50))
    cidade = Column(String(50))
    cep = Column(String(10))
    estado = Column(String(2))
    complemento = Column(String(50))

    id_aluno = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"))
    id_professor = Column(Integer, ForeignKey("professores.id", ondelete="CASCADE"))

    aluno = relationship("Aluno", back_populates="enderecos", passive_deletes=True)
    professor = relationship("Professor", back_populates="enderecos", passive_deletes=True)

    def to_dict(self):
        return {
            "id_endereco": self.id_endereco,
            "rua": self.rua,
            "numero": self.numero,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "cep": self.cep,
            "estado": self.estado,
            "complemento": self.complemento,
            "id_aluno": self.id_aluno,
            "id_professor": self.id_professor,
        }


class Matricula(Base):
    __tablename__ = "matricula"
    __table_args__ = {"sqlite_autoincrement": True}

    

    id_matricula = Column(Integer, primary_key=True, autoincrement=True)
    data_matricula = Column(String(10))
    situacao = Column(String(20))

    id_aluno = Column(Integer, ForeignKey("alunos.id",ondelete="CASCADE"))
    id_curso = Column(Integer, ForeignKey("cursos.id_curso",ondelete="CASCADE"))
    
    aluno = relationship(
        "Aluno",
        back_populates="matriculas",
        passive_deletes=True
    )

    curso = relationship(
        "Curso",
        back_populates="matriculas",
        passive_deletes=True
    )

    presencas = relationship(
        "Presenca",
        back_populates="matricula",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def to_dict(self):
        return {
            "id_matricula": self.id_matricula,
            "data_matricula": self.data_matricula,
            "situacao": self.situacao,

            "aluno": (
                self.aluno.nome
                if self.aluno else "—"
            ),

            "curso": (
                self.curso.nome_curso
                if self.curso else "—"
            ),
        }


class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = {"sqlite_autoincrement": True}


    id_nota = Column(Integer, primary_key=True, autoincrement=True)
    nota = Column(Integer)
    tipo_avaliacao = Column(String(50))

    id_aluno = Column(Integer, ForeignKey("alunos.id",ondelete="CASCADE"))
    id_disciplina = Column(Integer, ForeignKey("disciplinas.id_disciplina",ondelete="CASCADE"))
    
    aluno = relationship(
        "Aluno",
        back_populates="notas",
        passive_deletes=True
    )

    disciplina = relationship(
        "Disciplina",
        back_populates="notas",
        passive_deletes=True
    )
    

    def to_dict(self):
        return {
            "id_nota": self.id_nota,
            "nota": self.nota,
            "tipo_avaliacao": self.tipo_avaliacao,

            "aluno": (
                self.aluno.nome
                if self.aluno else "—"
            ),

            "disciplina": (
                self.disciplina.nome_disciplina
                if self.disciplina else "—"
            ),
        }

class Presenca(Base):
    __tablename__ = "presenca"
    __table_args__ = {"sqlite_autoincrement": True}

    

    id_presenca = Column(Integer, primary_key=True, autoincrement=True)
    data_aula = Column(String(12))
    presente = Column(String(1))

    id_matricula = Column(Integer, ForeignKey("matricula.id_matricula",ondelete="CASCADE"))
    id_aluno = Column(Integer, ForeignKey("alunos.id",ondelete="CASCADE"))
    id_disciplina = Column(Integer, ForeignKey("disciplinas.id_disciplina",ondelete="CASCADE"))
    
    aluno = relationship(
        "Aluno",
        back_populates="presencas",
        passive_deletes=True
    )

    disciplina = relationship(
        "Disciplina",
        back_populates="presencas",
        passive_deletes=True
    )

    matricula = relationship(
        "Matricula",
        back_populates="presencas",
        passive_deletes=True
    )

   

    def to_dict(self):
        return {
            "id_presenca": self.id_presenca,
            "data_aula": self.data_aula,
            "presente": self.presente,

            "aluno": (
                self.aluno.nome
                if self.aluno else "—"
            ),

            "disciplina": (
                self.disciplina.nome_disciplina
                if self.disciplina else "—"
            ),
        }


class Telefone(Base):
    __tablename__ = "telefone"
    __table_args__ = {"sqlite_autoincrement": True}

    id_telefone = Column(Integer, primary_key=True, autoincrement=True)
    numero_pessoal = Column(String(15))
    numero_profissional = Column(String(15))

    id_aluno = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"))
    id_professor = Column(Integer, ForeignKey("professores.id", ondelete="CASCADE"))

    aluno = relationship("Aluno", back_populates="telefones", passive_deletes=True)
    professor = relationship("Professor", back_populates="telefones", passive_deletes=True)

    def to_dict(self):
        return {
            "id_telefone": self.id_telefone,
            "numero_pessoal": self.numero_pessoal,
            "numero_profissional": self.numero_profissional,
            "id_aluno": self.id_aluno,
            "id_professor": self.id_professor,
        }