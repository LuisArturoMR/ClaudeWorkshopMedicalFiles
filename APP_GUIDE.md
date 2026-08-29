# 📖 Guía Visual - Interfaz de Desktop

## 🎯 Descripción General

La aplicación Streamlit proporciona una interfaz visual fácil de usar para:
1. Organizar archivos médicos
2. Redactar datos sensibles automáticamente
3. Generar documentos profesionales

## 🖼️ Pantallas de la Aplicación

### Pantalla Principal
```
┌─────────────────────────────────────────────────────────┐
│ 🏥 Sistema de Automatización Médica                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ✅ Privacidad Garantizada:                             │
│ Todos los datos se procesan localmente. Solo datos     │
│ redactados van a Claude. Nunca se envía información    │
│ sensible a internet.                                    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ [🏠 Inicio] [📁 Organizar] [🔐 Redactar] [📄 Generar] │
└─────────────────────────────────────────────────────────┘
```

### Barra Lateral
```
┌──────────────────────┐
│ 📋 Navegación       │
├──────────────────────┤
│ ○ 🏠 Inicio         │
│ ○ 📁 Organizar      │
│ ○ 🔐 Redactar       │
│ ○ 📄 Generar        │
├──────────────────────┤
│ 📚 Información       │
│ ▼ ℹ️ Cómo usar      │
│ ▼ 🔒 Seguridad      │
└──────────────────────┘
```

## 📄 Seccion 1: Inicio

Página de bienvenida con:
- Descripción de funcionalidades
- Información de seguridad
- Tutorial paso a paso
- Links a documentación

**Objetivo:** Informar al usuario sobre qué puede hacer

## 📁 Sección 2: Organizar Archivos

### Funcionalidad
Carga archivos médicos y los organiza automáticamente por categoría.

### Flujo
```
Usuario carga archivos
        ↓
Sistema identifica categoría
        ↓
Se organizan en carpetas:
  • Pólizas/
  • Expedientes/
  • Facturas/
  • Apelaciones/
  • Medicamentos/
        ↓
Usuario descarga estructura
```

### Interfaz
```
Organizar Archivos
├─ Input: Drag & drop o click para seleccionar
│  ├─ expediente_medico.txt
│  ├─ factura.txt
│  └─ póliza.txt
│
├─ Botón: [🚀 Organizar Archivos]
│
└─ Output: Estructura creada
   ├─ Expedientes/ (1 archivo)
   ├─ Facturas/ (1 archivo)
   └─ Polizas/ (1 archivo)
```

## 🔐 Sección 3: Redactar Datos

### Funcionalidad
Sube un archivo con datos sensibles y automáticamente redacta:
- SSN: `123-45-6789` → `[SSN_REDACTED]`
- Nombres: `Juan García` → `[PATIENT_NAME]`
- Pólizas: `BCBS-789456` → `[POLICY_ID]`
- Fechas: `03/15/1948` → `[DOB]`

### Flujo
```
Usuario sube archivo
        ↓
Sistema lee contenido localmente
        ↓
Redacta automáticamente
        ↓
Muestra preview
        ↓
Usuario descarga archivo redactado
        ↓
Archivo seguro para enviar a Claude
```

### Interfaz
```
Redactar Datos
├─ Información de seguridad (Local)
│
├─ Input: Sube archivo
│  └─ expediente_medico.txt (45 KB)
│
├─ Botón: [🔐 Redactar Datos]
│
├─ Resultado:
│  ✅ Archivo redactado (12 datos eliminados)
│
├─ Preview: Área de texto con contenido redactado
│  Muestra primeros ~300 caracteres
│
└─ Botón: [📥 Descargar archivo redactado]
```

## 📄 Sección 4: Generar Documentos

### Funcionalidad
Usa Claude API para generar documentos profesionales.

### Tipos de documentos
1. **Carta de Apelación**
   - Documento formal para apelar negaciones
   - Estructura profesional
   - Argumentos médicos

