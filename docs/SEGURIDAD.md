# 🔒 Política de Seguridad y Privacidad

## Garantías de Privacidad

Este proyecto está diseñado específicamente para **proteger datos médicos sensibles**:

### ✅ Lo Que Hacemos

1. **Datos locales primero**
   - Todos los archivos originales se quedan en tu máquina
   - Nada se sube a internet sin tu consentimiento explícito

2. **Redacción automática**
   - PII (Personally Identifiable Information) se redacta antes de cualquier procesamiento
   - SSN, fechas de nacimiento, nombres, números de póliza se reemplazan con placeholders

3. **Separación de datos**
   - Datos originales: `raw_data/` (nunca se toca)
   - Datos redactados: `for_claude/` (solo esto va a Claude)
   - Outputs: `outputs/` (documentos generados)

### ❌ Lo Que NO Hacemos

1. **NO grabamos datos**
   - Los datos originales no se envían a servidores externos
   - No hay logs con información sensible

2. **NO entrenamos con tus datos**
   - Cuando usas Claude API, Anthropic no retiene tus datos por defecto (30 días retención estándar)
   - Con Enterprise + Zero Retention, se borran inmediatamente

3. **NO compartimos información**
   - El proyecto es open-source pero tus datos son solo tuyos
   - No hay telemetría o tracking

## Cumplimiento Legal

### HIPAA (Health Insurance Portability and Accountability Act)

Si manejas datos de salud en EE.UU.:

- ✅ **Permitido**: Usar este sistema con datos de-identificados (redactados)
- ❌ **Prohibido**: Enviar PHI (Protected Health Information) sin Business Associate Agreement
- ✅ **Recomendado**: Usar con Anthropic Enterprise para máxima protección

**Configuración HIPAA-Compliant:**
```python
# 1. Redacta completamente
process_file("raw_data/patient.txt", "for_claude/patient_clean.txt")

# 2. Usa Anthropic Enterprise con Zero Retention
export ANTHROPIC_API_KEY="enterprise-key"

# 3. El output también es de-identificado
# → Documentos generados no contienen PII
```

### GDPR (General Data Protection Regulation)

Si tus usuarios son de EU:

- ✅ Datos están locales (User Control)
- ✅ Redacción automática (Data Minimization)
- ✅ Transparencia sobre cómo se usan

## Checklist de Seguridad

Antes de usar en producción:

### Para Desarrolladores

- [ ] `.env` no está comiteado
- [ ] `.gitignore` excluye `raw_data/`, `organized_data/`, `for_claude/`, `outputs/`
- [ ] No hay hardcoding de API keys
- [ ] Logs no contienen datos sensibles
- [ ] Tests verifican redacción correcta

### Para Usuarios Finales

- [ ] Datos originales están encriptados localmente (opcional)
- [ ] Solo datos redactados se envían a Claude
- [ ] Revisar outputs antes de usar
- [ ] Borrar archivos temporales después de usar
- [ ] Usar en máquina personal, no en servidor compartido

## Patrones de Redacción

Los siguientes patrones se redactan automáticamente:

```python
# Identificadores
SSN: 123-45-6789 → [SSN_REDACTED]
DNI: 12.345.678-9 → [DNI_REDACTED]

# Nombres
Juan García → [PATIENT_NAME]
Dr. Smith → [DOCTOR_NAME]

# Números de póliza
BCBS-789456 → [POLICY_ID]
AETNA-12345 → [POLICY_ID]

# Fechas de nacimiento
03/15/1948 → [DOB]
1948-03-15 → [DOB]

# Extensible en scripts/02_read_and_redact.py
```

## Incidentes de Seguridad

Si encuentras un vulnerability:

1. **NO lo publiques en Issues públicos**
2. Envía email a: security@tuorg.com (reemplazar)
3. Incluye: descripción, pasos para reproducir, impacto
4. Espera respuesta en 48 horas

```
Subject: [SECURITY] Descripción del problema

Descripción:
...

Pasos para reproducir:
...

Impacto:
...

Sugerencia de fix:
...
```

## Mejores Prácticas

### Almacenamiento Local

```bash
# ✅ BUENO - Encriptar datos locales
gpg --symmetric raw_data/expediente.txt
# Pide contraseña cada vez que se abre

# ❌ MALO - Dejar datos sensibles sin protección
# raw_data/ disponible para cualquiera en la máquina
```

### Credenciales

```bash
# ✅ BUENO - Variable de entorno
export ANTHROPIC_API_KEY="sk-ant-..."

# ✅ BUENO - .env local (no comiteado)
echo "ANTHROPIC_API_KEY=..." >> .env

# ❌ MALO - Hardcodear en código
API_KEY = "sk-ant-..." # En scripts/
```

### Outputs

```bash
# ✅ BUENO - Revisar antes de usar
cat outputs/carta_apelacion.txt
# (Verificar que no tiene datos reales)

# ✅ BUENO - Borrar outputs después
rm -rf outputs/*

# ❌ MALO - Asumir que están redactados
# (Siempre verificar manualmente)
```

## Auditoría

Cómo verificar que todo está seguro:

```bash
# 1. Ver qué se redactó
diff organized_data/Expedientes/paciente.txt \
     for_claude/Expedientes/paciente.txt

# 2. Verificar no hay PII en outputs
grep -r "[0-9]\{3\}-[0-9]\{2\}-[0-9]\{4\}" outputs/

# 3. Revisar logs
tail -f medical_automation.log
```

## FAQ de Seguridad

**P: ¿Puedo confiar en este software?**
A: Es open-source, puedes revisar todo el código. Pero úsalo bajo tu responsabilidad.

**P: ¿Qué pasa si alguien roba mi máquina?**
A: Si tiene acceso físico, puede acceder a raw_data/. Encripta tu disco.

**P: ¿Anthropic ve mis datos?**
A: Con Zero Retention (Enterprise), no. Con plan estándar, retienen 30 días.

**P: ¿Puedo usar esto con datos de pacientes reales?**
A: Solo si redactas completamente primero. Mejor: habla con tu legal team.

**P: ¿Es HIPAA-compliant?**
A: Potencialmente sí, si usas: Enterprise, Zero Retention, y redacción correcta.

---

**Última revisión**: 2024-08-29  
**Responsable**: Security Team
