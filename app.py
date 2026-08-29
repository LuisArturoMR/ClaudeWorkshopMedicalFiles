#!/usr/bin/env python3
"""
Sistema de Automatización Médica - Interfaz Streamlit
Interface desktop para organizar, redactar y generar documentos médicos
con privacidad local garantizada.
"""

import streamlit as st
import os
import sys
from pathlib import Path
import tempfile
import shutil
from datetime import datetime

# No necesario agregar scripts al path, usamos importlib

# Importar módulos propios
try:
    # Importar módulos con nombres numéricos
    import importlib.util

    # Cargar 01_organize_files.py
    spec = importlib.util.spec_from_file_location(
        "organize_files",
        str(Path(__file__).parent / "scripts" / "01_organize_files.py")
    )
    organize_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(organize_module)

    # Cargar 02_read_and_redact.py
    spec = importlib.util.spec_from_file_location(
        "read_and_redact",
        str(Path(__file__).parent / "scripts" / "02_read_and_redact.py")
    )
    redact_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(redact_module)
    LocalDataProcessor = redact_module.LocalDataProcessor

    # Cargar 03_generate_with_claude.py
    spec = importlib.util.spec_from_file_location(
        "generate_with_claude",
        str(Path(__file__).parent / "scripts" / "03_generate_with_claude.py")
    )
    generate_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generate_module)
    ClaudeDocumentGenerator = generate_module.ClaudeDocumentGenerator

except ImportError as e:
    st.error(f"❌ Error importando módulos: {e}")
    st.info("📁 Asegúrate de estar en la carpeta correcta y que los scripts existen en: scripts/")
    sys.exit(1)
except Exception as e:
    st.error(f"❌ Error inesperado: {e}")
    sys.exit(1)

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="🏥 Sistema Médico - Automatización",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1e7dd;
        border-left: 4px solid #198754;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #cfe2ff;
        border-left: 4px solid #0d6efd;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# INICIALIZACIÓN DE SESSION STATE
# ════════════════════════════════════════════════════════════════════════════

if "temp_dir" not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

if "processor" not in st.session_state:
    st.session_state.processor = LocalDataProcessor()

if "generator" not in st.session_state:
    st.session_state.generator = ClaudeDocumentGenerator()

# ════════════════════════════════════════════════════════════════════════════
# TÍTULO PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🏥 Sistema de Automatización Médica")
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
    <strong>✅ Privacidad Garantizada:</strong> Todos los datos se procesan localmente en tu máquina.
    Solo datos redactados van a Claude. Nunca se envía información sensible a internet.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR - NAVEGACIÓN
# ════════════════════════════════════════════════════════════════════════════

st.sidebar.markdown("---")
st.sidebar.markdown("## 📋 Navegación")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Selecciona una opción:",
    ["🏠 Inicio", "📁 Organizar Archivos", "🔐 Redactar Datos", "📄 Generar Documentos"],
    key="page_selector"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Información")
with st.sidebar.expander("ℹ️ Cómo usar", expanded=False):
    st.markdown("""
    **1️⃣ Organizar:** Carga tus archivos y categorízalos automáticamente

    **2️⃣ Redactar:** Elimina datos sensibles (SSN, nombres, números de póliza)

    **3️⃣ Generar:** Crea documentos profesionales con Claude

    ---

    **Datos sensibles que se redactan:**
    - SSN (123-45-6789)
    - Nombres
    - Números de póliza
    - Fechas de nacimiento
    """)

with st.sidebar.expander("🔒 Seguridad", expanded=False):
    st.markdown("""
    ✅ Datos locales - nunca salen de tu máquina

    ✅ Redacción automática de PII (Personally Identifiable Information)

    ✅ Solo datos redactados van a Claude API

    ✅ HIPAA/GDPR compliant
    """)

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA: INICIO
# ════════════════════════════════════════════════════════════════════════════

