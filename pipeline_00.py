import os
import gdown
import duckdb
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

# Função para baixar arquivos de um diretório google drive
def baixar_os_arquivos_do_google_drive(url_pasta, diretorio_local):
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url_pasta, output=diretorio_local, quiet=False, use_cookies=False)


# Função para listar os arquivos CSV no diretório especificado
def listar_arquivos_csv(diretorio):
    arquivos_csv = []
    todos_os_arquivos = os.listdir(diretorio)
    for arquivo in todos_os_arquivos:
        if arquivo.endswith('.csv'):
            caminho_completo = os.path.join(diretorio, arquivo)
            arquivos_csv.append(caminho_completo)
    return arquivos_csv


# Função para ler um arquivo CSV e retornar um DataFrame
def ler_csv(caminho_do_arquivo):
    data_frame_duckdb = duckdb.read_csv(caminho_do_arquivo)
    print(data_frame_duckdb)
    print(type(data_frame_duckdb))
    return data_frame_duckdb


# Função para adicionar uma coluna de total de vendas
def transformar(df):
    # Executa a consulta SQL que inclui a nova colunaa, operando sobre a tela virtual
    df_transformado = duckdb.sql('SELECT *, quantidade * valor AS total_vendas FROM df').df()
    # Remove o registro da tabela virtual para limpeza
    return df_transformado


# Função para converter o Duckdb em Pandas e salvar o DataFrame no PostgreSQL
def salvar_no_postgres(df_duckdb, tabela):
    DATABASE_URL = os.getenv("DATABASE_URL")  # Ex: 'postgresql://user:password@localhost:5432/database_name'
    engine = create_engine(DATABASE_URL)
    # Salvar o DataFrame no PostgreSQL
    df_duckdb.to_sql(tabela, con=engine, if_exists='append', index=False)

# Transformação

if __name__ == '__main__':
    url_pasta = 'https://drive.google.com/drive/folders/19flL9P8UV9aSu4iQtM6Ymv-77VtFcECP'
    diretorio_local = './pasta_gdown'

    # baixar_os_arquivos_do_google_drive(url_pasta, diretorio_local)
    lista_arquivos = listar_arquivos_csv(diretorio_local)
    for caminho_arquivo in lista_arquivos:
        duckdb_df = ler_csv(caminho_arquivo)
        pandas_df_transformado = transformar(duckdb_df)
        salvar_no_postgres(pandas_df_transformado, "vendas_calculado")
