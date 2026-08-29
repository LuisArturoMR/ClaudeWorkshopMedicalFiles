#!/usr/bin/env python3
"""
Lee archivos sensibles LOCALMENTE y genera versión redactada para Claude
Los datos originales NUNCA salen de tu máquina
"""

import re
from pathlib import Path
from datetime import datetime

class LocalDataProcessor:
    """Procesa datos médicos localmente con redacción automática"""

    def __init__(self):
        # Mapeo de redacción: datos reales → placeholders seguros
        self.redaction_map = {
            # Nombres (ejemplo - personalizar)
            r"Juan\s+García": "[PATIENT_NAME]",
            r"María\s+García": "[CAREGIVER_NAME]",

            # Números de seguridad social
            r"\d{3}-\d{2}-\d{4}": "[SSN_REDACTED]",

            # Números de póliza (ejemplo)
            r"BCBS-\d+": "[POLICY_ID]",
            r"AETNA-\d+": "[POLICY_ID]",
            r"UNI-\d+": "[POLICY_ID]",

            # Fechas de nacimiento
            r"(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d{2}": "[DOB]",
            r"(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])": "[DOB]",
        }

    def read_file_locally(self, filepath):
        """Lee archivo localmente (no sale de aquí)"""
        filepath = Path(filepath)

        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"❌ Error leyendo {filepath}: {e}")
            return None

    def redact_text(self, text):
        """Redacta datos sensibles automáticamente"""
        redacted = text

        for pattern, replacement in self.redaction_map.items():
            redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)

        return redacted

    def process_file(self, input_file, output_file):
        """Lee archivo → Redacta → Guarda versión limpia para Claude"""

        print(f"\n📖 Leyendo: {input_file}")

        # Leer localmente
        original_content = self.read_file_locally(input_file)
        if original_content is None:
            return None

        print(f"   ✅ Archivo leído (LOCAL - no enviado a internet)")

        # Redactar
        redacted_content = self.redact_text(original_content)

        # Guardar versión limpia
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(redacted_content)

        print(f"   ✅ Redactado automáticamente")
        print(f"   ✅ Guardado en: {output_file} (LISTO PARA CLAUDE)")

        return {
            "original_length": len(original_content),
            "redacted_length": len(redacted_content),
            "redactions_made": len(re.findall(r'\[.*?_REDACTED\]', redacted_content))
        }

    def process_directory(self, source_dir="organized_data", dest_dir="for_claude"):
        """Procesa TODOS los archivos de una carpeta"""

        source = Path(source_dir)
        if not source.exists():
            print(f"⚠️  Carpeta {source_dir} no existe")
            return

        print(f"\n{'='*60}")
        print(f"PROCESANDO ARCHIVOS LOCALMENTE")
        print(f"{'='*60}")
        print(f"Origen: {source_dir}")
        print(f"Destino (para Claude): {dest_dir}")
        print(f"Seguridad: DATOS NUNCA SALEN DE TU MÁQUINA")
        print(f"{'='*60}")

        total_redactions = 0
        files_processed = 0

        # Procesar cada categoría
        for category_dir in sorted(source.iterdir()):
            if category_dir.is_dir():
                print(f"\n📂 Categoría: {category_dir.name}")

                for file in sorted(category_dir.glob("*")):
                    if file.is_file() and not file.name.startswith("."):

                        # Crear estructura en destino
                        dest_category = Path(dest_dir) / category_dir.name
                        dest_file = dest_category / file.name

                        # Procesar
                        result = self.process_file(str(file), str(dest_file))

                        if result:
                            files_processed += 1
                            total_redactions += result["redactions_made"]

        print(f"\n{'='*60}")
        print(f"✅ RESUMEN:")
        print(f"   Archivos procesados: {files_processed}")
        print(f"   Datos redactados: {total_redactions}")
        print(f"   Ubicación destino: {dest_dir}/")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    processor = LocalDataProcessor()

    # Procesar todos los archivos
    processor.process_directory(
        source_dir="organized_data",
        dest_dir="for_claude"
    )
