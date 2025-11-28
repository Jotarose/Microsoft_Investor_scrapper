import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

from src.client import MicrosoftIRClient
from src.gemini_ai import GeminiAIError, generate_financial_tesis
from src.utils import handle_file_path, parse_data, save_data, save_tesis
from src.visualization import generate_tables
from src.worker import extract_financial_data

load_dotenv()  # Carga las variables de entorno desde el archivo .env


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

    data_file_path = handle_file_path("all_ms_financial_data.json")
    clean_data = parse_data(all_pretty_financial_data)
    save_data(data_file_path, clean_data)

    try:
        financial_tesis = generate_financial_tesis(clean_data)
        tesis_file_path = handle_file_path("financial_tesis.md")
        save_tesis(tesis_file_path, financial_tesis)

    except GeminiAIError as gaie:
        print(f"Error al generar la visualización con Gemini AI: {gaie}")

    # Plot visualizations (Data Tables)
    generate_tables(clean_data)

    end_time = time.time()
    print(f"\nTiempo total del programa {end_time - start_time:.2f}")


if __name__ == "__main__":
    main()