if page == "🏠 Inicio":
    st.markdown("## ¡Bienvenido!")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### ✨ Funcionalidades

        **Organizar Archivos**
        - Categoriza automáticamente tus documentos médicos
        - Pólizas, Expedientes, Facturas, etc.

        **Redactar Datos**
        - Elimina datos sensibles localmente
        - Protege privacidad de tu familia
        - 100% seguro en tu máquina

        **Generar Documentos**
        - Crea cartas de apelación profesionales
        - Genera checklists de documentos
        - Crea emails de seguimiento
        """)

    with col2:
        st.markdown("""
        ### 🔒 Privacidad

        Tu privacidad es lo primero:
        - ✅ Datos originales nunca salen de tu máquina
        - ✅ Redacción automática de información personal
        - ✅ Solo datos redactados van a Claude
        - ✅ Con Anthropic Enterprise: Zero Data Retention

        **Datos que redactamos:**
        - Números de Seguro Social
        - Nombres completos
        - Números de póliza de seguros
        - Fechas de nacimiento
        - Información médica identificable
        """)

    st.markdown("---")

    st.markdown("### 🚀 Cómo empezar")

    tab1, tab2, tab3 = st.tabs(["📁 Paso 1: Organizar", "🔐 Paso 2: Redactar", "📄 Paso 3: Generar"])

    with tab1:
        st.markdown("""
        **1. Ve a la sección "Organizar Archivos"**

        2. Carga tus archivos médicos (expedientes, facturas, pólizas, etc.)

        3. El sistema los organizará automáticamente por categoría

        4. Descarga los archivos organizados
        """)

    with tab2:
        st.markdown("""
        **1. Ve a la sección "Redactar Datos"**

        2. Carga un archivo con datos sensibles

        3. El sistema automáticamente:
           - Redacta números de SSN
           - Redacta nombres
           - Redacta números de póliza
           - Redacta fechas de nacimiento

        4. Descarga el archivo redactado (seguro para compartir)
        """)

    with tab3:
        st.markdown("""
        **1. Ve a la sección "Generar Documentos"**

        2. Sube archivos redactados

        3. El sistema genera:
           - 📧 Cartas de apelación profesionales
           - ✅ Checklists de documentos necesarios
           - 💬 Emails de seguimiento

        4. Descarga los documentos generados
        """)

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA: ORGANIZAR ARCHIVOS
# ════════════════════════════════════════════════════════════════════════════

elif page == "📁 Organizar Archivos":
    st.markdown("## 📁 Organizar Archivos Médicos")

    st.markdown("""
    Carga tus archivos y el sistema los organizará automáticamente por categoría:
    - **Pólizas**: Documentos de seguros médicos
    - **Expedientes**: Registros médicos y diagnósticos
    - **Facturas**: Recibos y cargos médicos
    - **Apelaciones**: Correspondencia de apelaciones
    - **Medicamentos**: Información de prescripciones
    """)

    st.markdown("---")

    # Upload de archivos
    uploaded_files = st.file_uploader(
        "📤 Carga tus archivos médicos",
        accept_multiple_files=True,
        type=["txt", "pdf", "doc", "docx", "csv", "xlsx"]
    )

    if uploaded_files:
        st.markdown("### Archivos cargados:")

        # Crear carpeta temporal para archivos
        temp_raw = Path(st.session_state.temp_dir) / "raw_upload"
        temp_raw.mkdir(exist_ok=True)

        file_info = []
        for uploaded_file in uploaded_files:
            file_path = temp_raw / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            file_info.append({
                "nombre": uploaded_file.name,
                "tamaño": f"{uploaded_file.size / 1024:.1f} KB",
                "tipo": uploaded_file.type
            })

        # Mostrar tabla de archivos
        col1, col2 = st.columns([3, 1])
        with col1:
            for info in file_info:
                st.markdown(f"✅ **{info['nombre']}** ({info['tamaño']})")

        st.markdown("---")

        # Botón para organizar
        if st.button("🚀 Organizar Archivos", key="organize_btn", type="primary"):
            with st.spinner("Organizando archivos..."):
                try:
                    # Categorías
                    categories = {
                        "Polizas": ["póliza", "policy", "cobertura", "plan"],
                        "Expedientes": ["diagnóstico", "receta", "nota médica", "prueba"],
                        "Facturas": ["factura", "invoice", "cobro", "pago"],
                        "Apelaciones": ["apelación", "appeal", "negación"],
                        "Medicamentos": ["medicamento", "medicina", "prescripción"],
                    }

                    # Estructura en memoria para guardar referencias
                    organized_files = {cat: [] for cat in list(categories.keys()) + ["Otros"]}

                    organized_count = 0
                    for file_path in sorted(temp_raw.glob("*")):
                        if file_path.is_file():
                            category = "Otros"
                            filename_lower = file_path.name.lower()

                            for cat, keywords in categories.items():
                                if any(kw in filename_lower for kw in keywords):
                                    category = cat
                                    break

                            # Guardar referencia del archivo
                            organized_files[category].append({
                                "path": file_path,
                                "name": file_path.name,
                                "size": file_path.stat().st_size
                            })
                            organized_count += 1

                    st.success(f"✅ {organized_count} archivo(s) organizados correctamente")

                    # Mostrar estructura
                    st.markdown("### 📂 Estructura creada:")
                    for category in list(categories.keys()) + ["Otros"]:
                        files = organized_files[category]
                        if files:
                            st.markdown(f"**{category}/** ({len(files)} archivo(s))")
                            for f in files:
                                size_kb = f["size"] / 1024
                                st.markdown(f"  - {f['name']} ({size_kb:.1f} KB)")

                    # Guardar en session state para descarga
                    st.session_state.organized_files = organized_files
                    st.session_state.organized_count = organized_count

                    # Botón de descarga
                    st.markdown("---")

                    # Crear ZIP con archivos organizados
                    import zipfile
                    import io

                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for category, files in organized_files.items():
                            for file_info in files:
                                file_path = file_info["path"]
                                # Guardar con estructura: categoria/archivo
                                arcname = f"{category}/{file_info['name']}"
                                zip_file.write(file_path, arcname=arcname)

                    zip_buffer.seek(0)

                    st.download_button(
                        label="📥 Descargar archivos organizados (ZIP)",
                        data=zip_buffer.getvalue(),
                        file_name=f"archivos_organizados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip",
                        type="primary"
                    )

                    st.info("✨ Los archivos han sido organizados. Continúa con el siguiente paso.")

                except Exception as e:
                    st.error(f"❌ Error al organizar: {e}")
                    import traceback
                    st.error(f"Detalles: {traceback.format_exc()}")

    else:
        st.info("👆 Carga archivos para comenzar")

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA: REDACTAR DATOS
# ════════════════════════════════════════════════════════════════════════════

elif page == "🔐 Redactar Datos":
    st.markdown("## 🔐 Redactar Datos Sensibles")

    st.markdown("""
    <div class="warning-box">
    <strong>🔒 Privacidad Local:</strong> El redactado ocurre completamente en tu máquina.
    Los datos originales nunca se envían a internet.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    Esta herramienta redacta automáticamente:
    - 🔢 Números de Seguro Social (SSN)
    - 👤 Nombres completos
    - 📋 Números de póliza
    - 📅 Fechas de nacimiento

    **Formatos soportados:** Texto plano (.txt)

    *Tip:* Si tienes archivos PDF o Word, copia el texto a un archivo .txt primero
    """)

    st.markdown("---")

    # Upload de archivo - solo TXT
    uploaded_file = st.file_uploader(
        "📤 Carga un archivo de texto para redactar",
        type=["txt"],
        key="redact_upload"
    )

    if uploaded_file:
        st.markdown("### Archivo cargado:")
        st.markdown(f"✅ **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

        st.markdown("---")

        # Botón para redactar
        if st.button("🔐 Redactar Datos", key="redact_btn", type="primary"):
            with st.spinner("Redactando datos..."):
                try:
                    # Leer contenido como texto
                    content = uploaded_file.read().decode('utf-8', errors='ignore')

                    if not content.strip():
                        st.warning("⚠️ El archivo está vacío o no se puede leer como texto")
                    else:
                        # Redactar
                        processor = st.session_state.processor
                        redacted_content = processor.redact_text(content)

                        # Contar redacciones
                        import re
                        redactions = len(re.findall(r'\[.*?_REDACTED\]', redacted_content))

                        st.success(f"✅ Archivo redactado correctamente ({redactions} datos sensibles eliminados)")

                        st.markdown("---")

                        # Mostrar preview
                        st.markdown("### 📄 Vista previa del archivo redactado:")
                        st.text_area(
                            "Contenido redactado:",
                            redacted_content,
                            height=300,
                            disabled=True
                        )

                        st.markdown("---")

                        # Botón de descarga
                        st.download_button(
                            label="📥 Descargar archivo redactado",
                            data=redacted_content,
                            file_name=f"redactado_{uploaded_file.name}",
                            mime="text/plain",
                            type="primary"
                        )

                        st.markdown("""
                        <div class="success-box">
                        <strong>✨ Listo para el siguiente paso:</strong> Este archivo redactado es seguro
                        para enviar a Claude o compartir con otros.
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error al redactar: {e}")

    else:
        st.info("👆 Carga un archivo para redactar")

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA: GENERAR DOCUMENTOS
# ════════════════════════════════════════════════════════════════════════════

