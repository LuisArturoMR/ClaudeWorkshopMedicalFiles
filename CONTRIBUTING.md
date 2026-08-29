# 🤝 Contribuyendo al Proyecto

¡Gracias por ayudar a mejorar el Sistema de Automatización Médica!

## 📋 Antes de Empezar

1. **Seguridad primero**: Este proyecto maneja datos médicos sensibles
2. **Nunca commits datos reales**: Solo datos de prueba redactados
3. **Revisa .gitignore**: Datos sensibles deben estar en `raw_data/`, `organized_data/`, `for_claude/`

## 🚀 Configuración del Ambiente

### 1. Fork y Clonar
```bash
git clone https://github.com/TU_USUARIO/medical_automation.git
cd medical_automation
```

### 2. Crear Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
cp .env.example .env
# Edita .env con tus valores
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 5. Verificar Instalación
```bash
python3 scripts/01_organize_files.py
```

## 📝 Workflow de Desarrollo

### 1. Crea una Rama
```bash
git checkout -b feature/descripcion-cambio
# Ejemplos:
# feature/mejor-redaccion
# feature/nuevas-categorias
# fix/bug-organizacion
```

### 2. Haz tus Cambios
- Edita scripts en `scripts/`
- Prueba localmente
- Asegúrate de que no haya datos sensibles

### 3. Commit con Mensaje Claro
```bash
git add scripts/mi_cambio.py
git commit -m "feature: agregar redacción de emails

- Redacta direcciones de email automáticamente
- Agrega validación de patrones
- Incluye tests"
```

### 4. Push y Pull Request
```bash
git push origin feature/descripcion-cambio
```
Luego crea un PR en GitHub

## 🧪 Testing

### Ejecutar con Datos de Prueba
```bash
python3 scripts/run_all.py
```

### Verificar Redacción
```bash
# Compara archivos redactados
diff organized_data/Expedientes/ejemplo.txt for_claude/Expedientes/ejemplo.txt
```

### Tests Unitarios (Cuando existan)
```bash
python3 -m pytest tests/
```

## 🔒 Checklist de Seguridad

Antes de hacer un commit:

- [ ] No hay archivos en `raw_data/` con datos reales
- [ ] No hay SSN, nombres, números de póliza en commits
- [ ] `.env` no está en el repo (solo `.env.example`)
- [ ] `outputs/` no contiene documentos generados
- [ ] `.gitignore` está actualizado

## 📚 Estructura del Proyecto

```
scripts/
├── 01_organize_files.py        # Categorización de archivos
├── 02_read_and_redact.py       # Redacción automática (CORE)
├── 03_generate_with_claude.py  # Generación con Claude API
└── run_all.py                  # Orquestador

tests/
├── test_organize.py            # [TODO] Tests de organización
├── test_redact.py              # [TODO] Tests de redacción
└── test_generate.py            # [TODO] Tests de generación

docs/
├── ARQUITECTURA.md             # [TODO] Diseño del sistema
├── PRIVACIDAD.md               # [TODO] Garantías de privacidad
└── TROUBLESHOOTING.md          # [TODO] Solución de problemas
```

## 🎯 Áreas para Contribuir

### Alto Impacto (Buscamos ayuda)
- [ ] Tests unitarios para cada módulo
- [ ] Mejor documentación de redacción
- [ ] Integración con más modelos de Claude
- [ ] Dashboard web simple para ver progreso
- [ ] Exportar a PDF/Word

### Medio Impacto
- [ ] Soporte para más idiomas
- [ ] Más patrones de redacción
- [ ] Optimizar velocidad de procesamiento
- [ ] Logging mejorado

### Bajo Impacto (Nice-to-have)
- [ ] Cambiar esquema de colores
- [ ] Agregar más emojis
- [ ] Documentación en otros idiomas

## 📞 Comunicación

- **Bugs**: Abre un Issue con `[BUG]` en el título
- **Features**: Abre un Issue con `[FEATURE]` en el título
- **Preguntas**: Abre una Discusión

**Formato de Issue:**
```
[TIPO] Título descriptivo

**Descripción:**
Qué está pasando

**Pasos para reproducir:**
1. ...
2. ...

**Resultado esperado:**
...

**Resultado actual:**
...
```

## 🚫 No Hacer

❌ Commit de datos reales  
❌ Cambiar `.gitignore` para permitir datos  
❌ Subir archivos de salida (`outputs/`)  
❌ Hardcodear claves API  
❌ PRs sin describir cambios  

## ✅ Hacer

✅ Usar datos de prueba redactados  
✅ Escribir commits descriptivos  
✅ Probar localmente antes de PR  
✅ Documentar cambios nuevos  
✅ Respetar la privacidad del usuario  

## 🔄 Proceso de Review

1. **Automático**: Verifica que .gitignore está respetado
2. **Automático**: Valida que no hay datos sensibles
3. **Manual**: Un mantenedor revisa el código
4. **Feedback**: Se sugieren cambios si es necesario
5. **Merge**: Se integra a main

## 📖 Recursos

- [README.md](README.md) - Documentación principal
- [Anthropic API Docs](https://docs.anthropic.com)
- [Python Best Practices](https://www.python.org/dev/peps/pep-0008/)

## ❓ Preguntas?

- Abre un Issue
- Crea una Discusión
- Contacta a los mantenedores

---

**¡Gracias por contribuir! 🎉**
