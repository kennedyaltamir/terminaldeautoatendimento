# dump_db_completo.py
import os
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada!")

# Ajuste para SQLAlchemy Postgres
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

output_file = "banco_de_dados_atual.txt"

with engine.connect() as conn, open(output_file, "w", encoding="utf-8") as f:
    f.write("Arquivo gerado pelo script dump_db.py\n\n")

    # Para cada tabela
    for table_name in inspector.get_table_names():
        f.write(f"TABELA: {table_name}\n")
        f.write("="*60 + "\n")

        # Pega todas as colunas
        columns = [col["name"] for col in inspector.get_columns(table_name)]
        f.write("\t".join(columns) + "\n")

        # Seleciona todos os dados
        rows = conn.execute(text(f"SELECT * FROM {table_name};")).mappings().all()

        if rows:
            for row in rows:
                f.write("\t".join(str(row.get(col, "NULL")) if row.get(col, None) is not None else "NULL" for col in columns) + "\n")
        else:
            f.write("[Tabela vazia]\n")

        f.write("\n")  # separa tabelas

print(f"✅ Arquivo '{output_file}' gerado com sucesso!")
