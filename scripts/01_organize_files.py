#!/usr/bin/env python3
"""
Organiza archivos médicos en categorías automáticamente
Lee archivos localmente, NO los envía a Claude
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Definir categorías y palabras clave
CATEGORIES = {
    "Polizas": ["póliza", "policy", "cobertura", "plan", "beneficio"],
    "Expedientes": ["diagnóstico", "receta", "nota médica", "prueba", "resultado"],
    "Facturas": ["factura", "invoice", "cobro", "pago", "cuenta"],
    "Apelaciones": ["apelación", "appeal", "negación", "denegación", "recurso"],
    "Medicamentos": ["medicamento", "medicina", "prescripción", "droga"],
    "Otros": []
}

def organize_files(source_dir="raw_data", dest_dir="organized_data"):
    """Organiza archivos en carpetas por categoría"""

    source = Path(source_dir)
    dest = Path(dest_dir)

    # Crear carpetas de destino
    for category in CATEGORIES:
        (dest / category).mkdir(parents=True, exist_ok=True)

    if not source.exists():
        print(f"⚠️  Carpeta {source_dir} no existe")
        return

    files_moved = 0
    print(f"\n📁 Organizando archivos desde: {source_dir}")
    print("-" * 50)

    # Recorrer y copiar archivos
    for file in sorted(source.glob("*")):
        if file.is_file() and not file.name.startswith("."):
            category = "Otros"

            # Detectar categoría por nombre
            filename_lower = file.name.lower()
            for cat, keywords in CATEGORIES.items():
                if any(keyword in filename_lower for keyword in keywords):
                    category = cat
                    break

            # Copiar archivo a carpeta de destino
            dest_category = dest / category
            dest_category.mkdir(parents=True, exist_ok=True)  # Asegurar que existe
            dest_path = dest_category / file.name

            try:
                # Copiar archivo (no copia simbólica para evitar problemas de permisos)
                if not dest_path.exists():
                    shutil.copy2(file, dest_path)
                    print(f"  ✅ {file.name:40} → {category}/")
                    files_moved += 1
                else:
                    print(f"  ⚠️  {file.name:40} → {category}/ (ya existe)")
            except Exception as e:
                print(f"  ❌ Error con {file.name}: {e}")

    print("-" * 50)
    print(f"✅ {files_moved} archivos organizados")
    print(f"📂 Revisa carpeta '{dest_dir}' para ver resultados\n")

if __name__ == "__main__":
    organize_files()
