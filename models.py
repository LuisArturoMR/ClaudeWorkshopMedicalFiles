"""
Pydantic v2 Models and Contracts for Medical Automation System
Ensures type safety and validation for all inputs/outputs
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from enum import Enum


class DocumentCategory(str, Enum):
    """Valid document categories"""
    POLIZAS = "Pólizas"
    EXPEDIENTES = "Expedientes"
    FACTURAS = "Facturas"
    APELACIONES = "Apelaciones"
    MEDICAMENTOS = "Medicamentos"
    OTROS = "Otros"


class FileUploadContract(BaseModel):
    """Validates file uploads"""
    model_config = ConfigDict(extra='forbid')

    filename: str = Field(..., min_length=1, max_length=255, description="Nombre del archivo")
    content: bytes = Field(..., min_length=1, description="Contenido del archivo")
    category: Optional[DocumentCategory] = Field(default=DocumentCategory.OTROS)


class RedactionRequest(BaseModel):
    """Validates redaction requests"""
    model_config = ConfigDict(extra='forbid')

    text: str = Field(..., min_length=1, description="Texto a redactar")
    language: Optional[str] = Field(default="es", description="Idioma")

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        """Validate text content"""
        if not v or not v.strip():
            raise ValueError("El texto no puede estar vacío")
        return v


class RedactionResult(BaseModel):
    """Result of redaction operation"""
    model_config = ConfigDict(extra='forbid')

    original_length: int = Field(..., description="Longitud original")
    redacted_length: int = Field(..., description="Longitud redactada")
    redactions_made: int = Field(..., ge=0, description="Número de redacciones")
    redacted_text: str = Field(..., description="Texto redactado")


class DocumentGenerationRequest(BaseModel):
    """Validates document generation requests"""
    model_config = ConfigDict(extra='forbid')

    redacted_content: str = Field(..., min_length=1, description="Contenido redactado")
    doc_type: str = Field(
        ...,
        description="Tipo de documento",
        pattern="^(Carta de Apelación|Checklist de Documentos|Email de Seguimiento)$"
    )
    diagnosis: str = Field(..., min_length=1, max_length=255, description="Diagnóstico")
    details: str = Field(..., min_length=1, description="Detalles adicionales")


class DocumentGenerationResult(BaseModel):
    """Result of document generation"""
    model_config = ConfigDict(extra='forbid')

    doc_type: str = Field(..., description="Tipo de documento")
    content: str = Field(..., description="Contenido generado")
    length: int = Field(..., ge=0, description="Longitud del documento")


class OrganizationRequest(BaseModel):
    """Validates file organization requests"""
    model_config = ConfigDict(extra='forbid')

    files: List[FileUploadContract] = Field(..., min_items=1, description="Archivos a organizar")


class OrganizationResult(BaseModel):
    """Result of file organization"""
    model_config = ConfigDict(extra='forbid')

    total_files: int = Field(..., ge=0, description="Total de archivos")
    organized_count: int = Field(..., ge=0, description="Archivos organizados")
    categories: dict = Field(..., description="Archivos por categoría")


class PHITokens(BaseModel):
    """Sensitive data tokens found and redacted"""
    model_config = ConfigDict(extra='forbid')

    ssn_count: int = Field(default=0, ge=0, description="SSN redactados")
    names_count: int = Field(default=0, ge=0, description="Nombres redactados")
    policy_count: int = Field(default=0, ge=0, description="Pólizas redactadas")
    dob_count: int = Field(default=0, ge=0, description="Fechas de nacimiento redactadas")
    other_count: int = Field(default=0, ge=0, description="Otros datos redactados")

    @property
    def total(self) -> int:
        """Total tokens redacted"""
        return (
            self.ssn_count
            + self.names_count
            + self.policy_count
            + self.dob_count
            + self.other_count
        )


class SystemHealthCheck(BaseModel):
    """System health status"""
    model_config = ConfigDict(extra='forbid')

    status: str = Field(..., pattern="^(healthy|warning|error)$")
    version: str = Field(..., description="System version")
    api_key_configured: bool = Field(..., description="API key configurada")
    message: Optional[str] = Field(default=None)