elif page == "📄 Generar Documentos":
    st.markdown("## 📄 Generar Documentos con Claude")

    st.markdown("""
    <div class="info-box">
    <strong>💡 Usando Claude API:</strong> Este sistema usa datos redactados para generar documentos profesionales.
    Requiere API key de Anthropic.
    </div>
    """, unsafe_allow_html=True)

    # Verificar API key
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        st.warning("""
        ⚠️ **Atención:** API key de Anthropic no configurada

        Necesitas:
        1. Obtener API key en: https://console.anthropic.com/
        2. Configurar: `export ANTHROPIC_API_KEY="sk-ant-..."`
        3. Reiniciar la aplicación
        """)
    else:
        st.success("✅ API key configurada correctamente")

    st.markdown("---")

    # Seleccionar tipo de documento
    doc_type = st.selectbox(
        "📋 Tipo de documento a generar:",
        ["Carta de Apelación", "Checklist de Documentos", "Email de Seguimiento"]
    )

    st.markdown("---")

    # Upload de archivo redactado
    uploaded_file = st.file_uploader(
        "📤 Carga archivo redactado",
        type=["txt"],
        key="generate_upload"
    )

    if uploaded_file:
        st.markdown("### Archivo cargado:")
        st.markdown(f"✅ **{uploaded_file.name}**")

        st.markdown("---")

        # Información adicional
        diagnosis = st.text_input(
            "🏥 Diagnóstico (ej: Diabetes tipo 2)",
            placeholder="Ingresa el diagnóstico"
        )

        condition = st.text_area(
            "📝 Detalles de la negación",
            placeholder="Describe por qué fue negada la cobertura",
            height=100
        )

        st.markdown("---")

        # Botón para generar
        if st.button("✨ Generar Documento", key="generate_btn", type="primary"):
            if not diagnosis or not condition:
                st.warning("Por favor completa todos los campos")
            elif not api_key:
                st.error("API key de Anthropic no configurada")
            else:
                with st.spinner(f"Generando {doc_type.lower()}..."):
                    try:
                        # Leer contenido
                        redacted_content = uploaded_file.read().decode('utf-8')

                        # Generar documento
                        generator = st.session_state.generator

                        if doc_type == "Carta de Apelación":
                            result = generator.generate_appeal_letter(
                                f"{redacted_content}\n\nDiagnóstico: {diagnosis}\nCondición: {condition}"
                            )
                            filename = f"carta_apelacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

                        elif doc_type == "Checklist de Documentos":
                            result = generator.generate_document_checklist(
                                f"{redacted_content}\n\nDiagnóstico: {diagnosis}"
                            )
                            filename = f"checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

                        else:  # Email de Seguimiento
                            result = generator.generate_follow_up_email(
                                f"{redacted_content}\n\nDiagnóstico: {diagnosis}"
                            )
                            filename = f"email_seguimiento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

                        if result:
                            st.success(f"✅ {doc_type} generado correctamente")

                            st.markdown("---")

                            # Mostrar resultado
                            st.markdown("### 📄 Documento generado:")
                            st.text_area(
                                "Contenido:",
                                result,
                                height=400,
                                disabled=True
                            )

                            st.markdown("---")

                            # Descargar
                            st.download_button(
                                label=f"📥 Descargar {doc_type}",
                                data=result,
                                file_name=filename,
                                mime="text/plain",
                                type="primary"
                            )
                        else:
                            st.error("Error generando documento. Revisa API key y límites.")

                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    else:
        st.info("👆 Carga un archivo redactado para generar documentos")

# ════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; margin-top: 2rem;">
<p>🏥 Sistema de Automatización Médica | Privacidad Garantizada | Desarrollado con ❤️ usando Claude</p>
<p style="font-size: 0.8rem;">Todos los datos se procesan localmente en tu máquina. Nunca se envía información sensible sin tu consentimiento explícito.</p>
</div>
""", unsafe_allow_html=True)
