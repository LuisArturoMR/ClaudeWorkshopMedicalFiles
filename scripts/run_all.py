#!/usr/bin/env python3
"""
Script maestro - Ejecuta todo el proceso automáticamente
1. Organiza archivos
2. Lee archivos localmente
3. Redacta datos sensibles
4. Genera documentos con Claude
"""

import sys
import os
from pathlib import Path

# Agregar scripts al path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from organize_files import organize_files
from read_and_redact import LocalDataProcessor
from generate_with_claude import ClaudeDocumentGenerator

def main():
    print("\n" + "="*70)
    print(" SISTEMA DE AUTOMATIZACIÓN MÉDICA - PRIVACIDAD LOCAL")
    print("="*70)
    print(" Todo sucede en tu máquina. Datos sensibles NUNCA salen.")
    print("="*70 + "\n")

    # PASO 1: Organizar
    print("\n[PASO 1/4] Organizando archivos médicos...")
    print("-" * 70)
    try:
        organize_files(source_dir="raw_data", dest_dir="organized_data")
    except Exception as e:
        print(f"❌ Error en organización: {e}")
        return

    # PASO 2: Leer y Redactar
    print("\n[PASO 2/4] Leyendo archivos LOCALMENTE y redactando...")
    print("-" * 70)
    try:
        processor = LocalDataProcessor()
        processor.process_directory(
            source_dir="organized_data",
            dest_dir="for_claude"
        )
    except Exception as e:
        print(f"❌ Error en redacción: {e}")
        return

    # PASO 3: Generar con Claude
    print("\n[PASO 3/4] Generando documentos con Claude...")
    print("-" * 70)
    try:
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("\n⚠️  ATENCIÓN: ANTHROPIC_API_KEY no configurada")
            print("   Opción 1: Saltamos Claude por ahora")
            print("   Opción 2: Configura primero y ejecuta step 3")
            response = input("\n¿Saltar Claude? (S/N): ").strip().lower()
            if response != 'n':
                print("   (Saltando generación con Claude)")
            else:
                generator = ClaudeDocumentGenerator()
                generator.process_and_generate(
                    source_dir="for_claude",
                    output_dir="outputs"
                )
        else:
            generator = ClaudeDocumentGenerator()
            generator.process_and_generate(
                source_dir="for_claude",
                output_dir="outputs"
            )
    except Exception as e:
        print(f"❌ Error en Claude: {e}")

    # RESUMEN FINAL
    print("\n" + "="*70)
    print(" ✅ PROCESO COMPLETADO")
    print("="*70)
    print("\n📁 ESTRUCTURA GENERADA:")
    print("   raw_data/           → Archivos originales (PRIVADOS)")
    print("   organized_data/     → Archivos organizados por categoría")
    print("   for_claude/         → Archivos redactados (LISTOS PARA CLAUDE)")
    print("   outputs/            → Documentos generados")
    print("\n🔒 SEGURIDAD:")
    print("   • Datos sensibles se quedan en tu máquina")
    print("   • Solo versiones redactadas van a Claude")
    print("   • Nada se sube a internet sin tu control")
    print("\n📝 PRÓXIMOS PASOS:")
    print("   1. Coloca tus archivos en 'raw_data/'")
    print("   2. Ejecuta nuevamente este script")
    print("   3. Revisa 'outputs/' para ver documentos generados")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
