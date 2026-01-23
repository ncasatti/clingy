"""
Interactive menu system with fzf integration

Provides a tree-based menu system for building interactive CLI workflows.
Uses fzf for fuzzy finding and selection.
"""

# Standard library
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

# Local
from manager.core.colors import Colors, Emojis
from manager.core.logger import log_error, log_info


@dataclass
class MenuNode:
    """Representa un nodo en el árbol de menús interactivos"""

    label: str  # Texto del menú
    emoji: str = ""  # Emoji opcional
    children: List["MenuNode"] = field(default_factory=list)  # Submenús
    action: Optional[Callable[[], bool]] = None  # Función a ejecutar
    data: Dict[str, Any] = field(default_factory=dict)  # Contexto extra

    def is_leaf(self) -> bool:
        """True si es una acción ejecutable (sin hijos)"""
        return len(self.children) == 0 and self.action is not None

    def is_submenu(self) -> bool:
        """True si tiene submenús"""
        return len(self.children) > 0

    def display_label(self) -> str:
        """Label formateado para mostrar en fzf"""
        prefix = self.emoji + "  " if self.emoji else ""
        return f"{prefix}{self.label}"


class MenuRenderer:
    """Renderiza árbol de menús usando fzf"""

    def __init__(self, root: MenuNode, header: str = "Main Menu"):
        """
        Inicializa el renderizador de menús.

        Args:
            root: Nodo raíz del árbol de menús
            header: Título del header principal
        """
        self.root = root
        self.header = header
        self.navigation_stack: List[MenuNode] = [root]

    def show(self) -> bool:
        """
        Muestra el menú y maneja la navegación.

        Returns:
            True si se ejecutó correctamente, False en caso de error
        """
        current_node = self.root

        while True:
            # Si el nodo actual es una hoja, ejecutar acción y volver
            if current_node.is_leaf():
                if current_node.action:
                    try:
                        result = current_node.action()
                        # Volver al nodo padre después de ejecutar
                        if len(self.navigation_stack) > 1:
                            self.navigation_stack.pop()
                            current_node = self.navigation_stack[-1]
                        else:
                            return result
                    except Exception as e:
                        log_error(f"Error executing action: {str(e)}")
                        if len(self.navigation_stack) > 1:
                            self.navigation_stack.pop()
                            current_node = self.navigation_stack[-1]
                        else:
                            return False
                else:
                    return False

            # Si es un submenú, mostrar opciones
            elif current_node.is_submenu():
                selected = self._select_with_fzf(current_node)

                if selected is None:
                    # Usuario canceló (ESC) - volver atrás o salir
                    if len(self.navigation_stack) > 1:
                        self.navigation_stack.pop()
                        current_node = self.navigation_stack[-1]
                    else:
                        return False

                elif selected.label == "Back":
                    # Opción "Back" seleccionada
                    if len(self.navigation_stack) > 1:
                        self.navigation_stack.pop()
                        current_node = self.navigation_stack[-1]
                    else:
                        return False

                else:
                    # Navegar al nodo seleccionado
                    self.navigation_stack.append(selected)
                    current_node = selected

            else:
                # Nodo sin hijos ni acción - volver
                if len(self.navigation_stack) > 1:
                    self.navigation_stack.pop()
                    current_node = self.navigation_stack[-1]
                else:
                    return False

    def _select_with_fzf(self, node: MenuNode) -> Optional[MenuNode]:
        """
        Usa fzf para seleccionar una opción del nodo actual.

        Args:
            node: Nodo cuyos hijos se mostrarán como opciones

        Returns:
            El MenuNode seleccionado o None si se canceló
        """
        if not node.children:
            return None

        # Construir lista de opciones con sus labels
        options = []
        node_map = {}

        for child in node.children:
            display = child.display_label()
            options.append(display)
            node_map[display] = child

        # Agregar opción "Back" al final si no estamos en root
        back_label = f"{Emojis.BACK}  Back"
        if len(self.navigation_stack) > 1:
            options.append(back_label)

        # Construir header del breadcrumb
        breadcrumb = " → ".join([n.label for n in self.navigation_stack])
        header = f"{self.header}\n{Colors.CYAN}{breadcrumb}{Colors.RESET}"

        # Ejecutar fzf
        selected_options = fzf_select(
            options, prompt=f"{node.label} > ", header=header, multi=False
        )

        if not selected_options:
            return None

        selected_display = selected_options[0]

        # Si seleccionó "Back", retornar un nodo especial
        if selected_display == back_label:
            return MenuNode(label="Back")

        # Retornar el nodo correspondiente
        return node_map.get(selected_display)


def fzf_select(
    options: List[str],
    prompt: str = "Select: ",
    header: str = "",
    multi: bool = False,
) -> Optional[List[str]]:
    """
    Wrapper genérico para selección con fzf.

    Args:
        options: Lista de strings a mostrar
        prompt: Texto del prompt
        header: Header para fzf
        multi: Habilitar multi-selección

    Returns:
        Lista de opciones seleccionadas o None si canceló

    Raises:
        FileNotFoundError: Si fzf no está instalado
    """
    if not options:
        log_error("No options provided to fzf")
        return None

    # Construir comando fzf
    cmd = [
        "fzf",
        "--prompt",
        prompt,
        "--height",
        "40%",
        "--border",
        "--ansi",
        "--reverse",
    ]

    if header:
        cmd.extend(["--header", header])

    if multi:
        cmd.append("--multi")

    # Preparar input
    input_data = "\n".join(options)

    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            check=False,  # No raise on non-zero exit
        )

        # Exit code 0: selección exitosa
        # Exit code 1: sin selección (ESC)
        # Exit code 130: CTRL+C
        if result.returncode == 130:
            # CTRL+C - propagar interrupción
            raise KeyboardInterrupt

        if result.returncode != 0:
            # ESC o error - retornar None
            return None

        # Parsear output
        selected = result.stdout.strip()
        if not selected:
            return None

        # Retornar lista de selecciones
        return selected.split("\n") if multi else [selected]

    except FileNotFoundError:
        log_error(
            "fzf not found. Install it with: brew install fzf (macOS) or sudo apt install fzf (Linux)"
        )
        sys.exit(1)

    except KeyboardInterrupt:
        log_info("Operation cancelled by user")
        sys.exit(0)


def fzf_select_items(
    prompt: str = "Select items: ", include_all: bool = True
) -> Optional[List[str]]:
    """
    Selector específico para items configurados.

    Args:
        prompt: Texto del prompt
        include_all: Si incluir opción [ALL ITEMS]

    Returns:
        Lista de items seleccionados o None
    """
    from manager.config import ITEMS

    options = []

    # Agregar opción [ALL ITEMS] al principio
    if include_all:
        options.append(f"{Colors.BOLD}{Colors.GREEN}[ALL ITEMS]{Colors.RESET}")

    # Agregar items individuales
    options.extend(ITEMS)

    # Ejecutar fzf con multi-selección
    selected = fzf_select(
        options, prompt=prompt, header="Use TAB to select multiple", multi=True
    )

    if not selected:
        return None

    # Si seleccionó [ALL ITEMS], retornar todos los items
    if any("[ALL ITEMS]" in s for s in selected):
        return ITEMS

    # Filtrar las opciones de control que puedan tener códigos ANSI
    filtered = []
    for s in selected:
        # Eliminar códigos ANSI para comparación
        clean = (
            s.replace(Colors.BOLD, "")
            .replace(Colors.GREEN, "")
            .replace(Colors.RESET, "")
        )
        if clean in ITEMS:
            filtered.append(clean)

    return filtered if filtered else None
