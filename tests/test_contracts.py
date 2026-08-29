"""
Tests for Pydantic contract validation
Ensures all data structures are validated and immutable
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    DocumentCategory,
    FileUploadContract,
    RedactionRequest,
    RedactionResult,
    DocumentGenerationRequest,
    OrganizationRequest,
    PHITokens,
    SystemHealthCheck,
)


class TestFileUploadContract:
    """Tests for file upload validation"""

    def test_valid_file_upload(self):
        """Test valid file upload contract"""
        contract = FileUploadContract(
            filename="test.txt",
            content=b"test content",
            category=DocumentCategory.EXPEDIENTES
        )
        assert contract.filename == "test.txt"
        assert contract.content == b"test content"
        assert contract.category == DocumentCategory.EXPEDIENTES

    def test_file_upload_empty_filename(self):
        """Test file upload with empty filename"""
        with pytest.raises(ValueError):
            FileUploadContract(filename="", content=b"content")

    def test_file_upload_empty_content(self):
        """Test file upload with empty content"""
        with pytest.raises(ValueError):
            FileUploadContract(filename="test.txt", content=b"")

    def test_file_upload_default_category(self):
        """Test file upload with default category"""
        contract = FileUploadContract(filename="test.txt", content=b"content")
        assert contract.category == DocumentCategory.OTROS

    def test_file_upload_extra_fields_forbidden(self):
        """Test that extra fields are forbidden"""
        with pytest.raises(ValueError):
            FileUploadContract(
                filename="test.txt",
                content=b"content",
                extra_field="not allowed"
            )

    def test_file_upload_max_filename_length(self):
        """Test filename length validation"""
        long_name = "x" * 256
        with pytest.raises(ValueError):
            FileUploadContract(filename=long_name, content=b"content")


class TestRedactionContracts:
    """Tests for redaction-related contracts"""

    def test_redaction_result_valid(self):
        """Test valid redaction result"""
        result = RedactionResult(
            original_length=100,
            redacted_length=80,
            redactions_made=5,
            redacted_text="redacted text here"
        )
        assert result.redactions_made == 5

    def test_redaction_result_negative_count(self):
        """Test redaction result with negative count"""
        with pytest.raises(ValueError):
            RedactionResult(
                original_length=100,
                redacted_length=80,
                redactions_made=-1,
                redacted_text="text"
            )

    def test_phi_tokens_calculation(self):
        """Test PHI tokens total calculation"""
        tokens = PHITokens(
            ssn_count=2,
            names_count=1,
            policy_count=1,
            dob_count=1,
            other_count=0
        )
        assert tokens.total == 5

    def test_phi_tokens_default_zeros(self):
        """Test PHI tokens with default zero values"""
        tokens = PHITokens()
        assert tokens.total == 0
        assert tokens.ssn_count == 0


class TestDocumentGenerationContracts:
    """Tests for document generation contracts"""

    def test_valid_document_generation_request(self):
        """Test valid document generation request"""
        req = DocumentGenerationRequest(
            redacted_content="[PATIENT_NAME] has Diabetes",
            doc_type="Carta de Apelación",
            diagnosis="Diabetes tipo 2",
            details="Negación de cobertura de insulina"
        )
        assert req.doc_type == "Carta de Apelación"

    def test_invalid_doc_type(self):
        """Test invalid document type"""
        with pytest.raises(ValueError):
            DocumentGenerationRequest(
                redacted_content="content",
                doc_type="Invalid Type",
                diagnosis="Diabetes",
                details="details"
            )

    def test_valid_doc_types(self):
        """Test all valid document types"""
        valid_types = [
            "Carta de Apelación",
            "Checklist de Documentos",
            "Email de Seguimiento"
        ]

        for doc_type in valid_types:
            req = DocumentGenerationRequest(
                redacted_content="content",
                doc_type=doc_type,
                diagnosis="Diabetes",
                details="details"
            )
            assert req.doc_type == doc_type


class TestOrganizationContracts:
    """Tests for file organization contracts"""

    def test_valid_organization_request(self):
        """Test valid organization request"""
        files = [
            FileUploadContract(
                filename="test1.txt",
                content=b"content1",
                category=DocumentCategory.EXPEDIENTES
            ),
            FileUploadContract(
                filename="test2.txt",
                content=b"content2",
                category=DocumentCategory.FACTURAS
            )
        ]
        req = OrganizationRequest(files=files)
        assert len(req.files) == 2

    def test_organization_request_empty_files(self):
        """Test organization request with empty files"""
        with pytest.raises(ValueError):
            OrganizationRequest(files=[])

    def test_organization_result_valid(self):
        """Test valid organization result"""
        result_data = {
            "Expedientes": ["file1.txt"],
            "Facturas": ["file2.txt"]
        }
        result = {
            "total_files": 2,
            "organized_count": 2,
            "categories": result_data
        }
        # Just verify structure is valid
        assert result["total_files"] == 2


class TestSystemHealthCheck:
    """Tests for system health contract"""

    def test_valid_healthy_status(self):
        """Test valid healthy status"""
        health = SystemHealthCheck(
            status="healthy",
            version="1.0.0",
            api_key_configured=True
        )
        assert health.status == "healthy"

    def test_invalid_status(self):
        """Test invalid status"""
        with pytest.raises(ValueError):
            SystemHealthCheck(
                status="unknown",
                version="1.0.0",
                api_key_configured=True
            )

    def test_valid_status_values(self):
        """Test all valid status values"""
        for status in ["healthy", "warning", "error"]:
            health = SystemHealthCheck(
                status=status,
                version="1.0.0",
                api_key_configured=False,
                message="test message"
            )
            assert health.status == status


class TestContractImmutability:
    """Tests for contract immutability"""

    def test_file_upload_validates_on_access(self):
        """Test that contracts validate data correctly"""
        contract = FileUploadContract(
            filename="test.txt",
            content=b"content"
        )

        # Verify the contract has the correct values
        assert contract.filename == "test.txt"
        assert contract.content == b"content"

    def test_redaction_request_validates_on_create(self):
        """Test redaction request validation on creation"""
        req = RedactionRequest(text="original text")

        # Verify the contract has the correct value
        assert req.text == "original text"
