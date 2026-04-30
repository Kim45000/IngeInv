# IngeInv — Gestión Inteligente de Mantenimiento Industrial

**IngeInv** es una plataforma de software orientada a la **gestión y predicción de fallos** en maquinaria industrial. Su objetivo es automatizar completamente la planificación de mantenimientos, optimizar costos operativos y brindar asistencia inteligente a ingenieros y técnicos de producción.

---

## 🚀 Características principales

| Módulo | Descripción |
|---|---|
| **Gestión de máquinas** | Registro de máquinas, componentes y su estado operativo |
| **Lecturas de sensores** | Ingesta y almacenamiento de telemetría en tiempo real |
| **Predicción de fallos** | Modelo de ML (scikit-learn) que estima la probabilidad de fallo |
| **Planificación de mantenimiento** | Generación automática de órdenes de trabajo preventivas y correctivas |
| **API REST** | Interfaz FastAPI documentada con Swagger UI |

---

## 🏗️ Arquitectura

```
IngeInv/
├── src/ingeinv/
│   ├── main.py          # Punto de entrada FastAPI
│   ├── database.py      # Configuración SQLAlchemy
│   ├── models/          # Modelos ORM (Machine, Component, SensorReading, …)
│   ├── services/        # Lógica de negocio (MachineService, PredictionService, …)
│   └── routers/         # Endpoints REST
└── tests/               # Tests con pytest
```

---

## ⚙️ Instalación

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
uvicorn src.ingeinv.main:app --reload
```

Navega a `http://localhost:8000/docs` para la documentación interactiva.

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
