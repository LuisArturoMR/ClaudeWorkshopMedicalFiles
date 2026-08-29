# 🚀 Setup en GitHub

Pasos para subir el proyecto a GitHub para que tu equipo pueda continuar.

## 1️⃣ Crear Repositorio en GitHub

### Opción A: Desde GitHub Web

1. Ve a https://github.com/new
2. **Repository name**: `medical-automation` (o lo que prefieras)
3. **Description**: "Sistema de automatización médica con privacidad local"
4. **Visibility**: `Private` (para datos sensibles) o `Public` (si lo haces open-source)
5. **NO** inicialices con README (ya tienes uno)
6. Click "Create repository"

### Opción B: Desde CLI

```bash
# Requiere GitHub CLI: https://cli.github.com/
gh repo create medical-automation \
  --description "Sistema de automatización médica" \
  --private \
  --source=. \
  --remote=origin \
  --push
```

---

## 2️⃣ Inicializar Git Localmente

```bash
cd /Users/arturomendoza/Documents/ClaudeWorkshopProject/medical_automation

# Inicializar git
git init

# Configurar usuario (una sola vez)
git config user.email "tu@email.com"
git config user.name "Tu Nombre"

# Agregar todos los archivos (respeta .gitignore)
git add .

# Primer commit
git commit -m "feat: Initial commit - Medical automation system with local privacy

- File organization by category
- Automatic redaction of sensitive data
- Claude API integration for document generation
- Comprehensive security and privacy features"

# Verificar que se ignoren datos sensibles
git status  # No debe mostrar raw_data/, organized_data/, etc.
```

---

## 3️⃣ Conectar con GitHub

```bash
# Cambiar remote (reemplaza TU_USUARIO con tu usuario GitHub)
git remote add origin https://github.com/TU_USUARIO/medical-automation.git

# Verificar
git remote -v

# Push al repo
git branch -M main
git push -u origin main
```

---

## 4️⃣ Verificar en GitHub

1. Ve a: https://github.com/TU_USUARIO/medical-automation
2. Verifica que ves:
   - ✅ Todos los archivos .py
   - ✅ README.md
   - ✅ CONTRIBUTING.md
   - ✅ .gitignore
   - ❌ raw_data/ (debe estar ignorado)
   - ❌ organized_data/
   - ❌ .env

---

## 5️⃣ Configurar GitHub (Recomendado)

### Proteger la rama main

1. Ve a Settings → Branches
2. Click "Add rule"
3. Branch name pattern: `main`
4. Activar:
   - ✅ Require pull request reviews
   - ✅ Require status checks
   - ✅ Require up-to-date branches
5. Save

### Activar GitHub Actions

1. Ve a Actions
2. Debe mostrar workflow "Security Checks"
3. Verifica que está activo

### Agregar Colaboradores

1. Ve a Settings → Collaborators
2. Click "Add people"
3. Invita a tu equipo

---

## 6️⃣ Para Tu Equipo: Clonar y Contribuir

```bash
# Clonar
git clone https://github.com/TU_USUARIO/medical-automation.git
cd medical-automation

# Leer instrucciones
cat QUICKSTART.md

# Seguir setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con API key

# Probar
python3 scripts/run_all.py

# Crear rama para contribuir
git checkout -b feature/mi-cambio

# Haz cambios, commit, push
git add .
git commit -m "feature: descripción"
git push origin feature/mi-cambio

# Abre Pull Request en GitHub
```

---

## 7️⃣ Estructura de Ramas

```
main (producción)
├── develop (integración)
│   ├── feature/mejor-redaccion
│   ├── feature/tests
│   ├── feature/pdf-export
│   └── ...
└── hotfix/bug-critico
```

**Política de commits:**
- `feature/...` - Nuevas features
- `fix/...` - Bug fixes
- `docs/...` - Solo documentación
- `test/...` - Tests
- `chore/...` - Mantenimiento

---

## 8️⃣ GitHub Issues Template

Para mantener issues organizados, crea `.github/ISSUE_TEMPLATE/bug.md`:

```markdown
---
name: 🐛 Bug Report
about: Reportar un bug
---

## Descripción del Bug
[Descripción clara]

## Pasos para Reproducir
1. ...
2. ...

## Comportamiento Esperado
[Qué debería pasar]

## Comportamiento Actual
[Qué pasó realmente]

## Ambiente
- OS: [Linux/Mac/Windows]
- Python: [3.9/3.10/3.11]
- Versión del proyecto: [rama o commit]

## Logs
[Pegue logs relevantes]
```

---

## ✅ Checklist Final

Antes de compartir el link con tu equipo:

- [ ] Repo está en GitHub
- [ ] .gitignore está funcionando (no muestra datos sensibles)
- [ ] README.md es visible
- [ ] CONTRIBUTING.md es accesible
- [ ] .env.example está en repo
- [ ] Ramas están protegidas
- [ ] GitHub Actions está activo
- [ ] Colaboradores invitados
- [ ] Wiki/Docs están listos (opcional)

---

## 📋 Compartir con el Equipo

Envía este mensaje:

```
¡Hola equipo!

El proyecto de automatización médica está listo en GitHub:
👉 https://github.com/TU_USUARIO/medical-automation

Para empezar:
1. Leer QUICKSTART.md (5 minutos)
2. Leer CONTRIBUTING.md (workflow)
3. Revisar TODO.md (qué hacer)

Preguntas? Abre un Issue.

¡A colaborar! 🚀
```

---

## 🆘 Solución de Problemas

### "fatal: not a git repository"
```bash
git init
```

### "Permission denied" en push
```bash
# Verificar que tienes permisos
git remote -v

# Si usas SSH, generar keys:
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub  # Agregar a GitHub
```

### "Archivo fue comiteado accidentalmente"
```bash
# Si lo hizo en el último commit:
git rm --cached archivo_sensible.txt
git commit --amend --no-edit
git push --force-with-lease

# Si fue hace varios commits:
# Revisa: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

---

**¡Listo! Tu equipo puede empezar a colaborar.** 🎉
