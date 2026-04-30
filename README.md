# IngeInv — Plataforma de Gestión Inteligente de Mantenimiento Industrial

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Kotlin](https://img.shields.io/badge/Android-Kotlin%20%7C%20Jetpack%20Compose-7F52FF?logo=kotlin&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/Licencia-MIT-green)

**IngeInv** es un ecosistema de herramientas para **ingeniería industrial** que combina una API REST, una aplicación de escritorio, una app Android y análisis inteligente de formas técnicas. Su objetivo es centralizar la gestión de maquinaria, automatizar el mantenimiento y dar soporte a ingenieros y técnicos de producción.

---

## 📦 Componentes del proyecto

| Componente | Archivo / Carpeta | Tecnología | Descripción |
|---|---|---|---|
| **API REST** | `src/ingeinv/` | Python · FastAPI · SQLAlchemy | Backend con endpoints para máquinas, mantenimiento y predicción de fallos |
| **App de Escritorio** | `Ingenieria.py` | Python · Tkinter / CustomTkinter | Interfaz gráfica completa: máquinas, componentes, calibraciones, planos y más |
| **App Android** | `IngenieriaScreen.kt` | Kotlin · Jetpack Compose | Pantalla principal del ingeniero con acceso a todos los módulos desde el móvil |
| **Análisis de Formas (ML/CV)** | `contour_fourier.py` | Python · OpenCV · NumPy | Extrae contornos de imágenes o PDF y los representa como serie de Fourier |

---

## 🚀 Funcionalidades principales

### 🔧 Gestión industrial (API + Desktop + Android)
- Registro de **máquinas**, componentes y estado operativo
- Gestión de **personal** técnico y operarios
- **Cronogramas de mantenimiento** preventivos y correctivos
- **Lecturas de sensores** y telemetría en tiempo real
- **Predicción de fallos** con modelo de Machine Learning (scikit-learn)
- **Asistente AaaS** con recomendaciones en tiempo real

### 🛠️ Herramientas especializadas (Android)
- **Calculadora Solar** — dimensionamiento de sistemas fotovoltaicos
- **Compilador LaTeX** — editor y visualizador de documentos técnicos
- **Planos y Datos Espaciales** — dibujo de planos y mapas con sensores

### 📐 Análisis de contornos (ML/CV)
- Extrae el contorno principal de cualquier imagen PNG/JPG o PDF técnico
- Calcula la **Serie de Fourier** del contorno como señal compleja `x + i·y`
- Exporta coeficientes a JSON para usar en modelos de clasificación o reconstrucción
- Genera imagen comparativa (original vs. reconstruida)

---

## 🏗️ Estructura del proyecto

```
IngeInv/
├── src/ingeinv/            # API REST (FastAPI)
│   ├── main.py             # Punto de entrada
│   ├── database.py         # Configuración SQLAlchemy
│   ├── models/             # Modelos ORM (Machine, Component, SensorReading, …)
│   ├── services/           # Lógica de negocio (MachineService, PredictionService, …)
│   └── routers/            # Endpoints REST (machines, maintenance, predictions)
├── tests/                  # Tests con pytest
├── Ingenieria.py           # App de escritorio (Tkinter/CustomTkinter)
├── IngenieriaScreen.kt     # Pantalla principal Android (Jetpack Compose)
├── contour_fourier.py      # Herramienta ML/CV: contornos → Fourier
├── requirements.txt        # Dependencias Python
└── pyproject.toml          # Configuración del paquete
```

---

## ⚙️ Instalación

```bash
pip install -r requirements.txt
```

Para usar la herramienta de análisis de contornos, instala también:

```bash
pip install opencv-python matplotlib PyMuPDF
```

---

## ▶️ Ejecución

### API REST

```bash
uvicorn src.ingeinv.main:app --reload
```

Navega a `http://localhost:8000/docs` para la documentación interactiva (Swagger UI).

### App de Escritorio

```bash
python Ingenieria.py
```

### Análisis de Contornos / Fourier

```bash
# Desde una imagen PNG o JPG
python contour_fourier.py --input plano.png --output coeficientes.json --plot reconstruccion.png

# Desde un PDF técnico
python contour_fourier.py --input manual.pdf --output coeficientes.json --terms 150
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Abre un *issue* o envía un *pull request*.

---

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
