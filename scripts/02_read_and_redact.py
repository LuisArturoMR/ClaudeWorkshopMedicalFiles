#!/usr/bin/env python3
"""
Lee archivos sensibles LOCALMENTE y genera versión redactada para Claude
Los datos originales NUNCA salen de tu máquina
Tokenización + Reglas de detección PHI/PII del HMRE Sovereign Engine
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


class SanitizationRule:
    """Una regla de detección de PHI/PII"""

    def __init__(self, label: str, pattern: str, group: int = 0, flags: int = 0):
        self.label = label
        self.pattern = re.compile(pattern, flags)
        self.group = group

    def scan(self, text: str) -> List[Tuple[int, int, str]]:
        """Retorna lista de (start, end, value) para matches"""
        findings = []
        for match in self.pattern.finditer(text):
            start, end = match.span(self.group)
            if start >= 0 and end > start:
                findings.append((start, end, match.group(self.group)))
        return findings


class LocalDataProcessor:
    """Procesa datos médicos con reglas de detección HMRE"""

    def __init__(self):
        self.vault = TokenVault()

        # Patrones de texto para nombres (con acentos mexicanos)
        _WORD = r"[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ''.-]*"
        _CONNECTOR = r"(?:de|del|la|las|los|y)"
        _NAME = r"{w}(?:[ ]+(?:{c}[ ]+)?{w}){{0,4}}".format(w=_WORD, c=_CONNECTOR)

        # Estados mexicanos
        _MX_STATES = (
            "AS|BC|BS|CC|CH|CL|CM|CS|DF|DG|GR|GT|HG|JC|MC|MN|MS|"
            "NE|NL|OC|PL|QR|QT|SL|SP|SR|TC|TL|TS|VZ|YN|ZS"
        )

        # Reglas de detección (ordenadas por especificidad - CURP antes que RFC)
        self.rules = [
            # CURP: 18 caracteres exactos, formato mexicano
            SanitizationRule(
                "CURP",
                r"\b[A-Z][AEIOUX][A-Z]{2}\d{6}[HM](?:" + _MX_STATES + r")"
                r"[B-DF-HJ-NP-TV-Z]{3}[A-Z0-9]\d\b",
            ),

            # RFC: Tax ID mexicano (11-13 caracteres)
            SanitizationRule("RFC", r"\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b"),

            # NSS: Seguro Social Mexicano (11 dígitos)
            SanitizationRule(
                "NSS",
                r"(?:NSS|N\.?S\.?S\.?|Seguro\s+Social|IMSS)\s*[:#-]?\s*(\d{11})\b",
                group=1,
                flags=re.IGNORECASE,
            ),

            # POLIZA: Números de póliza (variaciones)
            SanitizationRule(
                "POLIZA",
                r"(?:p[oó]liza|policy|certificado)\s*(?:n[uú]m(?:ero)?\.?|no\.?|#|:)?\s*"
                r"([A-Z0-9][A-Z0-9\-/]{5,23})",
                group=1,
                flags=re.IGNORECASE,
            ),

            # CLABE: Cuenta bancaria mexicana (18 dígitos exactos)
            SanitizationRule("CLABE", r"\b\d{18}\b"),

            # PAN: Tarjeta de crédito
            SanitizationRule("PAN", r"\b(?:\d{4}[ -]){3}\d{4}\b"),

            # EMAIL: Correos electrónicos
            SanitizationRule("EMAIL", r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),

            # PHONE: Teléfono (incluyendo formato mexicano +52)
            SanitizationRule(
                "PHONE",
                r"(?:\+52[ -]?)?(?:\(\d{2,3}\)[ -]?|\b\d{2,3}[ -])\d{3,4}[ -]?\d{4}\b"
            ),

            # MEDICO: Nombres de médicos
            SanitizationRule(
                "MEDICO",
                r"(?:Dra?|Doctora?|M[ée]dic[oa](?:\s+tratante)?|Cirujan[oa])\.?\s*:?\s+(" + _NAME + r")",
                group=1,
            ),

            # PACIENTE: Nombres de pacientes/asegurados
            SanitizationRule(
                "PACIENTE",
                r"(?:Nombre\s+del\s+[Pp]aciente|[Pp]aciente|[Aa]segurad[oa]|[Tt]itular|"
                r"[Bb]eneficiari[oa]|Patient)\s*:?\s+(" + _NAME + r")",
                group=1,
            ),
        ]

    def detect_sensitive_data(self, text: str) -> List[Dict[str, str]]:
        """Detecta datos sensibles - retorna tabla"""
        findings = []
        seen = set()

        for rule in self.rules:
            for start, end, value in rule.scan(text):
                key = (rule.label, value)
                if key not in seen:
                    findings.append({
                        "tipo": rule.label,
                        "valor_original": value,
                        "posicion": f"Car. {start}-{end}"
                    })
                    seen.add(key)

        return findings

    def tokenize_text(self, text: str) -> str:
        """Reemplaza datos sensibles con tokens [[LABEL#NNNN]]"""
        result = text
        offsets = []

        # Escanear todas las reglas para encontrar conflictos
        for rule in self.rules:
            for start, end, value in rule.scan(text):
                offsets.append((start, end, rule.label, value))

        # Ordenar por posición (reverso para no desplazar índices)
        offsets.sort(key=lambda x: x[0], reverse=True)

        # Reemplazar de atrás hacia adelante
        for start, end, label, value in offsets:
            token = self.vault.tokenize(label, value)
            result = result[:start] + token + result[end:]

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
