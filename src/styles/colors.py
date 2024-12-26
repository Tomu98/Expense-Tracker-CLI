from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "white": "#FFFFFF",
    "white_italic": "#FFFFFF italic",
    "white_dim": "#FFFFFF dim",
    "success": "#78dd00",
    "warning": "#ffcc00",
    "danger": "#ce4040",
    "id": "#FFFFFF italic dim",
    "date": "#69d3ff italic",
    "category": "#cc73ff italic",
    "category2": "#cc73ff",
    "amount": "#76ab2c italic",
    "amount2": "#ce4040 italic",
    "budget": "#008d5c italic",
    "budget2": "#ccff00 italic",
})

console = Console(theme=custom_theme)
