# 🚀 Ejecutar Interfaz Desktop con Streamlit

## Opción 1: Ejecutar Directamente (Recomendado)

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Configurar API Key (Opcional pero recomendado)
```bash
# En macOS/Linux:
export ANTHROPIC_API_KEY="sk-ant-..."

# En Windows (PowerShell):
$env:ANTHROPIC_API_KEY="sk-ant-..."

# O crear archivo .env:
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Paso 3: Ejecutar la app
```bash
streamlit run app.py
```

Debería abrir automáticamente en tu navegador: `http://localhost:8501`

---

## Opción 2: Ejecutar como Ejecutable (Desktop App)

Convertir a aplicación desktop con PyInstaller:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Generar ejecutable
pyinstaller --onefile --windowed \
  --name="Medical-Automation" \
  --icon="icon.png" \
  app.py
```

El ejecutable estará en: `dist/Medical-Automation`

---

## Opción 3: Crear Atajo en Escritorio (macOS/Linux)

### En macOS, crear `run_app.command`:
```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
streamlit run app.py
```

Luego:
```bash
chmod +x run_app.command
# Mueve a Escritorio o Aplicaciones
```

### En Linux, crear `run_app.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
streamlit run app.py
```

Luego:
```bash
chmod +x run_app.sh
# Ejecutar: ./run_app.sh
```

---

## Solución de Problemas

### "command not found: streamlit"
```bash
# Asegúrate de estar en el venv
source venv/bin/activate
pip install streamlit
```

### "ModuleNotFoundError: anthropic"
```bash
pip install -r requirements.txt
```

### "API key not configured"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
streamlit run app.py
```

### Puerto 8501 ya está en uso
```bash
# Usar puerto diferente
streamlit run app.py --server.port 8502
```

---

## 🎨 Interfaz de Usuario

La aplicación tiene 4 secciones:

### 1️⃣ Inicio
- Bienvenida e información
- Descripción de funcionalidades
- Instrucciones de uso

### 2️⃣ Organizar Archivos
- Sube múltiples archivos
- Se organizan automáticamente por categoría
- Descarga estructura organizada

### 3️⃣ Redactar Datos
- Sube archivo con datos sensibles
- Redacta automáticamente (SSN, nombres, pólizas)
- Descarga archivo seguro

### 4️⃣ Generar Documentos
- Sube archivo redactado
- Selecciona tipo de documento
- Ingresa diagnóstico y detalles
- Genera con Claude AI
- Descarga documento profesional

---

## ⚙️ Configuración Avanzada

### Personalizar tema Streamlit
Crear `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#0d6efd"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#212529"
font = "sans serif"

[client]
showErrorDetails = true
```

### Cambiar puerto
```bash
streamlit run app.py --server.port 8502
```

### Modo headless (sin navegador)
```bash
streamlit run app.py --logger.level=debug --client.showErrorDetails=true
```

---

## 📱 Acceder desde otra computadora (LAN)

Si quieres que otros en tu red accedan:

```bash
# Escuchar en todas las interfaces
streamlit run app.py --server.address 0.0.0.0
```

Luego otros pueden acceder a: `http://tu-ip:8501`

**⚠️ Advertencia de seguridad:** No hagas esto sin protección si tienes datos sensibles.

---

## 🐳 Opcional: Ejecutar con Docker

Crear `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

Ejecutar:
```bash
docker build -t medical-automation .
docker run -p 8501:8501 medical-automation
```

---

## ✨ Próximos Pasos

- [ ] Ejecuta `streamlit run app.py`
- [ ] Prueba con archivos de ejemplo
- [ ] Configura API key si quieres generar documentos
- [ ] Personaliza tema según prefieras
- [ ] Comparte con tu equipo

---

**¡Listo! Tu interfaz desktop está funcionando.** 🎉