2. **Checklist de Documentos**
   - Lista de qué documentos son necesarios
   - Descripción de cada uno
   - Explicación de importancia

3. **Email de Seguimiento**
   - Email profesional para seguimiento
   - Tone formal pero cortés
   - Referencia a póliza y apelación

### Flujo
```
Usuario sube archivo redactado
        ↓
Selecciona tipo de documento
        ↓
Ingresa diagnóstico y detalles
        ↓
Envía datos redactados a Claude
        ↓
Claude genera documento
        ↓
Muestra resultado
        ↓
Usuario descarga documento
```

### Interfaz
```
Generar Documentos
├─ Nota: Requiere API key configurada
│
├─ Selector: Tipo de documento
│  ○ Carta de Apelación
│  ○ Checklist de Documentos
│  ○ Email de Seguimiento
│
├─ Input: Archivo redactado
│  └─ redactado_expediente.txt
│
├─ Campos de entrada:
│  └─ Diagnóstico: [Diabetes tipo 2]
│  └─ Detalles: [Negación de cobertura...]
│
├─ Botón: [✨ Generar Documento]
│
├─ Resultado:
│  ✅ Carta de apelación generada
│
├─ Preview: Área de texto con documento
│
└─ Botón: [📥 Descargar Carta de Apelación]
```

## 🎨 Elementos Visuales

### Colores y Diseño
- **Fondo**: Blanco limpio
- **Botones principales**: Azul (#0d6efd)
- **Éxito**: Verde (#198754)
- **Advertencia**: Amarillo (#ffc107)
- **Info**: Azul claro (#0d6efd)

### Cajas de Información
```
✅ Éxito (Verde)
Archivo redactado correctamente (12 datos eliminados)

ℹ️ Información (Azul)
Todos los datos se procesan localmente en tu máquina

⚠️ Advertencia (Amarillo)
API key de Anthropic no configurada

🔒 Privacidad (Verde)
Solo datos redactados van a Claude API
```

## 🔄 Workflow Completo

### Ejemplo: Automatizar apelación médica

**Paso 1: Organizar (5 min)**
- Carga: expediente, factura, póliza, negación
- Se organizan automáticamente
- Descarga archivos organizados

**Paso 2: Redactar (2 min)**
- Sube expediente con datos reales
- Sistema redacta automáticamente
- Descarga versión segura

**Paso 3: Generar (3 min)**
- Sube expediente redactado
- Selecciona "Carta de Apelación"
- Ingresa diagnóstico
- Genera y descarga

**Total: 10 minutos** 🎯

## 💾 Gestión de Archivos

### Tipos soportados
- Texto: `.txt`
- PDF: `.pdf`
- Word: `.doc`, `.docx`
- Spreadsheet: `.csv`, `.xlsx`

### Ubicación
- **Subidas**: Se procesan localmente
- **Descargas**: Archivos procesados
- **Temporal**: Limpiado automáticamente

## 🔐 Seguridad en UI

### Indicadores
- ✅ = Acción exitosa
- ⚠️ = Requiere atención
- ❌ = Error

### Validaciones
- Verifica API key antes de generar
- Valida campos requeridos
- Muestra errores claros
- Nunca guarda datos reales

## 🚀 Características Futuras

### Próximas mejoras
- [ ] Exportar a PDF con formato
- [ ] Historial de documentos
- [ ] Presets de diagnósticos
- [ ] Visualización de redacciones
- [ ] Batch processing
- [ ] Integración con cloud storage
- [ ] Soporte multiidioma

---

## 📝 Notas

- La interfaz es responsiva (se adapta a cualquier tamaño)
- Funciona en navegador (http://localhost:8501)
- Se puede usar offline excepto para generar con Claude
- Todos los datos se quedan en tu máquina
- Compatible con Windows, macOS, Linux

---

**¡Interfaz lista para usar!** 🎉
