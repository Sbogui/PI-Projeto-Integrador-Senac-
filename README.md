# Sistema Escolar API — Flask + SQLAlchemy + SQLite

Projeto acadêmico desenvolvido com Python utilizando Flask, SQLAlchemy e SQLite para gerenciamento de:

- Alunos
- Professores
- Cursos
- Disciplinas
- Matrículas
- Notas
- Presenças
- Telefones
- Emails
- Endereços

---

# Tecnologias Utilizadas

- Python 3
- Flask
- SQLAlchemy
- SQLite
- HTML5
- CSS3
- JavaScript

---

# Estrutura do Projeto

```bash
projetoExemploPython/
│
├── app/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   └── routes.py
│
├── database.py
├── models.py
├── servicos.py
├── setup_database.py
├── requirements.txt
├── run.py
└── README.md
```

---

# Funcionalidades

## Professores
- Cadastro
- Listagem
- Associação com disciplinas

## Cursos
- Cadastro
- Associação com disciplinas

## Disciplinas
- Cadastro
- Associação com professores

## Alunos
- Cadastro
- Associação com cursos

## Matrículas
- Controle de vínculo entre aluno e disciplina

## Notas e Presenças
- Registro acadêmico completo

---

# Instalação

## 1. Clonar repositório

```bash
git clone https://github.com/Sbogui/PI-Projeto-Integrador-Senac-.git
```

## 2. Entrar na pasta

```bash
cd PI-Projeto-Integrador-Senac-
```

## 3. Criar ambiente virtual

### Windows
```bash
python -m venv .venv
```

### Linux/Mac
```bash
python3 -m venv .venv
```

---

# Ativar Ambiente Virtual

### Windows
```bash
.venv\Scripts\activate
```

### Linux/Mac
```bash
source .venv/bin/activate
```

---

# Instalar Dependências

```bash
pip install -r requirements.txt
```

---

# Criar Banco de Dados

```bash
python setup_database.py
```

---

# Executar Projeto

```bash
python run.py
```

A aplicação estará disponível em:

```bash
http://127.0.0.1:5000
```

---

# API REST

## Endpoints Principais

| Método | Endpoint |
|---|---|
| GET | /api/alunos |
| GET | /api/professores |
| GET | /api/cursos |
| GET | /api/disciplinas |
| POST | /api/alunos |
| POST | /api/professores |

---

# Banco de Dados

O projeto utiliza SQLite.

Arquivo gerado:

```bash
instance/app.db
```

---

# Autor

Lucas Fernandez e Pietro Bastos

---

# Licença

Projeto acadêmico para fins educacionais.