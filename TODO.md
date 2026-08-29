# 📝 Roadmap y Tasks Pendientes

## ✅ Completado (MVP)

- [x] Organización de archivos por categorías
- [x] Redacción automática de datos sensibles
- [x] Integración con Claude API
- [x] Generación de cartas de apelación
- [x] Generación de checklists
- [x] Documentación README
- [x] Setup para GitHub

## 🚀 Priority Alta (Próximas 2 Semanas)

- [ ] **Tests unitarios**
  - [ ] `test_organize.py` - Verificar categorización
  - [ ] `test_redact.py` - Verificar redacción correcta
  - [ ] `test_generate.py` - Verificar generación con Claude
  - [ ] Ejecutar: `pytest tests/`

- [ ] **Mejor manejo de errores**
  - [ ] Catch de excepciones específicas en scripts
  - [ ] Mensajes de error más descriptivos
  - [ ] Retry logic para Claude API

- [ ] **Validación de datos**
  - [ ] Verificar que archivos redactados no contienen PII
  - [ ] Warnings si encuentra patrones sospechosos
  - [ ] Report de datos encontrados vs redactados

## 🎯 Priority Media (Este Mes)

- [ ] **Extensión de categorías**
  - [ ] Agregar soporte para más tipos de documentos
  - [ ] Permitir categorías personalizadas en config

- [ ] **Más patrones de redacción**
  - [ ] Emails
  - [ ] Teléfonos
  - [ ] Direcciones
  - [ ] Números de cuenta bancaria

- [ ] **Exportación mejorada**
  - [ ] Generar PDFs con logos
  - [ ] Exportar a Word (.docx)
  - [ ] Crear zipfiles de resultados

- [ ] **Logging**
  - [ ] Archivo de log detallado
  - [ ] Nivel de verbosidad configurable
  - [ ] Auditoría de cambios

## 💡 Priority Baja (Futuro)

- [ ] **Interface Web**
  - [ ] Simple dashboard web
  - [ ] Drag & drop de archivos
  - [ ] Visualización de progreso en tiempo real

- [ ] **Integración con otros LLMs**
  - [ ] Gemini
  - [ ] GPT-4
  - [ ] Llama (local)

- [ ] **Automatización de aseguradoras**
  - [ ] API connector para aseguradoras comunes
  - [ ] Auto-submit de apelaciones
  - [ ] Tracking de status

- [ ] **Machine Learning**
  - [ ] Detectar automáticamente tipo de documento
  - [ ] Sugerir mejoras en redacción
  - [ ] Predicción de éxito de apelación

## 🐛 Bugs Conocidos

- [ ] Redacción puede no detectar variaciones de formato
- [ ] Algunos caracteres especiales pueden no redactarse
- [ ] Performance lenta con archivos >100MB

## 📊 Métricas

- Total issues: ~15
- Completados: ~8
- En progreso: 0
- Por hacer: ~7

## 🤝 Cómo Contribuir

Elige un task:
1. Abre un Issue con `[TASK]` en el título
2. Comenta: "Quiero trabajar en esto"
3. Se te asignará
4. Haz un PR cuando termines

Ejemplo:
```
[TASK] Crear test_organize.py

Quiero escribir tests unitarios para 01_organize_files.py
```

## 💬 Área de Discusión

- **Design**: Proponer nuevas features
- **Questions**: Preguntas sobre arquitectura
- **Ideas**: Sugerencias de mejora

---

**Última actualización**: 2024-08-29  
**Mantenedor principal**: @tu-usuario
