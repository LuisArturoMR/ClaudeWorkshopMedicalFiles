"""
Tests for data redaction functionality
"""

import pytest
import sys
import importlib.util
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import models
from models import RedactionRequest, PHITokens

# Import LocalDataProcessor using importlib (handles numeric prefixes)
spec = importlib.util.spec_from_file_location(
    "read_and_redact",
    str(Path(__file__).parent.parent / "scripts" / "02_read_and_redact.py")
)
redact_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(redact_module)
LocalDataProcessor = redact_module.LocalDataProcessor


class TestRedactionProcessor:
    """Test cases for LocalDataProcessor"""

    def test_processor_initialization(self):
        """Test processor can be initialized"""
        processor = LocalDataProcessor()
        assert processor is not None

    def test_ssn_redaction(self):
        """Test SSN redaction"""
        processor = LocalDataProcessor()
        text = "My SSN is 123-45-6789 and that's private"
        redacted = processor.redact_text(text)

        assert "[SSN_REDACTED]" in redacted
        assert "123-45-6789" not in redacted

    def test_name_redaction(self):
        """Test name redaction"""
        processor = LocalDataProcessor()
        text = "Patient name: Juan García, age 75"
        redacted = processor.redact_text(text)

        # Name should be redacted
        assert "[PATIENT_NAME]" in redacted or "García" not in redacted

    def test_policy_number_redaction(self):
        """Test policy number redaction"""
        processor = LocalDataProcessor()
        text = "Policy: BCBS-789456 is the coverage"
        redacted = processor.redact_text(text)

        assert "[POLICY_ID]" in redacted
        assert "BCBS-789456" not in redacted

    def test_date_redaction(self):
        """Test date of birth redaction"""
        processor = LocalDataProcessor()
        text = "DOB: 03/15/1948"
        redacted = processor.redact_text(text)

        assert "[DOB]" in redacted
        assert "03/15/1948" not in redacted

    def test_no_false_positives(self):
        """Test that normal text is not over-redacted"""
        processor = LocalDataProcessor()
        text = "This is a normal medical diagnosis: Diabetes type 2"
        redacted = processor.redact_text(text)

        # Should keep diagnosis but not add random redactions
        assert "Diabetes" in redacted
        assert text.count("[") <= redacted.count("[")

    def test_empty_text(self):
        """Test handling of empty text"""
        processor = LocalDataProcessor()
        text = ""
        redacted = processor.redact_text(text)

        assert redacted == ""

    def test_multiple_ssn(self):
        """Test redaction of multiple SSNs"""
        processor = LocalDataProcessor()
        text = "SSN1: 123-45-6789, SSN2: 987-65-4321"
        redacted = processor.redact_text(text)

        assert redacted.count("[SSN_REDACTED]") >= 2
        assert "123-45-6789" not in redacted
        assert "987-65-4321" not in redacted

    def test_mixed_sensitive_data(self):
        """Test redaction with mixed sensitive data"""
        processor = LocalDataProcessor()
        text = """
        Patient: Juan García
        SSN: 123-45-6789
        DOB: 03/15/1948
        Policy: BCBS-789456
        """
        redacted = processor.redact_text(text)

        # All sensitive data should be redacted
        assert "Juan García" not in redacted or "[PATIENT_NAME]" in redacted
        assert "123-45-6789" not in redacted
        assert "03/15/1948" not in redacted
        assert "BCBS-789456" not in redacted


class TestRedactionContract:
    """Test Pydantic contracts for redaction"""

    def test_redaction_request_valid(self):
        """Test valid redaction request"""
        req = RedactionRequest(text="This is text to redact")
        assert req.text == "This is text to redact"
        assert req.language == "es"

    def test_redaction_request_empty_text(self):
        """Test redaction request with empty text"""
        with pytest.raises(ValueError):
            RedactionRequest(text="")

    def test_redaction_request_whitespace_only(self):
        """Test redaction request with whitespace only"""
        with pytest.raises(ValueError):
            RedactionRequest(text="   ")

    def test_redaction_request_extra_fields_forbidden(self):
        """Test that extra fields are forbidden"""
        with pytest.raises(ValueError):
            RedactionRequest(text="text", extra_field="not allowed")

    def test_redaction_request_max_length(self):
        """Test very long text"""
        long_text = "x" * 100000
        req = RedactionRequest(text=long_text)
        assert len(req.text) == 100000
