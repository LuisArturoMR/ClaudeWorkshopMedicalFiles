# 🏥 Sistema de Automatización Médica - Privacidad Local

Un sistema completo que organiza archivos médicos, redacta datos sensibles **localmente**, y genera documentos automáticamente con Claude, con interfaz desktop fácil de usar.

## 🔒 Privacidad

✅ **Archivos originales** se quedan en tu máquina  
✅ **Datos redactados** son lo único que ve Claude  
✅ **Nada sale a internet** sin tu control  
✅ **HIPAA/GDPR ready** - Cumple con regulaciones

## 🎯 ¿Qué Hace?

### 📁 Organizar
Categoriza automáticamente tus archivos médicos (pólizas, expedientes, facturas)

### 🔐 Redactar
Elimina datos sensibles localmente (SSN, nombres, números de póliza)

### 📄 Generar
Crea documentos profesionales automáticamente:
- Cartas de apelación
- Checklists de documentos
- Emails de seguimiento  

## 📁 Estructura

```
medical_automation/
├── raw_data/              ← Tus archivos originales (PRIVADOS)
├── organized_data/        ← Archivos organizados por categoría
├── for_claude/           ← Archivos redactados (LISTOS PARA CLAUDE)
├── outputs/              ← Documentos generados
└── scripts/              ← Scripts Python
    ├── 01_organize_files.py
    ├── 02_read_and_redact.py
    ├── 03_generate_with_claude.py
    └── run_all.py (ejecuta todo)
```

## 🚀 Instalación y Uso

### Opción A: Interfaz Desktop (Recomendado) ⭐

#### 1. Requisitos
```bash
python3 --version  # Python 3.8+
```

#### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 3. Ejecutar interfaz
```bash
# Forma rápida (macOS/Linux):
./run_app.sh

# O manualmente:
streamlit run app.py
```

Se abre automáticamente en: `http://localhost:8501`

### Opción B: Scripts por línea de comandos

#### 1. Instalar
```bash
pip install -r requirements.txt
```

#### 2. Configurar API (opcional)
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

#### 3. Ejecutar
```bash
cd medical_automation
python3 scripts/run_all.py
```

## 📋 Proceso Paso a Paso

### **PASO 1: Organizar Archivos**
```bash
python3 scripts/01_organize_files.py
```
- Lee: `raw_data/` (tus archivos originales)
- Sale: `organized_data/` con carpetas por categoría
  - Pólizas/
  - Expedientes/
  - Facturas/
  - Apelaciones/
  - Medicamentos/

### **PASO 2: Leer Localmente + Redactar**
```bash
python3 scripts/02_read_and_redact.py
```
- Lee: `organized_data/` (en tu máquina, localmente)
- Redacta: Juan García → [PATIENT_NAME]
- Redacta: SSN 123-45-6789 → [SSN_REDACTED]
- Redacta: Póliza BCBS-789456 → [POLICY_ID]
- Sale: `for_claude/` (SEGURO para enviar a Claude)

**⚠️ IMPORTANTE**: Solo archivos redactados van a Claude. Los originales NO salen.

### **PASO 3: Generar Documentos**
```bash
python3 scripts/03_generate_with_claude.py
```
- Lee: `for_claude/` (datos redactados)
- Envía a Claude: "Genera carta de apelación"
- Sale: `outputs/`
  - `*_CARTA_APELACION.txt`
  - `*_CHECKLIST.txt`
  - `*_EMAIL_SEGUIMIENTO.txt`

### **TODO JUNTO**
```bash
python3 scripts/run_all.py
```

## 🔧 Personalización

### Agregar Tus Archivos

```bash
# Coloca tus archivos en:
cp /ruta/mis/archivos/* medical_automation/raw_data/

# Luego ejecuta:
python3 scripts/run_all.py
```

### Cambiar Reglas de Redacción

Edita `02_read_and_redact.py` - sección `redaction_map`:

```python
self.redaction_map = {
    r"TU_NOMBRE": "[PATIENT_NAME]",
    r"TU_NUMERO": "[ID_REDACTED]",
    # Agrega más según necesites
}
```

### Cambiar Categorías de Archivos

Edita `01_organize_files.py` - sección `CATEGORIES`:

```python
CATEGORIES = {
    "Tu_Categoria": ["palabra_clave1", "palabra_clave2"],
    # Agrega más según necesites
}
```

## 📊 Ejemplo Completo

**Entrada (raw_data/):**
```
expediente_medico.txt:
  Paciente: Juan García
  SSN: 123-45-6789
  Póliza: BCBS-789456
```

**Proceso:**
1. ✅ Se organiza en `organized_data/Expedientes/`
2. ✅ Se redacta a:
```
[PATIENT_NAME]
[SSN_REDACTED]
[POLICY_ID]
```
3. ✅ Se guarda en `for_claude/Expedientes/`
4. ✅ Claude recibe datos limpios
5. ✅ Genera: Carta de apelación, Checklist, Email de seguimiento
6. ✅ Guardados en `outputs/`

## 🔐 Seguridad - Preguntas Frecuentes

**P: ¿Mis datos van a Internet?**
A: No. Datos originales se quedan en tu máquina. Solo versiones redactadas van a Claude.

**P: ¿Qué pasa si la redacción falla?**
A: Revisa manualmente antes de enviar a Claude. El archivo está en `for_claude/` - puedes editarlo.

**P: ¿Pueden recuperar mis datos?**
A: No. Con data retention=0 (Enterprise) o redacción completa, no hay forma.

**P: ¿Qué hago si no quiero usar Claude?**
A: Usa solo los Pasos 1-2. Tendrás archivos organizados y redactados localmente.

## 📞 Soporte

Problemas comunes:
- `ModuleNotFoundError: anthropic` → `pip install anthropic`
- `ANTHROPIC_API_KEY not configured` → `export ANTHROPIC_API_KEY="..."`
- Archivos no se organizan → Revisa nombres con palabras clave en `CATEGORIES`

## 📝 Próximos Pasos

- [ ] Coloca tus archivos en `raw_data/`
- [ ] Ejecuta `python3 scripts/run_all.py`
- [ ] Revisa `outputs/` para documentos generados
- [ ] Personaliza redacción según tus datos
- [ ] Integra con tu flujo de seguros médicos

---

**Construido para privacidad. Diseñado para automatización.**
