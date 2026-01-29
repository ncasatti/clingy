# Plan: Migración konfig-manager → Template clingy

## Objetivo
Migrar konfig-manager (linkeo de dotfiles Linux) a template interactivo con fzf.

## Scope
- ✅ Linkeo de archivos/directorios
- ✅ Navegación por grupos
- ✅ Status visual (✓ ✗ ⚠)
- ✅ Acciones interactivas (fzf)
- ❌ Sync (futuro)
- ❌ Requirements (futuro)
- ❌ Install (futuro)

---

## Diseño de Menú

```
📦 KONFIG MANAGER
├── 🔍 Browse Configurations
│   ├── By Group (Hyprland, Themes, Shell, etc.)
│   │   ├── [✓] config → target
│   │   └── Actions (Link All, Unlink All)
│   └── All Configurations (flat list)
├── ⚡ Quick Actions
│   ├── Link All
│   ├── Unlink All
│   ├── Show Status Summary
│   └── Verify Integrity
├── 📊 Status & Info
└── 🚪 Exit
```

---

## Fases

### Fase 1: Estructura Base
- Crear `templates/konfig/`
- Copiar `mappings.py` (50+ configs)
- Crear `config.py` del template

### Fase 2: Core Linking Logic
- `core/link_core.py` - funciones puras (get_status, create_link, remove_link)
- `core/status.py` - status checking y summaries
- LinkStatus enum (LINKED, NOT_LINKED, CONFLICT, WRONG_TARGET, MISSING_SOURCE)

### Fase 3: Comando Browse
- `commands/browse.py` - navegación por grupos
- Menú dinámico con status icons
- Acciones: Link/Unlink individual y por grupo

### Fase 4: Quick Actions
- `commands/quick_actions.py`
- Link All, Unlink All, Status Summary, Verify Integrity

### Fase 5: Status Command
- `commands/status_cmd.py`
- Tablas detalladas, grupos summary, problemas

### Fase 6: Integración
- Emojis específicos
- Confirmaciones con fzf
- Manejo de sudo
- Registrar template en init.py

### Fase 7: Testing
- TESTING.md checklist
- README del template
- Test manual completo

---

## Testing Checklist

```bash
# Setup
clingy init --template konfig
# Edit config.py con KONFIG_PATH
clingy  # Ver menú

# Browse
# - Seleccionar grupo
# - Ver status
# - Link individual
# - Link grupo

# Quick Actions
# - Status Summary → tabla
# - Link All → confirmación
# - Verify → detectar problemas

# Edge cases
# - Missing source → warning
# - Conflict → opciones
# - Sudo → prompt password
```

Ver plan completo en: `.Claude/konfig-migration-plan.md`
