# Generador de Fichas Técnicas PCD - MICRO Automación

Sistema web desarrollado con **FastAPI** y **Jinja2** para la visualización y generación dinámica de fichas técnicas de insertos mecanizados (PCD / Widia / Horn) para **MICRO Automación**.

---

## 🚀 Características

- **Diseño Corporativo & Modo Claro**: Interfaz profesional utilizando la paleta de colores corporativos de MICRO (`#01b2fe`).
- **Diseño Responsivo (Mobile & Desktop)**: Adaptación completa para teléfonos móviles mediante CSS Grid.
- **Visualización de Planos Técnicos & Cotas**: Botón modal interactivo que muestra el plano esquemático del inserto junto a su tabla de medidas/cotas personalizadas de 2 columnas.
- **Tipos de Mecanizados Admitidos**: Sección dedicada a diagramas de operación de la herramienta.
- **Normalización ISO de Materiales**: Muestra insignias (badges) coloridas normalizadas para materiales ISO (`P`, `M`, `K`, `N`, `S`, `H`).
- **Resolición Directa de Archivos Multimedia**: Búsqueda automática en subcarpetas dedicadas dentro de `assets/`.
- **Manejo de Errores 404 Personalizado**: Página de error estilizada cuando no se ubica un código de inserto.

---

## 🛠️ Tecnologías y Gestor de Dependencias

- **Lenguaje**: Python 3.10+
- **Framework Web**: FastAPI / Starlette
- **Motor de Plantillas**: Jinja2
- **Gestor de Paquetes**: `uv` (Astral)
- **Procesamiento de Datos**: Pandas & OpenPyXL

---

## 📊 Estructura de Columnas Requeridas en la Hoja de Excel

El archivo de datos en Excel se encuentra por defecto en `./data/INSERTOS POLICRISTALINOS Y HORN.xlsx` (con los encabezados ubicados en la **segunda fila** / `header=1`).

Las columnas reconocidas y procesadas por el sistema son:

| Nombre de Columna en Excel | Descripción | Ejemplo / Formato |
| :--- | :--- | :--- |
| `CODIGO` | Código único identificador del inserto (**Requerido**). | `HINSE270` |
| `DETALLE` | Descripción o denominación técnica del inserto. | `GIPA 4,00 PCD` |
| `PORTA HERRAMIENTAS COMPATIBLE` | Lista de porta herramientas compatibles separados por comas. | `GHGR 20-4, SDJCR 2020K-11` |
| `Vc [m/mm]` | Rango de velocidad de corte admitida. | `120 - 257` |
| `Ft [mm/rpm]` | Rango de avance de mecanizado admitido. | `0.02 - 0.9` |
| `Ap [mm]` | Rango de profundidad de corte admitida. | `0.01 - 1.0` |
| `Radio [mm]` | Radio de punta del inserto (acepta también `R [mm]`). | `0.4` |
| `CLASIFICACIÓN ISO DE MATERIALES` | Clasificación de materiales admitidos separados por comas. | `N, M, K` |
| `Cotas Plano` | Parejas clave/valor para las medidas del plano (acepta `Cotas Plano` o `Medidas Plano`). | `LF: 125.0 mm; LU: 35.0 mm; CW: 3.0 mm` |

---

## 📁 Estructura de Directorios para Multimedia (`assets/`)

Para asociar las imágenes a cada inserto, basta con guardarlas en su respectivo directorio dentro de `assets/` usando como nombre el **código del inserto** (en minúsculas o mayúsculas) y extensión `.png`, `.jpg`, `.jpeg`, `.svg` o `.webp`:

```text
assets/
├── insertos/       <-- Fotos del inserto (ej: HINSE270.png)
├── planos/         <-- Planos técnicos / diagramas acotados (ej: HINSE270.png)
└── mecanizados/    <-- Dibujos de tipos de mecanizado (ej: HINSE270.png)
```

---

## 💻 Instalación y Ejecución

### 1. Clonar el repositorio e instalar dependencias con `uv`
```bash
uv sync
```

### 2. Iniciar el servidor de desarrollo FastAPI
```bash
uv run uvicorn main:app --reload
```

### 3. Consultar una Ficha Técnica
Abre tu navegador e ingresa a:
- [http://127.0.0.1:8000/ficha-tecnica?code=HINSE270](http://127.0.0.1:8000/ficha-tecnica?code=HINSE270)
