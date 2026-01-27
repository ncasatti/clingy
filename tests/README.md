# Manager-Core Test Suite

Test suite básico para el framework manager-core usando pytest.

## Estructura

```
tests/
├── __init__.py                  # Inicializador del paquete
├── conftest.py                  # Fixtures compartidos
├── test_discovery.py            # Tests de detección de contexto
├── test_command_discovery.py    # Tests de auto-discovery de comandos
└── test_init_command.py         # Tests del comando init
```

## Ejecución

### Correr todos los tests

```bash
pytest tests/ -v
```

### Correr tests específicos

```bash
# Solo tests de discovery
pytest tests/test_discovery.py -v

# Solo tests de command discovery
pytest tests/test_command_discovery.py -v

# Solo tests del comando init
pytest tests/test_init_command.py -v

# Test específico
pytest tests/test_discovery.py::TestFindManagerRoot::test_finds_project_in_current_directory -v
```

### Con coverage

```bash
# Reporte en terminal
pytest tests/ --cov=manager_core --cov-report=term-missing

# Reporte HTML
pytest tests/ --cov=manager_core --cov-report=html
# Abre: htmlcov/index.html
```

### Modo watch (requiere pytest-watch)

```bash
pip install pytest-watch
ptw tests/
```

## Fixtures Disponibles

### `temp_project`
Crea una estructura temporal de proyecto manager-core con:
- Directorio `commands/`
- Archivo `config.py` con configuración básica

### `temp_project_with_command`
Extiende `temp_project` agregando:
- Comando de prueba `TestCommand` en `commands/test_command.py`

### `empty_dir`
Crea un directorio vacío sin estructura de proyecto.

## Cobertura Actual

- **discovery.py**: 88% (detección de contexto)
- **init.py**: 73% (comando de inicialización)
- **commands/__init__.py**: 69% (auto-discovery)
- **core/emojis.py**: 100% (emojis)
- **core/dependency.py**: 100% (dependencias)

## Tests Incluidos

### test_discovery.py (14 tests)

**TestFindManagerRoot**
- ✅ Encuentra proyecto en directorio actual
- ✅ Busca hacia arriba en directorios
- ✅ Retorna None si no encuentra proyecto
- ✅ Se detiene en raíz del filesystem
- ✅ Requiere ambos `commands/` y `config.py`

**TestValidProjectDetection**
- ✅ Detecta proyecto válido
- ✅ Rechaza si falta `commands/`
- ✅ Rechaza si falta `config.py`
- ✅ Acepta `commands/` vacío

**TestLoadProjectConfig**
- ✅ Carga config.py exitosamente
- ✅ Lanza error si falta config.py
- ✅ Lanza error si config.py tiene errores de sintaxis

**TestGetProjectContext**
- ✅ Retorna contexto para proyecto válido
- ✅ Retorna None si no hay proyecto

### test_command_discovery.py (6 tests)

**TestDiscoverCommands**
- ✅ Descubre comandos del framework
- ✅ Descubre comandos del proyecto
- ✅ Retorna diccionario de comandos
- ✅ Comandos tienen atributos requeridos

**TestCommandValidation**
- ✅ Ignora clases que no heredan de BaseCommand
- ✅ Ignora BaseCommand mismo

### test_init_command.py (7 tests)

**TestInitCommand**
- ✅ Crea estructura de proyecto
- ✅ Crea template básico con comandos de ejemplo
- ✅ Falla si proyecto ya existe (sin --force)
- ✅ Sobrescribe con --force
- ✅ Falla con template inválido
- ✅ Comando tiene nombre correcto
- ✅ Comando tiene texto de ayuda

## Próximos Pasos

Para expandir la cobertura:

1. **Tests de CLI** (`test_cli.py`)
   - Pruebas de modo interactivo
   - Pruebas de modo CLI
   - Integración con fzf

2. **Tests de Menu** (`test_menu.py`)
   - Navegación de menú
   - Selección múltiple
   - Rendering de nodos

3. **Tests de Logger** (`test_logger.py`)
   - Salida de logs
   - Colores y emojis
   - Estadísticas

4. **Tests de Integración** (`test_integration.py`)
   - Flujo completo init → run
   - Carga de comandos del proyecto
   - Ejecución de comandos

## Notas

- Los tests usan `tmp_path` de pytest para directorios temporales
- Los fixtures se definen en `conftest.py` para reutilización
- Se usa `monkeypatch` para mockar funciones cuando es necesario
- Los tests son independientes y pueden ejecutarse en cualquier orden
