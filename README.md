# 🎓 GICA Generador

**Sistema Inteligente de Generación de Documentos de Tesis Académicas**

GICA Generador es una aplicación web desarrollada en Django que automatiza la generación de documentos de tesis académicas mediante inteligencia artificial. El sistema permite a los usuarios seleccionar formatos específicos por universidad y carrera, elegir prompts personalizados para diferentes secciones de tesis, y generar automáticamente contenido académico de calidad mediante integración con servicios de IA a través de n8n.

---

## 🚀 Características Principales

### ✨ Funcionalidades Core

- **📝 Gestión de Prompts**: Sistema CRUD completo para administrar plantillas de prompts con variables dinámicas y tipos de documento
- **🏫 Catálogo de Formatos de Tesis**: Base de datos de formatos por universidad, carrera, versión y estructura JSON personalizada
- **🧙‍♂️ Wizard de Generación**: Interfaz interactiva paso a paso para crear documentos de tesis de forma guiada
- **📊 Dashboard con Métricas**: Panel de control con estadísticas de proyectos generados, tokens consumidos y horas estimadas
- **🔗 Integración con Webhook n8n**: Automatización de solicitudes a servicios de IA para generación de contenido
- **📚 Historial de Generaciones**: Seguimiento completo de todos los proyectos de tesis generados

### 🏗️ Arquitectura Técnica

El proyecto implementa **Clean Architecture** garantizando:
- ✅ Separación de responsabilidades en capas
- ✅ Independencia de frameworks
- ✅ Testabilidad y mantenibilidad
- ✅ Escalabilidad del sistema

---

## 📁 Estructura del Proyecto

```
GICA_GENERADOR/
│
├── domain/                          # 🎯 Capa de Dominio (Lógica de Negocio Pura)
│   ├── entities/                    # Entidades del dominio
│   │   ├── prompt.py                # Entidad Prompt (plantillas de IA)
│   │   ├── formato_tesis.py         # Entidad FormatoTesis (estructura por universidad)
│   │   └── proyecto.py              # Entidad Proyecto (generaciones realizadas)
│   └── ports/                       # Interfaces/Contratos (Dependency Inversion)
│       ├── prompt_repository.py
│       ├── format_repository.py
│       └── generation_webhook_port.py
│
├── application/                     # ⚙️ Capa de Aplicación (Casos de Uso)
│   └── services/
│       ├── gestionar_prompts_service.py        # UC: Gestión de prompts
│       ├── sincronizar_formatos_service.py     # UC: Sincronización de formatos
│       └── solicitar_generacion_service.py     # UC: Generación de tesis
│
├── infrastructure/                  # 🔧 Capa de Infraestructura (Detalles de Implementación)
│   ├── django_app/                  # Framework Django
│   │   ├── models.py                # Modelos ORM (PromptModel, FormatoTesisModel, ProyectoModel)
│   │   ├── views.py                 # Vistas CBV/FBV
│   │   ├── forms.py                 # Formularios Django
│   │   ├── urls.py                  # Rutas URL
│   │   ├── admin.py                 # Configuración Admin
│   │   └── container.py             # Dependency Injection Container
│   └── adapters/                    # Adaptadores de infraestructura
│       ├── repositories/            # Implementaciones de repositorios
│       │   ├── django_prompt_repository.py
│       │   └── django_format_repository.py
│       └── http/                    # Adaptadores HTTP
│           ├── webhook_adapter.py   # Integración con n8n webhook
│           └── external_format_api_adapter.py
│
├── templates/                       # 🎨 Plantillas HTML
│   ├── base.html                    # Template base con Bootstrap
│   ├── prompts/                     # Templates CRUD de prompts
│   ├── generador/                   # Templates del wizard
│   └── dashboard/                   # Templates del dashboard
│
├── static/                          # 📦 Archivos estáticos (CSS, JS, imágenes)
│
├── gica_generador/                  # ⚙️ Configuración Django
│   ├── settings.py                  # Configuración principal
│   ├── urls.py                      # URLs raíz
│   └── wsgi.py                      # WSGI entry point
│
├── db.sqlite3                       # 💾 Base de datos SQLite
├── manage.py                        # 🛠️ CLI de Django
├── requirements.txt                 # 📋 Dependencias Python
├── .env.example                     # 🔑 Variables de entorno ejemplo
└── README.md                        # 📖 Documentación
```

---

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnologías |
|-----------|-------------|
| **Backend Framework** | Django 4.2+ |
| **Lenguaje** | Python 3.8+ |
| **Base de Datos** | SQLite (desarrollo), PostgreSQL/MySQL (producción) |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Automatización** | n8n (webhook integration) |
| **Gestión de Configuración** | python-dotenv |
| **HTTP Client** | requests |
| **Arquitectura** | Clean Architecture, Dependency Injection |

---

## 📋 Requisitos Previos

- **Python**: 3.8 o superior
- **pip**: Gestor de paquetes de Python
- **Git**: Para clonar el repositorio (opcional)

---

## ⚙️ Configuración e Instalación

### 1️⃣ Clonar el Repositorio (opcional)

```bash
git clone <URL_DEL_REPOSITORIO>
cd GICA_GENERADOR
```

### 2️⃣ Crear Entorno Virtual (Recomendado)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno

