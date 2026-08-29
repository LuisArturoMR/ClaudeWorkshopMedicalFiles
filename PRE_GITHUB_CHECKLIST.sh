#!/bin/bash
# 🔒 Pre-GitHub Security Checklist
# Ejecuta esto ANTES de subir a GitHub

echo "════════════════════════════════════════════════════════════════"
echo "  🔒 PRE-GITHUB SECURITY CHECKLIST"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

passed=0
failed=0

# Función para pasar test
pass() {
    echo -e "${GREEN}✅ PASS${NC} - $1"
    ((passed++))
}

# Función para fallar test
fail() {
    echo -e "${RED}❌ FAIL${NC} - $1"
    ((failed++))
}

# Función para warning
warn() {
    echo -e "${YELLOW}⚠️  WARN${NC} - $1"
}

echo "1️⃣  Verificando Git..."
echo "────────────────────────────────────────────────────────────────"

if [ -d ".git" ]; then
    pass "Git repository existe"
else
    warn "Git no inicializado - ejecuta: git init"
fi

echo ""
echo "2️⃣  Verificando .gitignore..."
echo "────────────────────────────────────────────────────────────────"

if grep -q "raw_data" .gitignore 2>/dev/null; then
    pass ".gitignore contiene: raw_data/"
else
    fail ".gitignore NO contiene: raw_data/"
fi

if grep -q "organized_data" .gitignore 2>/dev/null; then
    pass ".gitignore contiene: organized_data/"
else
    fail ".gitignore NO contiene: organized_data/"
fi

if grep -q "for_claude" .gitignore 2>/dev/null; then
    pass ".gitignore contiene: for_claude/"
else
    fail ".gitignore NO contiene: for_claude/"
fi

if grep -q "\.env" .gitignore 2>/dev/null && ! grep -q "\.env\.example" .gitignore 2>/dev/null; then
    pass ".gitignore contiene: .env (pero no .env.example)"
else
    fail ".gitignore NO contiene .env correctamente"
fi

echo ""
echo "3️⃣  Verificando que datos sensibles NO están comiteados..."
echo "────────────────────────────────────────────────────────────────"

# SSN pattern
if git ls-files 2>/dev/null | xargs grep -l '\b[0-9]\{3\}-[0-9]\{2\}-[0-9]\{4\}\b' 2>/dev/null ; then
    fail "ENCONTRADO: Patrón SSN (123-45-6789) en archivos comiteados"
else
    pass "No encontrado: Patrón SSN en archivos"
fi

# Nombres de ejemplo
if git ls-files 2>/dev/null | xargs grep -l "Juan García" 2>/dev/null ; then
    fail "ENCONTRADO: Nombre 'Juan García' en archivos comiteados"
else
    pass "No encontrado: Nombre 'Juan García' en archivos"
fi

# Números de póliza
if git ls-files 2>/dev/null | xargs grep -l "BCBS-[0-9]" 2>/dev/null ; then
    fail "ENCONTRADO: Patrón de póliza en archivos comiteados"
else
    pass "No encontrado: Patrón de póliza en archivos"
fi

# API Keys
if git ls-files 2>/dev/null | xargs grep -l "sk-ant-" 2>/dev/null ; then
    fail "ENCONTRADO: API Key en archivos comiteados"
else
    pass "No encontrado: API Key en archivos"
fi

echo ""
echo "4️⃣  Verificando archivos no están en staging..."
echo "────────────────────────────────────────────────────────────────"

if git status 2>/dev/null | grep -q "raw_data" ; then
    fail "ERROR: raw_data/ está siendo tracked"
else
    pass "raw_data/ no está siendo tracked"
fi

if git status 2>/dev/null | grep -q "\.env" ; then
    fail "ERROR: .env está siendo tracked"
else
    pass ".env no está siendo tracked"
fi

echo ""
echo "5️⃣  Verificando archivos necesarios existen..."
echo "────────────────────────────────────────────────────────────────"

files=("README.md" "CONTRIBUTING.md" "SETUP_GITHUB.md" "TODO.md" "requirements.txt" ".env.example" ".gitignore" "LICENSE")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        pass "Archivo existe: $file"
    else
        fail "Archivo FALTA: $file"
    fi
done

echo ""
echo "6️⃣  Verificando scripts..."
echo "────────────────────────────────────────────────────────────────"

scripts=("scripts/01_organize_files.py" "scripts/02_read_and_redact.py" "scripts/03_generate_with_claude.py" "scripts/run_all.py")

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        pass "Script existe: $script"
    else
        fail "Script FALTA: $script"
    fi
done

echo ""
echo "7️⃣  Verificando Python está disponible..."
echo "────────────────────────────────────────────────────────────────"

if command -v python3 &> /dev/null; then
    version=$(python3 --version)
    pass "Python disponible: $version"
else
    fail "Python3 NO está disponible"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  📊 RESULTADOS"
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ Pasados: $passed${NC}"
echo -e "${RED}❌ Fallidos: $failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡LISTO PARA GITHUB!${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. git init (si no lo hiciste)"
    echo "2. git add ."
    echo "3. git commit -m 'feat: Initial commit - Medical automation system'"
    echo "4. Crear repo en GitHub"
    echo "5. git remote add origin https://github.com/TU_USUARIO/medical-automation.git"
    echo "6. git push -u origin main"
    exit 0
else
    echo -e "${RED}⚠️  PROBLEMAS ENCONTRADOS${NC}"
    echo ""
    echo "Revisa los errores arriba y corrige antes de subir a GitHub"
    echo "Ver: SETUP_GITHUB.md para más ayuda"
    exit 1
fi
