# ⚡ Inicio Rápido (5 Minutos)

**Para colaboradores: Setup + primer test en 5 minutos**

## 1️⃣ Clonar y Setup (2 min)

```bash
# Clonar
git clone https://github.com/tu-org/medical_automation.git
cd medical_automation

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalar
pip install -r requirements.txt
```

## 2️⃣ Configurar API (1 min)

```bash
# Copiar template
cp .env.example .env

# Editar .env con tu API key
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## 3️⃣ Ejecutar Demo (2 min)

```bash
python3 scripts/run_all.py
```

Debería ver:
- ✅ Paso 1: Archivos organizados
- ✅ Paso 2: Datos redactados
- ✅ Paso 3: Documentos generados (si está API key)

## 4️⃣ Revisar Resultados

```bash
# Ver archivos organizados
ls organized_data/

# Ver datos redactados
cat for_claude/Expedientes/expediente_medico.txt

# Ver documentos generados
ls outputs/
```

## ✅ Listo!

Ya puedes:
- Contribuir cambios
- Crear tu rama: `git checkout -b feature/tu-cambio`
- Hacer un PR

## 📚 Siguiente Paso

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para workflow completo.

---

**¿Problemas?** Revisa [README.md](README.md) → Troubleshooting