1. Copie el archivo de ejemplo `.env.example` a `.env`:
   ```bash
   copy .env.example .env     # Windows
   cp .env.example .env       # Linux/Mac
   ```

2. Edite el archivo `.env` y ajuste las variables según su entorno:

```env
# Modo de desarrollo/producción
DEBUG=True

# Clave secreta de Django (cambiar en producción)
SECRET_KEY=tu_clave_segura_cambiar_en_produccion

# Base de datos (SQLite por defecto)
DATABASE_URL=sqlite:///db.sqlite3

# Webhook n8n para envío de generación de tesis
WEBHOOK_URL=https://autogica.ingemec.org.pe/webhook-test/c8e6e6f5-9707-41a8-85dc-5ed8438087c1

# API externa de formatos (opcional, si está vacío usa datos simulados)
EXTERNAL_FORMATS_API_URL=

# Hosts permitidos (separados por coma)
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5️⃣ Ejecutar Migraciones de Base de Datos

```bash
python manage.py migrate
```

### 6️⃣ (Opcional) Crear Superusuario para Admin

```bash
python manage.py createsuperuser
```

### 7️⃣ Cargar Datos Iniciales (Opcional)

Si existen fixtures con formatos o prompts predefinidos:

```bash
python manage.py loaddata initial_data
```

---

## 🚀 Levantar el Proyecto

### Modo Desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: **http://127.0.0.1:8000/**

### Especificar Puerto Personalizado

```bash
python manage.py runserver 8080
```

### Acceder desde la Red Local

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 📖 Guía de Uso

### 🎯 Rutas Principales

| URL | Descripción |
|-----|-------------|
| `/` | Redirige automáticamente al wizard de generación |
| `/wizard/` | Wizard interactivo para generar documentos de tesis |
| `/dashboard/` | Panel de control con métricas y estadísticas |
| `/historial/` | Historial completo de generaciones realizadas |
| `/prompts/` | Lista de prompts disponibles |
| `/prompts/crear/` | Crear nuevo prompt |
| `/prompts/editar/<id>/` | Editar prompt existente |
| `/prompts/eliminar/<id>/` | Eliminar prompt |
| `/admin/` | Panel de administración Django |

### 🧙‍♂️ Flujo de Generación de Tesis

1. **Acceder al Wizard**: Navegar a `/wizard/`
2. **Seleccionar Formato**: Elegir universidad, carrera y formato de tesis
3. **Elegir Prompt**: Seleccionar el tipo de documento (introducción, capítulo, conclusión, etc.)
4. **Completar Variables**: Rellenar las variables dinámicas requeridas (tema, objetivos, etc.)
5. **Enviar Solicitud**: El sistema envía la petición al webhook de n8n
6. **Seguimiento**: Ver el progreso en el dashboard y historial

### 📊 Dashboard

El dashboard muestra:
- Total de proyectos generados
- Total de tokens consumidos
- Horas estimadas de trabajo ahorradas
- Últimas 10 generaciones realizadas

---

## 🔌 API Endpoints (JSON)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/prompts/` | Listar todos los prompts activos |
| `GET` | `/api/prompts/<id>/` | Obtener prompt específico |
| `POST` | `/api/prompts/` | Crear nuevo prompt |
| `PUT` | `/api/prompts/<id>/` | Actualizar prompt |
| `DELETE` | `/api/prompts/<id>/` | Eliminar prompt |
| `POST` | `/api/solicitar-generacion/` | Enviar solicitud de generación |

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test infrastructure.django_app

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

---

## 📦 Dependencias

```txt
Django>=4.2,<5.0          # Framework web principal
python-dotenv>=1.0.0      # Gestión de variables de entorno
requests>=2.31.0          # Cliente HTTP para webhooks
```

---

## 🏛️ Principios de Clean Architecture

### Capas y Flujo de Dependencias

```
┌─────────────────────────────────────────────┐
│          CAPA DE PRESENTACIÓN               │
│        (Templates, Views, URLs)             │
└────────────────┬────────────────────────────┘
                 │ depends on ↓
┌────────────────▼────────────────────────────┐
│       CAPA DE APLICACIÓN                    │
│     (Services/Use Cases)                    │
└────────────────┬────────────────────────────┘
                 │ depends on ↓
┌────────────────▼────────────────────────────┐
│          CAPA DE DOMINIO                    │
│     (Entities, Ports/Interfaces)            │
└─────────────────────────────────────────────┘
                 ▲ implemented by
┌────────────────┴────────────────────────────┐
│       CAPA DE INFRAESTRUCTURA               │
│  (Repositories, Adapters, Django ORM)       │
└─────────────────────────────────────────────┘
```

### Ventajas de esta Arquitectura

✅ **Independencia de Frameworks**: La lógica de negocio no depende de Django  
✅ **Testabilidad**: Fácil de crear tests unitarios con mocks  
✅ **Mantenibilidad**: Cambios aislados por capa  
✅ **Escalabilidad**: Fácil agregar nuevas funcionalidades  

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto es privado y confidencial.

---

## 👥 Equipo de Desarrollo

**GICA - Generador Inteligente de Contenido Académico**

---

## 📧 Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contactar al equipo de desarrollo.

---

**¡Gracias por utilizar GICA Generador! 🎓✨**
