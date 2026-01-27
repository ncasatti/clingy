"""
Interactive menu system with fzf integration

Provides a tree-based menu system for building interactive CLI workflows.
Uses fzf for fuzzy finding and selection.
"""

# Standard library
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

# Local
from manager_core.core.colors import Colors
from manager_core.core.emojis import Emojis
from manager_core.core.logger import log_error, log_info


@dataclass
class MenuNode:
    """Represents a node in the interactive menu tree"""

    label: str = ""  # Menu text (static)
    emoji: str = ""  # Optional emoji
    children: List["MenuNode"] = field(default_factory=list)  # Submenus
    action: Optional[Callable[[], bool]] = None  # Function to execute
    data: Dict[str, Any] = field(default_factory=dict)  # Extra context
    label_generator: Optional[Callable[[], str]] = None  # Dynamic label generator

    def is_leaf(self) -> bool:
        """True if it's an executable action (no children)"""
        return len(self.children) == 0 and self.action is not None

    def is_submenu(self) -> bool:
        """True if it has submenus"""
        return len(self.children) > 0

    def display_label(self) -> str:
        """
        Formatted label for display in fzf.

        Uses label_generator if available (for dynamic content),
        otherwise uses static label.
        """
        # Use dynamic label if generator exists
        if self.label_generator is not None:
            text = self.label_generator()
        else:
            text = self.label

        # Add emoji prefix if present
        prefix = self.emoji + " " if self.emoji else ""
        return f"{prefix}{text}"


class MenuRenderer:
    """Renders menu tree using fzf"""

    def __init__(self, root: MenuNode, header: str = "Main Menu"):
        """
        Initialize the menu renderer.

        Args:
            root: Root node of the menu tree
            header: Main header title
        """
        self.root = root
        self.header = header
        self.navigation_stack: List[MenuNode] = [root]
        self.last_esc_time: float = 0.0  # Track last ESC press for double-ESC detection

    def show(self) -> bool:
        """
        Show the menu and handle navigation.

        Returns:
            True if executed successfully, False on error
        """
        current_node = self.root

        while True:
            # If current node is a leaf, execute action and return
            if current_node.is_leaf():
                if current_node.action:
                    try:
                        result = current_node.action()
                        # Return to parent node after execution
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

            # If it's a submenu, show options
            elif current_node.is_submenu():
                selected = self._select_with_fzf(current_node)

                if selected is None:
                    # User cancelled (ESC) - go back or exit with double-ESC
                    if len(self.navigation_stack) > 1:
                        # In submenu - go back
                        self.navigation_stack.pop()
                        current_node = self.navigation_stack[-1]
                    else:
                        # In root - require double ESC to exit
                        current_time = time.time()
                        if current_time - self.last_esc_time < 2.0:
                            # Double ESC detected - exit
                            log_info("Exiting...")
                            return False
                        else:
                            # First ESC - show message and continue
                            log_info("Press ESC again to exit, or select an option")
                            self.last_esc_time = current_time
                            # Continue showing menu (don't change current_node)

                elif selected.label == "Back":
                    # "Back" option selected
                    if len(self.navigation_stack) > 1:
                        self.navigation_stack.pop()
                        current_node = self.navigation_stack[-1]
                    else:
                        return False

                else:
                    # Navigate to selected node
                    self.navigation_stack.append(selected)
                    current_node = selected

            else:
                # Node without children or action - go back
                if len(self.navigation_stack) > 1:
                    self.navigation_stack.pop()
                    current_node = self.navigation_stack[-1]
                else:
                    return False

    def _select_with_fzf(self, node: MenuNode) -> Optional[MenuNode]:
        """
        Use fzf to select an option from the current node.

        Args:
            node: Node whose children will be shown as options

        Returns:
            The selected MenuNode or None if cancelled
        """
        if not node.children:
            return None

        # Build options list with their labels
        options = []
        node_map = {}

        for child in node.children:
            display = child.display_label()
            options.append(display)
            node_map[display] = child

        # Add "Back" option at the end if not at root
        back_label = f"{Emojis.BACK}  Back"
        if len(self.navigation_stack) > 1:
            options.append(back_label)

        # Build breadcrumb header
        breadcrumb = " → ".join([n.label for n in self.navigation_stack])
        header = f"{self.header}\n{Colors.CYAN}{breadcrumb}{Colors.RESET}"

        # Execute fzf
        selected_options = fzf_select(
            options, prompt=f"{node.label} > ", header=header, multi=False
        )

        if not selected_options:
            return None

        selected_display = selected_options[0]

        # If "Back" was selected, return a special node
        if selected_display == back_label:
            return MenuNode(label="Back")

        # Return the corresponding node
        return node_map.get(selected_display)


def fzf_select(
    options: List[str],
    prompt: str = "Select: ",
    header: str = "",
    multi: bool = False,
) -> Optional[List[str]]:
    """
    Generic wrapper for selection with fzf.

    Args:
        options: List of strings to display
        prompt: Prompt text
        header: Header for fzf
        multi: Enable multi-selection

    Returns:
        List of selected options or None if cancelled

    Raises:
        FileNotFoundError: If fzf is not installed
    """
    if not options:
        log_error("No options provided to fzf")
        return None

    # Build fzf command
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

    # Prepare input
    input_data = "\n".join(options)

    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            check=False,  # No raise on non-zero exit
        )

        # Exit code 0: successful selection
        # Any other code: cancelled (ESC/Ctrl+C) or error
        if result.returncode != 0:
            # User cancelled or error - return None
            return None

        # Parse output
        selected = result.stdout.strip()
        if not selected:
            return None

        # Return list of selections
        return selected.split("\n") if multi else [selected]

    except FileNotFoundError:
        log_error(
            "fzf not found. Install it with: brew install fzf (macOS) or sudo apt install fzf (Linux)"
        )
        sys.exit(1)

    except KeyboardInterrupt:
        # Ctrl+C pressed - return None to go back
        return None


def fzf_select_items(
    items: Optional[List[str]] = None,
    prompt: str = "Select items: ",
    include_all: bool = True,
) -> Optional[List[str]]:
    """
    Specific selector for configured items.

    Args:
        items: List of items to select from (if None, uses ITEMS from config)
        prompt: Prompt text
        include_all: Whether to include [ALL ITEMS] option

    Returns:
        List of selected items or None
    """
    # If items not provided, get ITEMS dynamically from config
    if items is None:
        try:
            from config import ITEMS

            items = ITEMS
        except ImportError:
            try:
                from manager_core.config import ITEMS

                items = ITEMS
            except ImportError:
                items = []

    # If no items available, return None
    if not items:
        return None

    options = []

    # Add [ALL ITEMS] option at the beginning
    if include_all:
        options.append(f"{Colors.BOLD}{Colors.GREEN}[ALL ITEMS]{Colors.RESET}")

    # Add individual items
    options.extend(items)

    # Execute fzf with multi-selection
    selected = fzf_select(options, prompt=prompt, header="Use TAB to select multiple", multi=True)

    if not selected:
        return None

    # If [ALL ITEMS] was selected, return all items
    if any("[ALL ITEMS]" in s for s in selected):
        return items  # Return the items list directly

    # Filter control options that may have ANSI codes
    filtered = []
    for s in selected:
        # Remove ANSI codes for comparison
        clean = s.replace(Colors.BOLD, "").replace(Colors.GREEN, "").replace(Colors.RESET, "")
        if clean in items:
            filtered.append(clean)

    return filtered if filtered else None
