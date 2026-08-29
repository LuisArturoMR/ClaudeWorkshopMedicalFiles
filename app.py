#!/usr/bin/env python3
"""
Sistema de Automatización Médica - Interfaz Streamlit
Interface desktop para organizar, redactar y generar documentos médicos
con privacidad local garantizada.
"""

# ⚠️ CARGAR .env PRIMERO (antes de cualquier otra cosa)
from dotenv import load_dotenv
load_dotenv()

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
    page_title="CustodIA - Automatización Médica",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado - Diseño tipo CustodIA
st.markdown("""
<style>
    :root {
        --primary-color: #1a7a7a;
        --secondary-color: #2a9d9d;
        --light-bg: #f5f5f5;
        --text-dark: #1f1f1f;
    }

    .main {
        padding: 0rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #e0e0e0;
    }

    /* Sidebar menu items */
    [data-testid="stSidebar"] .stRadio > label {
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s;
        color: #1f1f1f !important;
    }

    [data-testid="stSidebar"] .stRadio > label:hover {
        background-color: #f0f0f0;
        color: #1f1f1f !important;
    }

    /* Sidebar text color */
    [data-testid="stSidebar"] {
        color: #1f1f1f !important;
    }

    [data-testid="stSidebar"] span {
        color: #1f1f1f !important;
    }

    /* Section headers */
    .section-header {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        color: #999;
        text-transform: uppercase;
        margin: 1.5rem 0 1rem 0;
        padding-left: 1rem;
    }

    /* Success box */
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

    /* Feature cards */
    .feature-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s;
    }

    .feature-card:hover {
        border-color: #1a7a7a;
        box-shadow: 0 2px 8px rgba(26, 122, 122, 0.1);
    }

    .feature-number {
        color: #1a7a7a;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .feature-title {
        color: #1f1f1f;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: #666;
        font-size: 0.9rem;
    }

    /* Main title */
    .main-title {
        color: #1f1f1f;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0;
        line-height: 1.2;
    }

    .main-subtitle {
        color: #1a7a7a;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1rem;
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab-list"] button {
        border-bottom: 2px solid transparent;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom-color: #1a7a7a;
        color: #1a7a7a;
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
# SIDEBAR - NAVEGACIÓN (Diseño CustodIA)
# ════════════════════════════════════════════════════════════════════════════

# Logo en sidebar - Usar ruta correcta
from PIL import Image
try:
    logo = Image.open("logo.jpeg")
    st.sidebar.image(logo, use_column_width=True)
except:
    st.sidebar.markdown("### 📋 CustodIA")

# Navegación principal
st.sidebar.markdown('<div class="section-header">Espacio de Trabajo</div>', unsafe_allow_html=True)

page = st.sidebar.radio(
    "Selecciona una opción:",
    ["🏠 Inicio", "📁 Organizar Archivos", "🔐 Redactar Datos", "🤖 Automatizaciones"],
    key="page_selector",
    label_visibility="collapsed"
)

# Información
st.sidebar.markdown('<div class="section-header">Información</div>', unsafe_allow_html=True)

with st.sidebar.expander("❓ Cómo usar", expanded=False):
    st.markdown("""
    **1️⃣ Organizar:** Carga tus archivos y categorízalos automáticamente

    **2️⃣ Redactar:** Elimina datos sensibles (SSN, nombres, números de póliza)

    **3️⃣ Automatizar:** Genera documentos o chatea con Claude

    ---

    **Datos que protegemos:**
    - SSN y Seguro Social
    - Nombres y documentos
    - Números de póliza
    - Información bancaria
    """)

with st.sidebar.expander("🔐 Seguridad", expanded=False):
    st.markdown("""
    ✅ **Procesamiento local** - Datos nunca salen de tu máquina

    ✅ **Redacción automática** - Reemplaza PHI/PII con tokens

    ✅ **Solo datos seguros** - Solo redactados van a Claude

    ✅ **Cumplimiento** - HIPAA, GDPR compatible
    """)

# Indicador de procesamiento local
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding: 1rem; background-color: #f0f0f0; border-radius: 0.5rem; margin-top: 2rem;">
    <div style="color: #1a7a7a; font-weight: 600; margin-bottom: 0.5rem;">
        ✓ PROCESAMIENTO LOCAL
    </div>
    <div style="font-size: 0.85rem; color: #666;">
        Tus archivos nunca salen de este dispositivo.
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TÍTULO PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

# Espacio en blanco para que no quede pegado al sidebar
st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA: INICIO
# ════════════════════════════════════════════════════════════════════════════

if page == "🏠 Inicio":
    # Título y descripción
    st.markdown("### CONFIANZA Y PRIVACIDAD")
    st.markdown("# Seguridad sin concesiones")
    st.markdown("""
    Diseñado para mantener el control de la información clínica donde pertenece: contigo.
    """)

    st.markdown("---")

    # Características principales
    st.markdown("## ¿Cómo funciona?")

    # Usar 2 columnas para las 4 tarjetas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">01</div>
            <div class="feature-title">Procesamiento estrictamente local</div>
            <div class="feature-description">
            Una capa de protección clara y verificable, pensada para documentación sensible.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">02</div>
            <div class="feature-title">Redacción antes de cualquier generación</div>
            <div class="feature-description">
            Una capa de protección clara y verificable, pensada para documentación sensible.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">03</div>
            <div class="feature-title">Zero data retention en integraciones empresariales</div>
            <div class="feature-description">
            Una capa de protección clara y verificable, pensada para documentación sensible.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">04</div>
            <div class="feature-title">Cifrado durante las transferencias autorizadas</div>
            <div class="feature-description">
            Una capa de protección clara y verificable, pensada para documentación sensible.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🚀 Cómo empezar")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **📁 Paso 1: Organizar**

        Carga tus documentos médicos y el sistema los categoriza automáticamente.
        """)

    with col2:
        st.markdown("""
        **🔐 Paso 2: Redactar**

        Elimina automáticamente datos sensibles (SSN, nombres, pólizas).
        """)

    with col3:
        st.markdown("""
        **🤖 Paso 3: Automatizar**

        Genera documentos o chatea con Claude usando solo datos redactados.
        """)

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA: ORGANIZAR ARCHIVOS
# ════════════════════════════════════════════════════════════════════════════

