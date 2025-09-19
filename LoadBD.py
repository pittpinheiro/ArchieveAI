import sqlite3
import pandas as pd

try: 
    conectar = sqlite3.connect("Livros.sql")
    print("Conexão com o banco estabelecida.")

    leitura = pd.read_sql_query("SELECT * FROM Livros", conectar)

    print(leitura.head())

except sqlite3.Error as e:
    print(f"Erro ao acessar a base: {e}")

except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

finally:
    if conectar:
        conectar.close()
        print("Conexão com o banco encerrada.")