# Plan: Refactor a manager-core (Context-Aware CLI Framework)

## Objetivo
Transformar el proyecto actual en un framework CLI instalable con detección de contexto, similar a Git/Poetry/Terraform.

## Comportamiento deseado
- `pip install manager-core` → instala framework globalmente
- `manager init` → crea proyecto con commands/ y config.py
- `manager` → detecta proyecto automáticamente y carga comandos

---

## Fase 0: Preparación

### Paso 0.1: Crear backup del estado actual
```bash
git add -A && git commit -m "chore: backup before manager-core refactor"
```

---

## Fase 1: Renombrar Package

### Paso 1.1: Renombrar directorio
```bash
mv manager manager_core
```

### Paso 1.2: Actualizar todos los imports
Cambiar en TODOS los archivos:
- `from manager.` → `from manager_core.`
- `import manager.` → `import manager_core.`

### Paso 1.3: Actualizar pyproject.toml
```toml
[project]
name = "manager-core"
[project.scripts]
manager = "manager_core.cli:main"
```

### Paso 1.4: Actualizar manager.py
```python
from manager_core.cli import main
```

### Paso 1.5: Test
```bash
python manager.py greet --language es
python manager.py info
```

---

## Fase 2: Sistema de Discovery

### Paso 2.1: Crear manager_core/core/discovery.py
Implementar:
- `find_manager_root()` - busca hacia arriba
- `load_project_config()` - carga config.py dinámico
- `get_project_context()` - combina ambos

### Paso 2.2: Exportar en __init__.py

---

## Fase 3: CLI Context-Aware

### Paso 3.1: Crear manager_core/cli_builder.py
- `CLIContext` class
- `create_cli_context()` - detecta proyecto
- `_discover_project_commands()` - carga comandos del proyecto

### Paso 3.2: Refactorizar cli.py
```python
def main():
    ctx = create_cli_context()
    
    if not ctx.has_project:
        if sys.argv[1] != "init":
            log_error("No project found. Run: manager init")
            sys.exit(1)
    
    # Use ctx.commands instead of discover_commands()
```

---

## Fase 4: Comando init

### Paso 4.1: Crear manager_core/commands/init.py
- Copiar template a directorio actual
- Validar que no exista proyecto
- Opción --force para sobreescribir

---

## Fase 5: Templates

### Paso 5.1-5.6: Crear templates/basic/
- config.py
- commands/__init__.py
- commands/greet.py
- commands/info.py
- commands/calculator.py

---

## Fase 6: Limpieza

### Paso 6.1: Eliminar comandos de ejemplo
Eliminar de manager_core/commands/:
- greet.py, files.py, calculator.py, info.py, list_items.py, requirements.py

### Paso 6.2: Convertir config.py en framework config

---

## Fase 7: Config Dinámico

### Paso 7.1: Modificar base.py
Cambiar ITEMS estático por dinámico:
```python
def _get_items():
    try:
        from project_config import ITEMS
    except ImportError:
        from manager_core.config import ITEMS
    return ITEMS
```

### Paso 7.2: Modificar menu.py
Mismo cambio para fzf_select_items()

---

## Fase 8: Eliminar Wrapper

```bash
rm manager.py
```

---

## Fase 9: Documentación

- Actualizar AGENTS.md
- Actualizar README.md

---

## Fase 10: Tests

```bash
cd /tmp && mkdir test-manager && cd test-manager
python -m manager_core.cli init
python -m manager_core.cli
```

---

## Fase 11: Commit

```bash
git add -A
git commit -m "refactor!: rename to manager-core with context detection"
```
