"""
Migração manual para a Área do Professor.

Preserva todos os dados existentes:
- Cria a tabela `turmas` (nova) via metadata, se ainda não existir.
- Adiciona colunas novas nas tabelas já existentes via ALTER TABLE,
  pulando qualquer coluna que já exista (idempotente — pode rodar
  mais de uma vez sem erro).

"""

from sqlalchemy import inspect, text

from database import Base, engine
import models 


COLUNAS_NOVAS = {
    "professores": [
        ("id_usuario", "INTEGER REFERENCES usuarios(id)"),
    ],
    "matricula": [
        ("id_turma", "INTEGER REFERENCES turmas(id_turma)"),
    ],
    "notas": [
        ("observacoes", "VARCHAR(255)"),
        ("id_professor", "INTEGER REFERENCES professores(id)"),
        ("id_turma", "INTEGER REFERENCES turmas(id_turma)"),
    ],
    "presenca": [
        ("periodo", "VARCHAR(30)"),
        ("id_professor", "INTEGER REFERENCES professores(id)"),
        ("id_turma", "INTEGER REFERENCES turmas(id_turma)"),
    ],
}


def colunas_existentes(inspetor, tabela):
    return {coluna["name"] for coluna in inspetor.get_columns(tabela)}


def migrar():
    inspetor = inspect(engine)
    tabelas_existentes = set(inspetor.get_table_names())

    print("=" * 50)
    print("Criando tabelas novas (ex: turmas), se necessário...")
    print("=" * 50)

    # create_all só cria o que ainda não existe — não mexe em tabelas
    # ou dados já presentes.
    Base.metadata.create_all(bind=engine)

    # Recarrega o inspetor após criar tabelas novas
    inspetor = inspect(engine)

    print("=" * 50)
    print("Adicionando colunas novas nas tabelas existentes...")
    print("=" * 50)

    with engine.begin() as conexao:
        for tabela, colunas in COLUNAS_NOVAS.items():

            if tabela not in tabelas_existentes and tabela not in inspect(engine).get_table_names():
                print(f"  [pular] tabela '{tabela}' não existe ainda.")
                continue

            existentes = colunas_existentes(inspetor, tabela)

            for nome_coluna, definicao_sql in colunas:

                if nome_coluna in existentes:
                    print(f"  [ok] {tabela}.{nome_coluna} já existe, pulando.")
                    continue

                comando = f"ALTER TABLE {tabela} ADD COLUMN {nome_coluna} {definicao_sql}"

                print(f"  [+] {comando}")

                conexao.execute(text(comando))

    print("=" * 50)
    print("Migração concluída. Nenhum dado foi apagado.")
    print("=" * 50)


if __name__ == "__main__":
    migrar()