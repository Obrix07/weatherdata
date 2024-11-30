import pandas as pd
import psycopg2

# Inférence des types SQL pour la création de la table
def infer_sql_type(pandas_dtype, col_name=None):
    # Mappez les colonnes spécifiques à leurs types attendus
    type_map = {
        "STATION": "BIGINT",
        "DATE": "DATE",
        "LATITUDE": "FLOAT",
        "LONGITUDE": "FLOAT",
        "ELEVATION": "FLOAT",
        "TEMP": "FLOAT",
        "TEMP_ATTRIBUTES": "INTEGER",
        "DEWP": "FLOAT",
        "DEWP_ATTRIBUTES": "INTEGER",
        "SLP": "FLOAT",
        "SLP_ATTRIBUTES": "INTEGER",
        "STP": "FLOAT",
        "STP_ATTRIBUTES": "INTEGER",
        "VISIB": "FLOAT",
        "VISIB_ATTRIBUTES": "INTEGER",
        "WDSP": "FLOAT",
        "WDSP_ATTRIBUTES": "INTEGER",
        "MXSPD": "FLOAT",
        "GUST": "FLOAT",
        "MAX": "FLOAT",
        "MAX_ATTRIBUTES": "TEXT",
        "MIN": "FLOAT",
        "MIN_ATTRIBUTES": "TEXT",
        "PRCP": "FLOAT",
        "PRCP_ATTRIBUTES": "TEXT",
        "SNDP": "FLOAT",
        "FRSHTT": "INTEGER",
    }

    if col_name and col_name.upper() in type_map:
        return type_map[col_name.upper()]

    # Inférer automatiquement si la colonne n'est pas dans le type_map
    if pandas_dtype == "int64":
        return "INTEGER"
    elif pandas_dtype == "float64":
        return "FLOAT"
    elif pandas_dtype == "object":
        return "TEXT"
    elif pandas_dtype == "datetime64[ns]":
        return "TIMESTAMP"
    else:
        return "TEXT"

# Analyse du fichier et génération des colonnes
def analyze_sample(file_path):
    """
    Analyse un fichier CSV et infère les colonnes et types SQL pour la création de table.
    """
    df = pd.read_csv(file_path, delimiter=',', nrows=0)  # Lire uniquement les en-têtes
    columns = []
    for col in df.columns:
        sql_type = infer_sql_type(df[col].dtype.name, col_name=col)
        columns.append(f'"{col}" {sql_type}')
    return columns

# Création de la table dans PostgreSQL
def create_table(connection, table_name, columns):
    """
    Crée une table PostgreSQL avec les colonnes spécifiées.
    """
    columns_sql = ',\n'.join(columns)
    create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} (\n{columns_sql}\n);'
    cursor = connection.cursor()
    cursor.execute(create_table_sql)
    connection.commit()
    print(f"Table {table_name} créée avec succès.")
    cursor.close()

if __name__ == "__main__":
    # Exemple de fichier pour l'analyse des colonnes
    sample_file = '../data/gsod/01001099999.csv'
    table_name = 'gsod_data'

    # Analyse et création de la table
    columns = analyze_sample(sample_file)
    conn = psycopg2.connect(
        dbname="weatherdata",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    create_table(conn, table_name, columns)
    conn.close()