elif page == "📁 Organizar Archivos":
    st.markdown("## 📁 Organizar Archivos Médicos")

    # Crear directorio persistente para archivos organizados
    ORGANIZED_DIR = Path("organized_files")
    ORGANIZED_DIR.mkdir(exist_ok=True)

    st.markdown("""
    Carga tus archivos y el sistema los organizará automáticamente por categoría:
    - **Pólizas**: Documentos de seguros médicos
    - **Expedientes**: Registros médicos y diagnósticos
    - **Facturas**: Recibos y cargos médicos
    - **Apelaciones**: Correspondencia de apelaciones
    - **Medicamentos**: Información de prescripciones
    """)

    st.markdown("---")

    # Mostrar archivos ya organizados
    st.markdown("### 📂 Archivos Organizados (Almacenados):")

    all_organized = {}
    for category_dir in sorted(ORGANIZED_DIR.iterdir()):
        if category_dir.is_dir():
            files = list(category_dir.glob("*"))
            if files:
                all_organized[category_dir.name] = files

    if all_organized:
        for category, files in all_organized.items():
            with st.expander(f"**{category}** ({len(files)} archivo(s))", expanded=False):
                for f in files:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"📄 {f.name}")
                    with col2:
                        if st.button("🗑️", key=f"delete_{f}", help="Eliminar"):
                            f.unlink()
                            st.success(f"Eliminado: {f.name}")
                            st.rerun()
    else:
        st.info("📭 No hay archivos organizados aún. Carga algunos arriba.")

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

                    # Crear carpetas persistentes
                    for category in list(categories.keys()) + ["Otros"]:
                        (ORGANIZED_DIR / category).mkdir(exist_ok=True)

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

                            # Copiar archivo a carpeta persistente
                            dest_path = ORGANIZED_DIR / category / file_path.name
                            if not dest_path.exists():
                                shutil.copy2(file_path, dest_path)

                            organized_files[category].append({
                                "path": dest_path,
                                "name": file_path.name,
                                "size": dest_path.stat().st_size
                            })
                            organized_count += 1

                    st.success(f"✅ {organized_count} archivo(s) organizados y guardados")

                    # Mostrar estructura
                    st.markdown("### 📂 Estructura creada:")
                    for category in list(categories.keys()) + ["Otros"]:
                        files = organized_files[category]
                        if files:
                            st.markdown(f"**{category}/** ({len(files)} archivo(s))")
                            for f in files:
                                size_kb = f["size"] / 1024
                                st.markdown(f"  - {f['name']} ({size_kb:.1f} KB)")

                    # Guardar en session state
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

                    st.info("✨ Los archivos han sido organizados y guardados. Continúa con el siguiente paso.")

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

    # Crear directorio persistente si no existe
    ORGANIZED_DIR = Path("organized_files")
    ORGANIZED_DIR.mkdir(exist_ok=True)

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

    **Formatos soportados:** Texto (.txt) y PDF
    """)

    st.markdown("---")

    # Recolectar todos los archivos organizados
    available_files = {}
    for category_dir in sorted(ORGANIZED_DIR.iterdir()):
        if category_dir.is_dir():
            for file_path in sorted(category_dir.glob("*")):
                if file_path.is_file():
                    display_name = f"{category_dir.name} / {file_path.name}"
                    available_files[display_name] = file_path

    # Opción 1: Seleccionar de archivos organizados
    if available_files:
        st.markdown("### 📂 Opción 1: Seleccionar de Archivos Organizados")
        selected_file = st.selectbox(
            "Elige un archivo para redactar:",
            options=available_files.keys(),
            key="select_organized_file"
        )

        if st.button("📖 Cargar Archivo Seleccionado", key="load_organized_btn", type="primary"):
            uploaded_file = available_files[selected_file]
            # Leer el archivo seleccionado
            with open(uploaded_file, 'rb') as f:
                file_content = f.read()

            # Crear un objeto tipo file para compatibilidad
            class FileObj:
                def __init__(self, name, content):
                    self.name = name
                    self.size = len(content)
                    self._content = content

                def read(self):
                    return self._content

            uploaded_file = FileObj(uploaded_file.name, file_content)
            st.session_state.loaded_file = uploaded_file
            st.success(f"✅ Archivo cargado: {selected_file}")

        st.markdown("---")
        st.markdown("### 📤 Opción 2: Cargar Nuevo Archivo")
    else:
        st.info("📭 No hay archivos organizados. Primero organiza archivos en la sección anterior.")

    # Upload de archivo nuevo
    uploaded_file_new = st.file_uploader(
        "📤 O carga un nuevo archivo para redactar",
        type=["txt", "pdf"],
        key="redact_upload"
    )

    # Usar archivo cargado (ya sea del selectbox o del uploader)
    uploaded_file = st.session_state.get("loaded_file") or uploaded_file_new

    if uploaded_file:
        st.markdown("### Archivo cargado:")
        st.markdown(f"✅ **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

        st.markdown("---")

        # Botón para redactar
        if st.button("🔐 Redactar Datos", key="redact_btn", type="primary"):
            with st.spinner("Redactando datos..."):
                try:
                    # Detectar tipo de archivo y extraer contenido
                    file_extension = uploaded_file.name.lower().split('.')[-1]

                    if file_extension == 'pdf':
                        # Procesar PDF
                        import pdfplumber
                        import io

                        pdf_bytes = uploaded_file.read()
                        pdf_file = io.BytesIO(pdf_bytes)

                        with pdfplumber.open(pdf_file) as pdf:
                            content = ""
                            for page_num, page in enumerate(pdf.pages, 1):
                                text = page.extract_text()
                                if text:
                                    content += f"--- Página {page_num} ---\n{text}\n\n"

                        st.info(f"📄 Extrayendo texto de {len(pdf.pages)} páginas...")
                    else:
                        # Procesar archivo de texto
                        content = uploaded_file.read().decode('utf-8', errors='ignore')

                    if not content.strip():
                        st.warning("⚠️ El archivo está vacío o no se puede extraer texto")
                    else:
                        processor = st.session_state.processor

                        # Detectar datos sensibles ANTES de redactar
                        st.markdown("### 🔍 Datos Sensibles Detectados:")
                        findings = processor.detect_sensitive_data(content)

                        if findings:
                            import pandas as pd
                            df = pd.DataFrame(findings)
                            st.dataframe(
                                df,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "tipo": st.column_config.TextColumn("Tipo de Dato"),
                                    "valor_original": st.column_config.TextColumn("Valor Original"),
                                    "posicion": st.column_config.TextColumn("Posición")
                                }
                            )
                            st.info(f"📊 Se encontraron **{len(findings)}** datos sensibles")
                        else:
                            st.info("✅ No se detectaron datos sensibles")

                        st.markdown("---")

                        # Tokenizar (crear tokens [[LABEL#NNNN]])
                        mutilated_content = processor.tokenize_text(content)

                        # Mostrar texto "mutilado"
                        st.markdown("### 📝 Texto Mutilado (para Claude):")
                        st.code(mutilated_content if mutilated_content else "(vacío)", language="text")

                        # Mostrar tabla de tokens
                        tokens = processor.vault.get_all_tokens()
                        if tokens:
                            st.markdown("### 🔐 Inventario de Tokens:")
                            import pandas as pd
                            tokens_df = pd.DataFrame(tokens)
                            st.dataframe(
                                tokens_df,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "token": st.column_config.TextColumn("Token", width="medium"),
                                    "tipo": st.column_config.TextColumn("Tipo"),
                                    "valor_original": st.column_config.TextColumn("Valor Original")
                                }
                            )

                        st.success(f"✅ Archivo tokenizado ({len(tokens)} tokens generados)")

                        st.markdown("---")

                        # Botón para "Revelar" (rehydrate) - mostrar valores originales
                        if tokens and st.button("🔍 Revelar Valores Originales", key="reveal_btn"):
                            st.warning("⚠️ PHI en claro - visible solo en esta sesión de RAM")
                            revealed = []
                            for token_info in tokens:
                                revealed.append({
                                    "Token": token_info["token"],
                                    "Tipo": token_info["tipo"],
                                    "Valor Original": token_info["valor_original"]
                                })
                            import pandas as pd
                            st.dataframe(
                                pd.DataFrame(revealed),
                                use_container_width=True,
                                hide_index=True
                            )

                        st.markdown("---")

                        # Botón de descarga - archivo mutilado como .txt
                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        st.download_button(
                            label="📥 Descargar archivo mutilado (.txt)",
                            data=mutilated_content,
                            file_name=f"mutilado_{base_name}.txt",
                            mime="text/plain",
                            type="primary"
                        )

                        st.markdown("""
                        <div class="success-box">
                        <strong>✨ Listo para el siguiente paso:</strong> Este archivo con tokens
                        es seguro para enviar a Claude. Los datos originales quedan solo en esta sesión de RAM.
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error al redactar: {e}")

    else:
        st.info("👆 Carga un archivo para redactar")

