"""
Pytest configuration and fixtures for Medical Automation System
"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture(scope="session")
def temp_workspace():
    """Create temporary workspace for tests"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_text_file(temp_workspace):
    """Create a sample text file with medical data"""
    content = """EXPEDIENTE MÉDICO - CONFIDENCIAL

Paciente: Juan García
Edad: 75 años
SSN: 123-45-6789
Fecha de Nacimiento: 03/15/1948
Número de Póliza: BCBS-789456

DIAGNÓSTICO PRINCIPAL:
- Diabetes tipo 2
- Hipertensión arterial

MEDICAMENTOS:
1. Metformina 1000mg
2. Lisinopril 10mg
3. Atorvastatina 20mg
"""
    file_path = Path(temp_workspace) / "sample_medical.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def sample_redacted_content():
    """Sample of what redacted content should look like"""
    return """EXPEDIENTE MÉDICO - CONFIDENCIAL

Paciente: [PATIENT_NAME]
Edad: 75 años
SSN: [SSN_REDACTED]
Fecha de Nacimiento: [DOB]
Número de Póliza: [POLICY_ID]

DIAGNÓSTICO PRINCIPAL:
- Diabetes tipo 2
- Hipertensión arterial

MEDICAMENTOS:
1. Metformina 1000mg
2. Lisinopril 10mg
3. Atorvastatina 20mg
"""


@pytest.fixture
def file_samples(temp_workspace):
    """Create multiple sample files for organization tests"""
    samples = {
        "expediente.txt": "Diagnóstico: Diabetes tipo 2\nPaciente: Juan",
        "factura.txt": "Factura Médica\nCobro: $500",
        "póliza.txt": "Póliza de Cobertura\nBCSS-789456",
    }

    files = {}
    for name, content in samples.items():
        file_path = Path(temp_workspace) / name
        file_path.write_text(content)
        files[name] = file_path

    return files
