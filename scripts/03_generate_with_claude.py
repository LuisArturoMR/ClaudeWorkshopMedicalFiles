#!/usr/bin/env python3
"""
Lee archivos redactados LOCALMENTE y genera documentos con Claude API
"""

from pathlib import Path
import os
from anthropic import Anthropic

class ClaudeDocumentGenerator:
    """Genera documentos usando Claude con datos redactados"""

    def __init__(self):
        self.client = Anthropic()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            print("⚠️  ADVERTENCIA: ANTHROPIC_API_KEY no está configurada")
            print("   Necesitas: export ANTHROPIC_API_KEY='sk-...'")

    def read_redacted_file(self, filepath):
        """Lee archivo redactado (que ya está limpio)"""
        filepath = Path(filepath)

        if not filepath.exists():
            print(f"❌ Archivo no encontrado: {filepath}")
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def generate_appeal_letter(self, case_data):
        """Genera carta de apelación profesional"""

        prompt = f"""
Basándote en la siguiente información médica REDACTADA, genera una carta de apelación
profesional a una aseguradora. La carta debe ser formal, empática y bien estructurada.

INFORMACIÓN REDACTADA (sin datos personales sensibles):
{case_data}

La carta debe incluir:
1. Encabezado formal
2. Referencia a póliza (redactada)
3. Descripción clara de la condición
4. Argumentos médicos por qué debe cubrirse
5. Llamado a la acción
6. Firma (genérica)

IMPORTANTE: Mantén TODA la redacción - NO uses datos reales si los ves.
Genera como si fueran ejemplos ficticios.
"""

        print("\n🤖 Enviando a Claude para generar carta de apelación...")
        print("   ✅ Datos redactados (solo placeholders enviados)")

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def generate_document_checklist(self, case_data):
        """Genera checklist de documentos necesarios"""

        prompt = f"""
Basándote en la siguiente información médica REDACTADA, crea un checklist de
documentos típicamente necesarios para apelar esta negación.

INFORMACIÓN REDACTADA:
{case_data}

Crea un checklist profesional que incluya:
- Documentos médicos necesarios
- Cartas de médicos
- Pruebas diagnósticas
- Registros de tratamiento
- Documentación de costos

Formato:
☐ Documento 1 - Descripción
☐ Documento 2 - Descripción
etc.

Con breve nota sobre por qué cada uno es importante.
"""

        print("\n🤖 Generando checklist de documentos...")
        print("   ✅ Datos redactados (solo placeholders enviados)")

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def generate_follow_up_email(self, case_data):
        """Genera email de seguimiento"""

        prompt = f"""
Genera un email profesional de seguimiento para la aseguradora sobre esta apelación.
Datos REDACTADOS:

{case_data}

El email debe:
1. Ser cortés pero firme
2. Referenciar la póliza
3. Preguntar por estado de apelación
4. Establecer deadline de respuesta
5. Ofrecer información adicional

Formato de email profesional.
"""

        print("\n🤖 Generando email de seguimiento...")
        print("   ✅ Datos redactados")

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def process_and_generate(self, source_dir="for_claude", output_dir="outputs"):
        """Procesa archivos redactados y genera documentos"""

        if not self.api_key:
            print("\n❌ No se puede continuar sin API key")
            print("   Configura: export ANTHROPIC_API_KEY='tu-clave'")
            return

        source = Path(source_dir)
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*70}")
        print(f"GENERADOR DE DOCUMENTOS CON CLAUDE")
        print(f"{'='*70}")
        print(f"Leyendo desde: {source_dir}/ (archivos redactados)")
        print(f"Guardando en: {output_dir}/ (nuevos documentos)")
        print(f"Seguridad: Solo datos redactados enviados a Claude")
        print(f"{'='*70}\n")

        documents_generated = 0

        # Procesar cada categoría
        for category_dir in sorted(source.iterdir()):
            if category_dir.is_dir():
                print(f"\n📂 Procesando categoría: {category_dir.name}")

                for file in sorted(category_dir.glob("*")):
                    if file.is_file() and not file.name.startswith("."):

                        print(f"\n   📄 Archivo: {file.name}")

                        # Leer archivo redactado
                        content = self.read_redacted_file(file)
                        if not content:
                            continue

                        # Generar documentos
                        case_name = file.stem

                        # 1. Carta de apelación
                        letter = self.generate_appeal_letter(content)
                        if letter:
                            output_file = output / f"{case_name}_CARTA_APELACION.txt"
                            with open(output_file, 'w', encoding='utf-8') as f:
                                f.write(letter)
                            print(f"      ✅ Carta generada: {output_file.name}")
                            documents_generated += 1

                        # 2. Checklist
                        checklist = self.generate_document_checklist(content)
                        if checklist:
                            output_file = output / f"{case_name}_CHECKLIST.txt"
                            with open(output_file, 'w', encoding='utf-8') as f:
                                f.write(checklist)
                            print(f"      ✅ Checklist generado: {output_file.name}")
                            documents_generated += 1

                        # 3. Email de seguimiento
                        email = self.generate_follow_up_email(content)
                        if email:
                            output_file = output / f"{case_name}_EMAIL_SEGUIMIENTO.txt"
                            with open(output_file, 'w', encoding='utf-8') as f:
                                f.write(email)
                            print(f"      ✅ Email generado: {output_file.name}")
                            documents_generated += 1

        print(f"\n{'='*70}")
        print(f"✅ COMPLETADO")
        print(f"   Documentos generados: {documents_generated}")
        print(f"   Ubicación: {output_dir}/")
        print(f"{'='*70}\n")


if __name__ == "__main__":
    generator = ClaudeDocumentGenerator()
    generator.process_and_generate(
        source_dir="for_claude",
        output_dir="outputs"
    )
