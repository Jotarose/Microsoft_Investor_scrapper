# 📈 Microsoft Financial Intelligent Analyzer

**De Datos Brutos a Tesis de Inversión: Una Pipeline ETL con IA Generativa.**

Este proyecto va más allá de un simple *web scraper*. Es una herramienta integral de ingeniería de datos y análisis financiero que automatiza el ciclo de vida de la información corporativa de Microsoft: desde la extracción de datos crudos en informes anuales hasta la generación de tesis de inversión profesionales mediante Inteligencia Artificial y visualización de tendencias.

---

## Tabla de contenidos

1. [Instalación y Configuración](#instalación-y-configuración)
2. [Uso](#uso)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Funcionalidades principales](#funcionalidades-principales)
5. [Resultados y Salidas](#resultados-y-salidas)
6. [Consideraciones](#consideraciones)
7. [Contribuir](#contribuir)
8. [Contacto](#contacto)

## Instalación y Configuración

### Prerrequisitos
* **Python 3.10+**
* Una API Key de Google Gemini (Obtenla en [Google AI Studio](https://aistudio.google.com/)).

### Pasos

1.  **Clonar y preparar entorno:**
    Se recomienda usar un entorno virtual.

    ```bash
    # En PowerShell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

    # Instalar dependencias en modo editable
    pip install -e .[dev]
    ```

2.  **Configurar Variables de Entorno:**
    Para activar el analista IA, crea un archivo `.env` en la raíz del proyecto:

    ```env
    GEMINI_API_KEY=tu_clave_api_aqui
    ```

---
Notas:

- Si no usas `pip install -e .`, puedes instalar directamente las dependencias listadas en `pyproject.toml`.
- El proyecto reclama Python >= 3.10 (ver `pyproject.toml`).
- **Variables de entorno requeridas**: Para usar la funcionalidad de IA con Gemini, debes crear un archivo `.env` en la raíz del proyecto con tu clave API:
  ```
  GEMINI_API_KEY=tu_clave_api_aqui
  ```
  Obtén tu clave en [Google AI Studio](https://aistudio.google.com/app/apikey).

## Uso

El punto de entrada es el script `main.py` en la raíz del proyecto. Ejecuta el script desde la raíz del repositorio:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Al ejecutarlo, el flujo general es:

1. **Extracción web**: `src.client.MicrosoftIRClient` recopila las URLs de los informes anuales de Microsoft IR.
2. **Paralización de workers**: `main.py` usa un `ThreadPoolExecutor` para paralelizar la extracción por año.
3. **Parsing de tablas**: `src.worker.extract_financial_data` descarga la página del informe, localiza la tabla "INCOME STATEMENTS" y la transforma a un diccionario estructurado.
4. **Limpieza y serialización**: `src.utils.parse_data` y `src.utils.save_data` guardan el JSON en `downloads/all_ms_financial_data.json`.
5. **Análisis con IA**: `src.gemini_ai.generate_financial_tesis` genera un análisis profesional usando **Gemini AI** (requiere `GEMINI_API_KEY` en `.env`).
6. **Visualización**: `src.visualization.generate_tables` genera gráficas comparativas de ingresos y rentabilidad usando **matplotlib** y **seaborn**.

## Estructura del proyecto

```plaintext
.
├── main.py                  # Orquestador principal del flujo
├── pyproject.toml           # Gestión de dependencias y metadatos
├── .env                     # Variables de entorno (API Keys)
├── src/
│   ├── client.py            # Cliente HTTP (Scraper)
│   ├── worker.py            # Lógica de extracción y parsing HTML
│   ├── gemini_ai.py         # Módulo de Inteligencia Artificial
│   ├── visualization.py     # Motor de generación de gráficas
│   └── utils.py             # Herramientas de I/O y limpieza
├── downloads/
│   ├── all_ms_financial_data.json  # Dataset final
│   └── financial_tesis.md          # Reporte de IA
└── tests/                   # Suite de pruebas unitarias
```

- `main.py`: Orquestador principal. Gestiona extracción, IA, visualización y guardado de resultados.
- `pyproject.toml`: Metadatos, dependencias (incluyendo `google-genai`, `matplotlib`, `pandas`, `seaborn`).
- `README.md`: Este archivo.
- `downloads/`:
  - `all_ms_financial_data.json`: Datos financieros extraídos por año.
  - `financial_tesis.md`: Análisis generado por Gemini AI.
- `tests/`:
  - `test_client.py`: Tests unitarios para `MicrosoftIRClient`.
  - `test_worker.py`: Tests para extracción de datos financieros.
  - `test_utils.py`: Tests para funciones de utilidad.
- `src/`:
  - `__init__.py`: Inicializador del paquete.
  - `client.py`: Cliente HTTP para descargar informes de Microsoft IR.
  - `worker.py`: Extracción y parsing de tablas financieras.
  - `utils.py`: Helpers para rutas, serialización y guardado.
  - **`gemini_ai.py`** (NUEVO): Análisis con IA usando Gemini 2.5 Pro.
    - Requiere `GEMINI_API_KEY` en `.env`.
  - **`visualization.py`** (NUEVO): Gráficas y visualizaciones.

## Funcionalidades Principales

El sistema opera en cuatro fases críticas:

1.  **Extracción Inteligente (Scraping Avanzado):**
    * Navegación automática por el portal de *Investor Relations* de Microsoft.
    * Descarga y parseo de informes anuales históricos.
    * Extracción quirúrgica de tablas "INCOME STATEMENTS" usando `BeautifulSoup`.
    * Ejecución paralela mediante `ThreadPoolExecutor` para maximizar la velocidad.

2.  **Normalización de Datos (ETL):**
    * Limpieza y estructuración de datos financieros no estandarizados.
    * Conversión de formatos de moneda, manejo de valores negativos y saneamiento de nulos.
    * Serialización a JSON estructurado (`downloads/all_ms_financial_data.json`).

3.  **Analista Financiero IA (Gemini 2.5 Pro):**
    * Integración con **Google Gemini** para interpretar los datos estructurados.
    * Generación automática de una **Tesis de Inversión** (Buy/Hold/Sell).
    * Análisis profundo de la transformación del modelo de negocio (Licencias vs. Nube), márgenes operativos y eficiencia de I+D.

4.  **Visualización de Datos (Business Intelligence):**
    * Generación de gráficos interactivos con `matplotlib` y `seaborn`.
    * Análisis visual de la transición de ingresos (*Product vs. Service*).
    * Comparativa de Crecimiento vs. Rentabilidad (Revenue vs. Net Income).

---

## Resultados y Salidas

El proyecto genera tres tipos de entregables de alto valor:

### 1. Datos Estructurados (JSON)
**Archivo:** `downloads/all_ms_financial_data.json`  
Base de datos limpia y lista para ser consumida por otras aplicaciones o analistas.

```json
"2024": {
    "Revenue:": {
      "Product": "$64,773",
      "Service and other": "180,349",
      "Total revenue": "245,122"
    },
    "Net income": { "Total": "$88,136" }
}
```

### 2. Tesis de Inversión (Markdown)
**Archivo**: `downloads/financial_tesis.md`

Un reporte ejecutivo generado por IA que incluye:
- Memo Ejecutivo: Resumen de desempeño.
- Análisis de Márgenes: Gross, Operating y Net margins.
- Veredicto: Recomendación justificada (Ej: "SOBREPONDERAR").
- Riesgos: Evaluación de competencia y costes de infraestructura IA.

### 3. Visualización Gráfica
Se generan dashboards visuales para entender la historia detrás de los números:

- **Business Model Shift**: Gráfico de barras apiladas mostrando cómo los Servicios (Azure/Cloud) han canibalizado y superado a los Productos tradicionales.

- **Growth vs Profitability:** Gráfico de doble eje para medir el apalancamiento operativo.

## Consideraciones

- **Ética de Scraping:** Este proyecto respeta los tiempos de respuesta, pero asegúrate de revisar el robots.txt si planeas escalarlo o aumentar la frecuencia de peticiones.

- **Costes de API:** El uso de Gemini Pro puede tener costes asociados dependiendo de tu cuota en Google Cloud/AI Studio.

- **Robustez**: El extractor depende de la estructura HTML de los informes de Microsoft. Si ellos cambian su diseño web radicalmente, el worker.py podría requerir ajustes.

---

## Contribuir
¡Las contribuciones son bienvenidas!
1. Haz un Fork del proyecto.
2. Crea una rama (git checkout -b feature/nueva-funcionalidad).
3. Commit a tus cambios.
4. Abre un Pull Request.

---

## Contacto
Autor: Juan Arabaolaza Contacto: juan.arabaolaza@gmail.com
