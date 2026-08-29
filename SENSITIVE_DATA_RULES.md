# Reglas de Detección de Datos Sensibles (PHI/PII)

Este documento describe las reglas de detección de **Información Personal Identificable (PHI/PII)** utilizado en el sistema.

Las reglas están basadas en el **HMRE Sovereign Engine** (Heurístico Lab) y son específicas para documentos médicos mexicanos.

---

## 📋 Datos Detectados

### 1. **CURP** (Clave Única de Registro de Población)
- **Formato**: 18 caracteres exactos
- **Patrón**: `ABCD891215HDFRNN01`
- **Ejemplo**: `GARM770102HDFRRN03`
- **Precisión**: Muy alta (formato muy específico)

### 2. **RFC** (Registro Federal de Contribuyentes)
- **Formato**: 11-13 caracteres
- **Patrón**: `AAA123456XYZ`
- **Ejemplo**: `GUAG6001255LA`
- **Precisión**: Alta (evita falsos positivos con CURP)

### 3. **NSS** (Número de Seguro Social - IMSS)
- **Formato**: 11 dígitos
- **Variaciones**: `NSS 12345678901`, `N.S.S. 12345678901`
- **Ejemplo**: `02123456789`
- **Precisión**: Alta

### 4. **POLIZA** (Número de Póliza de Seguros)
- **Formato**: Alfanumérico, 6-24 caracteres
- **Variaciones**: `Póliza XXX-123456`, `Policy #ABC123456`
- **Ejemplo**: `BCBS-789456`, `AET/2024-567890`
- **Precisión**: Media-Alta

### 5. **CLABE** (Cuenta Bancaria)
- **Formato**: Exactamente 18 dígitos
- **Patrón**: `002000000000000001`
- **Ejemplo**: `032180000118359719`
- **Precisión**: Muy alta

### 6. **PAN** (Número de Tarjeta de Crédito)
- **Formato**: 16 dígitos (4 grupos de 4)
- **Variaciones**: `1234-5678-9012-3456`, `1234 5678 9012 3456`
- **Ejemplo**: `4111-2222-3333-4444`
- **Precisión**: Alta

### 7. **EMAIL** (Correo Electrónico)
- **Formato**: `usuario@dominio.extension`
- **Ejemplo**: `paciente@gmail.com`
- **Precisión**: Alta

### 8. **PHONE** (Número Telefónico)
- **Formato**: Soporta formato mexicano
- **Variaciones**: `+52 55 1234 5678`, `(55) 1234-5678`
- **Ejemplo**: `+52 55 2234 5678`, `(33) 1234-5678`
- **Precisión**: Alta

### 9. **MEDICO** (Nombre de Médico/Profesional)
- **Triggers**: `Dr.`, `Dra.`, `Médico`, `Cirujano`
- **Formato**: Nombre + Apellido(s)
- **Ejemplo**: `Dr. Juan García López`
- **Precisión**: Alta (requiere prefijo)

### 10. **PACIENTE** (Nombre de Paciente/Asegurado)
- **Triggers**: `Paciente:`, `Asegurado:`, `Beneficiario:`
- **Formato**: Nombre + Apellido(s)
- **Ejemplo**: `Paciente: María García Rodríguez`
- **Precisión**: Alta (requiere contexto)

---

## 🎯 Tokenización

Cada dato sensible se reemplaza por un **token estable** en formato:

```
[[TIPO#NNNN]]
```

**Ejemplo:**
- Original: `Mi RFC es GUAG6001255LA`
- Tokenizado: `Mi RFC es [[RFC#0001]]`

**Características:**
- ✅ Tokens estables: Mismo valor → Mismo token
- ✅ Colapsing: Duplicados usan el mismo token
- ✅ Reversible: Puede rehidratarse localmente
- ✅ Rastreable: Inventario de tokens con valores originales

---

## 🔒 Seguridad

### Zero-Copy Guarantee
- Valores originales NUNCA se escriben a disco
- Solo en `bytearray` en RAM (puede ser limpiado con `memset`)
- Tokens son seguros para enviar a Claude

### Privacy Model
1. **Detecta**: Escanea documento por PHI/PII
2. **Tokeniza**: Reemplaza con `[[TIPO#NNNN]]`
3. **Almacena**: Valores en TokenVault (RAM-only)
4. **Envía**: Solo el texto tokenizado a Claude
5. **Preserva**: Valores no persisten en disk

---

## 📊 Matriz de Precisión

| Tipo | Precisión | Falsos Positivos | Falsos Negativos |
|------|-----------|-----------------|-----------------|
| CURP | ★★★★★ | Muy bajo | Muy bajo |
| RFC | ★★★★★ | Muy bajo | Muy bajo |
| NSS | ★★★★☆ | Bajo | Bajo |
| CLABE | ★★★★★ | Muy bajo | Muy bajo |
| PAN | ★★★★☆ | Medio | Bajo |
| POLIZA | ★★★★☆ | Medio | Bajo |
| EMAIL | ★★★★☆ | Bajo | Bajo |
| PHONE | ★★★★☆ | Medio | Bajo |
| MEDICO | ★★★★☆ | Bajo | Bajo |
| PACIENTE | ★★★★☆ | Bajo | Bajo |

---

## 🔧 Personalización

Para agregar nuevas reglas en `scripts/02_read_and_redact.py`:

```python
# En LocalDataProcessor.__init__()
self.rules.append(
    SanitizationRule(
        "LABEL",  # Tipo de dato
        r"PATTERN",  # Regex
        group=0,  # Grupo de captura (default: 0)
        flags=re.IGNORECASE  # Banderas (opcional)
    )
)
```

---

## 📚 Referencias

- **HMRE Sovereign Engine**: `/Users/arturomendoza/Downloads/arch-ord-2026-c6f33b/`
- **Archivo de Perimeter**: `app/api/perimeter.py`
- **CURP Specification**: https://www.gob.mx/curp/
- **RFC Specification**: https://www.sat.gob.mx/

---

## ✅ Última Actualización

- **Fecha**: 2026-08-29
- **Versión**: 2.0 (Con reglas HMRE)
- **Estado**: Producción