# ════════════════════════════════════════════════════════════════════════════
# PÁGINA: AUTOMATIZACIONES (Con Chat)
# ════════════════════════════════════════════════════════════════════════════

elif page == "🤖 Automatizaciones":
    st.markdown("## 🤖 Automatizaciones con Claude")

    st.markdown("""
    <div class="info-box">
    <strong>💬 Chat Inteligente:</strong> Interactúa con Claude usando solo tus documentos redactados (sin PHI/PII).
    Los datos originales nunca se envían.
    </div>
    """, unsafe_allow_html=True)

    # Crear directorio para documentos generados
    GENERATED_DIR = Path("generated_documents")
    GENERATED_DIR.mkdir(exist_ok=True)

    # Verificar API key
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        st.warning("""
        ⚠️ **API key no configurada**
        1. Obtener en: https://console.anthropic.com/
        2. Crear archivo `.env` con: `ANTHROPIC_API_KEY=sk-ant-...`
        """)
    else:
        st.success("✅ API key configurada")

    st.markdown("---")

    # Mostrar documentos generados previamente
    st.markdown("### 📂 Documentos Guardados Localmente:")

    generated_files = list(GENERATED_DIR.glob("*.txt"))
    if generated_files:
        for f in sorted(generated_files):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"📄 {f.name} ({f.stat().st_size / 1024:.1f} KB)")
            with col2:
                if st.button("🗑️", key=f"delete_gen_{f}"):
                    f.unlink()
                    st.success(f"Eliminado: {f.name}")
                    st.rerun()
    else:
        st.info("📭 No hay documentos guardados")

    st.markdown("---")

    # Tabs: Chat vs Generador
    tab_chat, tab_generator = st.tabs(["💬 Chat", "📋 Generador de Documentos"])

    with tab_chat:
        st.markdown("### 💬 Chat con Claude (Documentos Redactados)")

        # Seleccionar documentos redactados
        ORGANIZED_DIR = Path("organized_files")
        available_files = {}
        for category_dir in sorted(ORGANIZED_DIR.iterdir()) if ORGANIZED_DIR.exists() else []:
            if category_dir.is_dir():
                for file_path in sorted(category_dir.glob("*")):
                    if file_path.is_file():
                        display_name = f"{category_dir.name} / {file_path.name}"
                        available_files[display_name] = file_path

        if available_files:
            selected_docs = st.multiselect(
                "📁 Selecciona documentos para el contexto:",
                options=available_files.keys(),
                key="chat_docs"
            )

            if selected_docs and api_key:
                # Inicializar chat history
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []

                # Mostrar conversación
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

                # Input del usuario
                user_input = st.chat_input("Escribe tu pregunta o solicitud...")

                if user_input:
                    # Agregar mensaje del usuario
                    st.session_state.chat_history.append({"role": "user", "content": user_input})

                    with st.chat_message("user"):
                        st.markdown(user_input)

                    # Procesar con Claude
                    with st.chat_message("assistant"):
                        with st.spinner("Claude está pensando..."):
                            try:
                                # Cargar documentos seleccionados
                                docs_dict = {}
                                for display_name in selected_docs:
                                    file_path = available_files[display_name]

                                    # Detectar tipo de archivo
                                    if file_path.suffix.lower() == '.pdf':
                                        # Extraer texto de PDF
                                        import pdfplumber
                                        import io

                                        with open(file_path, 'rb') as f:
                                            pdf_file = io.BytesIO(f.read())

                                        try:
                                            with pdfplumber.open(pdf_file) as pdf:
                                                text = ""
                                                for page_num, page in enumerate(pdf.pages, 1):
                                                    extracted = page.extract_text()
                                                    if extracted:
                                                        text += f"--- Página {page_num} ---\n{extracted}\n\n"
                                                docs_dict[display_name] = text if text else "[PDF sin texto extraíble]"
                                        except Exception as pdf_err:
                                            docs_dict[display_name] = f"[Error extrayendo PDF: {str(pdf_err)[:50]}]"
                                    else:
                                        # Leer como texto
                                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                            docs_dict[display_name] = f.read()

                                # Llamar a Claude
                                generator = st.session_state.generator
                                response = generator.chat_with_context(user_input, docs_dict)

                                st.markdown(response)
                                st.session_state.chat_history.append({"role": "assistant", "content": response})

                            except Exception as e:
                                error_msg = f"❌ Error: {str(e)[:100]}"
                                st.error(error_msg)
                                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            else:
                st.info("👆 Selecciona documentos y asegúrate de que la API key esté configurada")
        else:
            st.info("📭 No hay documentos redactados. Primero redacta archivos en la sección anterior.")

    with tab_generator:
        st.markdown("### 📋 Generador Automático de Documentos")

        # Seleccionar tipo de documento
        doc_type = st.selectbox(
            "Tipo de documento:",
            ["Carta de Apelación", "Checklist de Documentos", "Email de Seguimiento"]
        )

        # Seleccionar archivo
        if available_files and api_key:
            selected_file = st.selectbox(
                "Selecciona un archivo:",
                options=available_files.keys(),
                key="gen_file"
            )

            # Información adicional
            diagnosis = st.text_input("🏥 Diagnóstico:", placeholder="Ej: Diabetes tipo 2")
            condition = st.text_area("📝 Detalles:", placeholder="Por qué fue negada", height=80)

            if st.button("✨ Generar Documento", type="primary"):
                if not diagnosis or not condition:
                    st.warning("Completa todos los campos")
                else:
                    with st.spinner("Generando..."):
                        try:
                            file_path = available_files[selected_file]

                            # Detectar tipo de archivo
                            if file_path.suffix.lower() == '.pdf':
                                # Extraer texto de PDF
                                import pdfplumber
                                import io

                                with open(file_path, 'rb') as f:
                                    pdf_file = io.BytesIO(f.read())

                                content = ""
                                try:
                                    with pdfplumber.open(pdf_file) as pdf:
                                        for page_num, page in enumerate(pdf.pages, 1):
                                            extracted = page.extract_text()
                                            if extracted:
                                                content += f"--- Página {page_num} ---\n{extracted}\n\n"
                                except Exception as pdf_err:
                                    st.error(f"Error extrayendo PDF: {pdf_err}")
                                    content = "[Error en PDF]"
                            else:
                                # Leer como texto
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read()

                            generator = st.session_state.generator
                            prompt_content = f"{content}\n\nDiagnóstico: {diagnosis}\n\nDetalles: {condition}"

                            if doc_type == "Carta de Apelación":
                                result = generator.generate_appeal_letter(prompt_content)
                                filename = f"carta_apelacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                            elif doc_type == "Checklist de Documentos":
                                result = generator.generate_document_checklist(prompt_content)
                                filename = f"checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                            else:
                                result = generator.generate_follow_up_email(prompt_content)
                                filename = f"email_seguimiento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

                            if result:
                                st.success(f"✅ Documento generado")

                                # Guardar localmente
                                output_path = GENERATED_DIR / filename
                                with open(output_path, 'w', encoding='utf-8') as f:
                                    f.write(result)
                                st.success(f"✅ Guardado localmente: {filename}")

                                # Mostrar contenido
                                st.text_area("Contenido:", result, height=300, disabled=True)

                                # Descargar
                                st.download_button(
                                    label=f"📥 Descargar {doc_type}",
                                    data=result,
                                    file_name=filename,
                                    mime="text/plain",
                                    type="primary"
                                )
                            else:
                                st.error("❌ Error generando documento")

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)[:100]}")
        else:
            st.info("📭 No hay documentos disponibles o API key no configurada")

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
