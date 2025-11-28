import json
from pathlib import Path


def handle_file_path(file_name: str):
    script_path = Path(__file__)
    project_root = script_path.parent.parent
    data_folder = project_root / "downloads"
    data_folder.mkdir(exist_ok=True)
    file_path = data_folder / file_name
    return file_path


def parse_data(all_reports: list[dict]) -> dict:
    pretty_data = dict()

    for report in all_reports:
        """
        Estas son dos opciones que tengo para hacer debug, porque me daba un fallo
        de KeyError "data"
            - Eso era que algun diccionario en la lista no tenia esa key
            - Estas opciones me permiten sacar el año del report
                - Debajo las keys que tienen

        print(f"Procesando año: {report.get('year', 'Año desconocido')}")
        print(f"Llaves disponibles: {report.keys()}")  # Esto nos dará una pista

        - SOLUCION:
            - Me di cuenta que cuando no puede obtener los datos, puse una key = "error"
        """

        if "data" in report.keys():
            pretty_data[report["year"]] = report["data"]
        else:
            pretty_data[report["year"]] = report["error"]

    return pretty_data


def save_data(file_path: str, report: dict):

    with open(file_path, "w", encoding="utf-8") as f:
        try:
            json.dump(report, f, indent=4, ensure_ascii=False)
        except PermissionError:
            print(f"\nError: Permiso denegado para escribir en '{file_path}'.\n")
        except Exception as e:
            print(f"\nError de Sistema/IO al escribir en '{file_path}': {e}\n")
