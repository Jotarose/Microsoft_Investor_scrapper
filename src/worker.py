from bs4 import BeautifulSoup

from client import MicrosoftIRClient, Report

# KISS Keep It Simple Stupid
# No es necesario crear una clase para el worker
# En los apuntes dejo la documentacion de porque


def extract_financial_data(MSclient: MicrosoftIRClient, report: Report) -> dict:
    """
    Extrae datos financieros desde el informe HTML de Microsoft Investor Relations.
        - Esta función descarga el contenido HTML asociado a un reporte anual

        - Localiza la tabla correspondiente a *INCOME STATEMENTS*

            - Se identifica la tabla mediante una búsqueda literal del texto "INCOME STATEMENTS" porque el HTML es inconsistente entre años.
            - Las clases CSS utilizadas para detectar indentación son:
                - `"cell-indent"`
                - `"cell-indent-double"`
                - Si un elemento padre tiene valor propio, se asigna como `"Total"`.

        - LA transforma en un diccionario estructurado.

        - La lógica identifica secciones principales y subítems mediante clases CSS relacionadas con indentación.

    Args:
        MSclient (MicrosoftIRClient): Cliente confirgurado

        report (Report): objeto que contiene año y url del reporte

    Returns:
        dict:
            ```
            {
                "year": <año>,
                "data": {
                    "Section A": {
                        "Total": "...",
                        "Subitem 1": "...",
                        "Subitem 2": "...",
                    },
                    "Section B": {
                        ...
                    }
                }
            }
            ```

            Si la tabla no se encuentra, se devuelve:
            ```
            {
                "year": <año>,
                "error": "Tabla no encontrada"
            }
            ```

    Raises:
        None: Esta función maneja fallos comunes internamente y en caso de que
        la tabla no exista, devuelve un diccionario con la clave `"error"`.
    """

    client = MSclient
    raw_report = client.get_url_content(report.url)

    soup = BeautifulSoup(raw_report.text, "lxml")
    income_statements = soup.find(string="INCOME STATEMENTS")
    if not income_statements:
        return {"year": report.year, "error": "Tabla no encontrada"}
    income_table = income_statements.find_next("table")

    financial_data = dict()
    current_section = "General"

    for tr in income_table.find_all("tr"):
        cells = tr.find_all("td")

        # Seguridad: Ignoramos filas que no tengan al menos 2 celdas
        if len(cells) < 2:
            continue

        # Extraer la etiqueta (soup object) para analizar sus clases
        row_title_tag = cells[0]
        row_title_text = row_title_tag.get_text(strip=True)
        row_value = cells[1].get_text(strip=True)

        # Si no hay título, saltamos
        if not row_title_text:
            continue

        # --- LÓGICA MAESTRA ---
        # Obtenemos la lista de clases CSS de la primera celda
        # Si no tiene clases, devuelve una lista vacía []
        row_classes = row_title_tag.get("class", [])

        # CASO A: Es una SECCIÓN PRINCIPAL (Padre)
        # Identificamos al padre porque NO tiene la clase "cell-indent"
        if "cell-indent" not in row_classes and "cell-indent-double" not in row_classes:
            current_section = row_title_text
            # Creamos el diccionario para esta nueva sección
            financial_data.setdefault(current_section, {})

            # Si el padre tiene un valor propio (ej: "Research and development"),
            # lo guardamos como "Total" para no romper la estructura
            if row_value:
                financial_data[current_section]["Total"] = row_value

            continue  # Pasamos a la siguiente fila

        # CASO B: Es un SUB-ITEM (Hijo)
        # Si llegamos aquí, es porque TIENE indentación
        if row_value:
            # Aseguramos que la sección existe (por si acaso)
            financial_data.setdefault(current_section, {})
            # Guardamos el dato
            financial_data[current_section][row_title_text] = row_value

    # Resultado final
    final_result = {"year": report.year, "data": financial_data}

    return final_result
