# Wesley Inventario Bot 🤖📦

**Un chatbot inteligente para gestionar el inventario del Centro Médico Wesley**

---

## Descripción 📋

**Wesley_Inventario_Bot** es un chatbot desarrollado para consultar y gestionar el inventario del Centro Médico Wesley. Con este bot, los usuarios pueden obtener información en tiempo real sobre la disponibilidad de medicamentos y otros suministros médicos. La inteligencia detrás de este bot está diseñada para aprender y proporcionar estimaciones de disponibilidad de productos, ayudando en la toma de decisiones.

### Equipo de desarrollo 👥

- **Víctor Aparicio**
- **Yelimar Hernández**
- **Ricardo Parra**
- **Enmanuel Torres**

## Requisitos de Instalación ⚙️

Para ejecutar este proyecto, es necesario configurar un entorno con **Conda** y luego instalar las dependencias especificadas a continuación.

---

### Pasos para Configuración del Entorno

#### 1. Crear el entorno virtual

```bash
conda create --name nombre_del_entorno python=3.9
```

#### 2. Activar el entorno

```bash
conda activate nombre_del_entorno
```

#### 3. Instalar dependencias:

- Instalar Spacy:
  ```bash
  pip install spacy
  ```

- Instalar Experta:
  ```bash
  pip install experta
  ```

- Instalar PyTorch (CPU):
  ```bash
  conda install pytorch cpuonly -c pytorch
  ```

- Instalar Rasa con Spacy:
  ```bash
  pip install rasa[spacy]
  ```

- Instalar Rasa SDK:
  ```bash
  pip install rasa-sdk
  ```

- Descargar el modelo de Spacy en español:
  ```bash
  python -m spacy download es_core_news_md
  ```

- Instalar el conector de MySQL:
  ```bash
  pip install mysql-connector-python
  ```
- Instalar el Dotenv:
  ```bash
    pip install python-dotenv
  ```

## Entrenamiento y Ejecución del Bot 🚀

### Para entrenar el modelo de Rasa:

1. Activar el entorno:
   ```bash
   conda activate nombre_del_entorno
   ```

2. Ejecutar el entrenamiento del modelo:
   ```bash
   rasa train
   ```

### Para iniciar el bot en modo interactivo:

1. Activar el servidor de acciones personalizadas:
   ```bash
   rasa run actions
   ```
2.  Iniciar el bot:
```bash
rasa shell
```

