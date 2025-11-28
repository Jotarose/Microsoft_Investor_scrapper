import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, element


@dataclass
class Report:
    """
    Representa la información extraída de un informe anual.

    Attributes:
        year (int): El año fiscal asociado al informe.
        url (str): La URL absoluta o relativa al documento o página del informe.
    """

    year: int
    url: str


class MicrosoftIRClient:
    """
    Cliente para interactuar con el portal de Relaciones con Inversores de Microsoft.

    Se encarga de gestionar la conexión HTTP simulando un navegador real y
    parsear el contenido HTML para extraer recursos financieros.

    Attributes:
        _base_url (str): La URL punto de entrada para los informes anuales.
        _headers (dict): Cabeceras HTTP para evitar bloqueos (User-Agent, etc.).
    """

    _base_url = "https://www.microsoft.com/en-us/Investor/annual-reports"
    _headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

    def __init__(self):
        # Podría usar requests.get(self._base_url, headers=self._headers)
        # Ya que solo estoy haciendo una petición y en ella descargo todo
        self._session = requests.sessions.Session()
        self._session.headers.update(self._headers)

    def get_annual_reports(self) -> list[Report]:
        """
        Obtiene una lista de informes anuales disponibles en la web de Microsoft.

        Realiza una petición GET a la página de informes, parsea el HTML y filtra
        los enlaces que corresponden a informes anuales.

        Returns:
            list[Report]: Una lista de objetos Report conteniendo el año y la URL.
                          Devuelve una lista vacía si no se encuentran coincidencias.

        Raises:
            requests.RequestException: Si ocurre un error de red al conectar con Microsoft.
        """

        response = self._session.get(self._base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        all_annual_urls = soup.find_all(
            "a", attrs={"aria-label": re.compile(r"Annual report VIEW ONLINE", re.I)}
        )

        return self._parse_reports(all_annual_urls)

    def get_url_content(self, annual_url: str) -> requests.Response:
        """
        Realiza una petición GET a una url de Annual report

        Returns:
            requests.Response: devuelve la respuesta ya cruda

        Raises:
            requests.RequestException: Si ocurre un error de red al conectar con Microsoft.
        """
        response = self._session.get(annual_url)
        response.raise_for_status()

        return response

    def _parse_reports(self, all_annual_urls: list[element.Tag]) -> list[Report]:
        """
        Procesa las etiquetas HTML crudas y extrae los datos estructurados.

        Busca un patrón de año (4 dígitos) dentro del atributo aria-label de cada etiqueta.

        Args:
            all_annual_urls (list[element.Tag]): Lista de etiquetas <a> encontradas por BeautifulSoup.

        Returns:
            list[Report]: Lista limpia de objetos Report validados.
        """

        reports = []

        for tag in all_annual_urls:
            aria = tag.get("aria-label")
            match = re.search(r"\b(\d{4})\b", aria)

            if match:
                year = int(match.group(1))

            url = tag.get("href")
            reports.append(Report(year, url))

        return reports


def main():

    client = MicrosoftIRClient()
    links = client.get_annual_reports()

    for link in links:
        print(link)


if __name__ == "__main__":
    main()
