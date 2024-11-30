import os
import requests

def download_gsod_data(years, base_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for year in years:
        year_url = f'{base_url}{year}/'
        response = requests.get(year_url)
        if response.status_code == 200:
            files = [line.split('"')[1] for line in response.text.splitlines() if '.csv' in line]
            for file in files:
                file_url = f'{year_url}{file}'
                local_path = f'{output_dir}/{file}'
                with requests.get(file_url, stream=True) as r:
                    r.raise_for_status()
                    with open(local_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f'Téléchargé : {file}')
        else:
            print(f"Échec du téléchargement pour l'année {year}")

# Utilisation
if __name__ == "__main__":
    years = [2019, 2020, 2021, 2022, 2023]
    base_url = 'https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/'
    output_dir = '../data/gsod'
    download_gsod_data(years, base_url, output_dir)
