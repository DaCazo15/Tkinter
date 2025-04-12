import requests
from bs4 import BeautifulSoup
import urllib3

def scrap():
    url = "https://www.bcv.org.ve/"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers, verify=False, timeout=20)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        print("Página cargada correctamente.")

        ttls = soup.find_all('div', class_ = 'col-sm-6 col-xs-6')  
        mds = soup.find_all('div', class_ = 'col-sm-6 col-xs-6 centrado') 
        ttl, md = [], []
        if ttls and mds:
            long = len(ttls)
            for i in range(long):
                ttl.append(ttls[i].text.strip())
                md.append(mds[i].text.strip())
        else:
            return "none", "none"
        return ttl, md
    else:
        return f"Error al recuperar la página. Código de estado: {response.status_code}"