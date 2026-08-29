#!/usr/bin/env python3
"""
Lee archivos sensibles LOCALMENTE y genera versión redactada para Claude
Los datos originales NUNCA salen de tu máquina
Tokenización inspirada en HMRE Sovereign Engine: tokens [[LABEL#NNNN]]
"""

import re
import hashlib
import secrets
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Tuple
from uuid import uuid4


class TokenVault:
    """Almacén de tokens PHI/PII en RAM (similar a HMRE)"""

    def __init__(self):
        self._key = secrets.token_bytes(32)
        self._forward: Dict[bytes, str] = {}  # hash -> token
        self._reverse: Dict[str, str] = {}     # token -> plaintext
        self._counters: Dict[str, int] = {}

    def _digest(self, label: str, value: str) -> bytes:
        """Hash estable para colapsing duplicados"""
        return hashlib.blake2b(
            value.encode("utf-8"), key=self._key, digest_size=16, person=b"medic-vault"
        ).digest() + label.encode("ascii")

    def tokenize(self, label: str, value: str) -> str:
        """Genera o retorna token estable: [[LABEL#NNNN]]"""
        digest = self._digest(label, value)
        token = self._forward.get(digest)
        if token is not None:
            return token
        index = self._counters.get(label, 0) + 1
        self._counters[label] = index
        token = f"[[{label}#{index:04d}]]"
        self._forward[digest] = token
        self._reverse[token] = value
        return token

    def detokenize(self, token: str) -> Optional[str]:
        """Restaura el valor original"""
        return self._reverse.get(token)

    def get_all_tokens(self) -> List[Dict[str, str]]:
        """Retorna lista de todos los tokens encontrados"""
        return [
            {
                "token": token,
                "tipo": token.split("#")[0].lstrip("["),
                "valor_original": value,
            }
            for token, value in self._reverse.items()
        ]

    def rehydrate(self, text: str) -> str:
        """Restaura todos los valores originales en un texto"""
        result = text
        TOKEN_RE = re.compile(r"\[\[[A-Z_]+#\d{4,}\]\]")

        def replace(match):
            return self.detokenize(match.group(0)) or match.group(0)

        return TOKEN_RE.sub(replace, result)


class LocalDataProcessor:
    """Procesa datos médicos localmente con tokenización"""

    def __init__(self):
        self.vault = TokenVault()

        # Reglas de detección: (label, pattern, flags)
        self.rules = [
            # Números de seguridad social
            ("SSN", r"\b\d{3}-\d{2}-\d{4}\b", re.IGNORECASE),

            # Fechas de nacimiento
            ("DOB", r"\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d{2}\b", re.IGNORECASE),
            ("DOB", r"\b(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\b", re.IGNORECASE),

            # Números de póliza
            ("POLIZA", r"\b(?:póliza|policy|certificado)\s*(?:nú?m|no|#)?\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-/]{5,23})\b", re.IGNORECASE),
            ("POLIZA", r"\b[A-Z]{2,4}-\d{6,8}\b", re.IGNORECASE),

            # Nombres (patrones: Nombre Apellido - capitalizado)
            ("PACIENTE", r"\b[A-Z][a-záéíóú]+(?:\s+[A-Z][a-záéíóú]+)+\b", re.IGNORECASE),
        ]

    def detect_sensitive_data(self, text: str) -> List[Dict[str, str]]:
        """Detecta datos sensibles sin modificar - retorna para tabla"""
        findings = []
        seen = set()

        for label, pattern, flags in self.rules:
            for match in re.finditer(pattern, text, flags):
                # Usar el grupo 1 si existe (captura), sino el match completo
                value = match.group(1) if match.groups() else match.group(0)
                key = (label, value)

                if key not in seen:
                    findings.append({
                        "tipo": label,
                        "valor_original": value,
                        "posicion": f"Car. {match.start()}-{match.end()}"
                    })
                    seen.add(key)

        return findings

    def tokenize_text(self, text: str) -> str:
        """Reemplaza datos sensibles con tokens [[LABEL#NNNN]]"""
        result = text

        for label, pattern, flags in self.rules:
            def replace_with_token(match):
                value = match.group(1) if match.groups() else match.group(0)
                return self.vault.tokenize(label, value)

            result = re.sub(pattern, replace_with_token, result, flags=flags)

        return result

    def redact_text(self, text: str) -> str:
        """Alias para tokenize_text para compatibilidad"""
        return self.tokenize_text(text)

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
            "redactions_made": len(re.findall(r'\[\[[A-Z_]+#\d{4,}\]\]', redacted_content))
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
