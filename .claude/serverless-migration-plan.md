# Plan: Migración manager-serverless → Template serverless

## Objetivo
Migrar clingy para AWS Lambda + Go a template interactivo con fzf.

## Scope
- ✅ Build/Zip/Deploy de funciones Go
- ✅ CloudWatch Logs (tail, filtering)
- ✅ Invoke (local/remoto) con payloads composables
- ✅ CloudWatch Insights (queries predefinidas)
- ✅ Status (list functions, check deps)

## Diseño de Menú

```
🚀 SERVERLESS MANAGER
├── 📦 Functions (Build, Zip, Deploy, Clean)
├── 🔍 Logs & Monitoring (View, Tail, Insights)
├── ▶️ Invoke (Local/Remote con payloads)
├── 📊 Status & Info
└── 🚪 Exit
```

## Fases

### Fase 1: Estructura + Config (Pasos 1-2)
- Crear directorios (commands/, core/, core_commands/)
- config.py con GO_FUNCTIONS, AWS settings

### Fase 2: Core Utilities (Pasos 3-6)
- payload_composer.py
- payload_navigator.py
- insights_queries.py
- insights_formatter.py

### Fase 3: Comandos Core (Pasos 7-13)
- build.py, zip.py, deploy.py
- logs.py, invoke.py, insights.py
- clean.py
- Cambiar imports: manager.* → clingy.*

### Fase 4: Menú Functions (Paso 14)
- functions.py con MenuNode
- Build/Zip/Deploy con fzf
- Full Pipeline (Build → Zip → Deploy)

### Fase 5: Menús Logs & Invoke (Pasos 15-16)
- logs_menu.py (View, Tail, Insights)
- invoke_menu.py (Local/Remote, PayloadNavigator)

### Fase 6: Status (Paso 17-20)
- status.py (List, Build Status, Deps, Config)
- __init__.py exports

### Fase 7: Integración (Paso 21)
- Registrar template en init.py

### Fase 8: Testing (Pasos 22-26)
- Functions workflow
- Logs workflow
- Invoke workflow
- Status workflow

### Fase 9: Docs (Paso 27)
- README.md con Quick Start

---

## Comandos a Migrar

| Comando | Migrar a | Líneas |
|---------|----------|--------|
| build.py | core_commands/ | ~176 |
| zip.py | core_commands/ | ~150 |
| deploy.py | core_commands/ | ~323 |
| logs.py | core_commands/ | ~361 |
| invoke.py | core_commands/ | ~928 |
| insights.py | core_commands/ | ~823 |
| clean.py | core_commands/ | ~100 |

**Total estimado:** ~3500 líneas

Ver plan completo en: `.Claude/serverless-migration-plan.md`
