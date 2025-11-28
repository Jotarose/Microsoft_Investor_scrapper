import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.client import MicrosoftIRClient
from src.utils import handle_file_path, parse_data, save_data
from src.worker import extract_financial_data


def main():
    start_time = time.time()
    max_workers = 6
    client = MicrosoftIRClient()

    try:
        report_dict = client.get_annual_reports()
        all_pretty_financial_data = []
        futures = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for report in report_dict:
                # .submit() programa la tarea y devuelve un objeto Future INMEDIATAMENTE.
                # NO bloquea el programa principal.
                future = executor.submit(extract_financial_data, client, report)

                # Guardamos el "recibo" (future) para reclamar el resultado luego.
                futures.append(future)

            for future in as_completed(futures):
                try:
                    # .result() bloquea solo lo necesario para recuperar el dato del hilo que YA terminó.
                    # Si el worker falló, aquí es donde salta la excepción.
                    data = future.result()
                    all_pretty_financial_data.append(data)
                except Exception as e:
                    print(f"Error en un worker: {e}")

    except Exception as e:
        print(f"ERROR: {e}")

    file_path = handle_file_path("all_ms_financial_data.json")
    clean_data = parse_data(all_pretty_financial_data)
    save_data(file_path, clean_data)

    end_time = time.time()
    print(f"\nTiempo total del programa {end_time - start_time:.2f}")


if __name__ == "__main__":
    main()
