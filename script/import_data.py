import os
import pandas as pd
import psycopg2

def clean_csv(file_path):
    """
    Vérifie si un fichier CSV contient des lignes problématiques (noms de colonnes)
    et les supprime avant l'importation.
    """
    try:
        print(f"Nettoyage du fichier : {file_path}")
        # Spécifiez explicitement le délimiteur
        df = pd.read_csv(file_path, delimiter=',')  # Charger le fichier CSV avec le bon délimiteur

        # Supprimer les lignes où les valeurs sont identiques aux noms des colonnes
        if df.iloc[0].to_dict() == {col: col for col in df.columns}:
            print(f"L'en-tête est détectée comme une ligne de données dans {file_path}. Ligne supprimée.")
            df = df.iloc[1:]  # Supprimer la première ligne

        # Sauvegarder le fichier nettoyé
        df.to_csv(file_path, index=False)
        print(f"Fichier nettoyé avec succès : {file_path}")
    except Exception as e:
        print(f"Erreur lors du nettoyage du fichier {file_path} : {e}")

def import_with_copy(connection, table_name, file_path):
    """
    Importer un fichier CSV dans PostgreSQL en utilisant COPY via psycopg2.
    """
    cursor = connection.cursor()
    try:
        print(f"Tentative d'importation pour le fichier : {file_path}")
        with open(file_path, 'r') as f:
            # Utiliser COPY avec CSV HEADER pour ignorer les en-têtes
            cursor.copy_expert(f"""
                COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER ',';  
            """, f)
        connection.commit()
        print(f"Données du fichier {file_path} insérées avec succès.")
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de l'importation du fichier {file_path} : {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    # Connexion à PostgreSQL
    conn = psycopg2.connect(
        dbname="weatherdata",
        user="postgres",
        password="root",  # Remplacez par votre mot de passe PostgreSQL
        host="localhost",
        port="5432"
    )

    # Nom de la table PostgreSQL
    table_name = 'gsod_data'

    # Répertoire contenant les fichiers CSV
    data_dir = '../data/gsod'  # Modifiez ce chemin en fonction de votre structure

    # Parcourir tous les fichiers CSV dans le dossier
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.csv'):  # Vérifier si c'est un fichier CSV
            file_path = os.path.join(data_dir, file_name)
            try:
                # Nettoyer le fichier CSV avant importation
                clean_csv(file_path)
                # Importer les données dans PostgreSQL
                import_with_copy(conn, table_name, file_path)
            except Exception as e:
                print(f"Erreur générale pour le fichier {file_name} : {e}")

    conn.close()
    print("Importation terminée pour tous les fichiers.")
