from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "white": "#FFFFFF",
    "white_italic": "#FFFFFF italic",
    "white_dim": "#FFFFFF dim",
    "success": "#71d200 bold",
    "warning": "#ffd700 bold",
    "danger": "#ff0d0d bold",
    "info": "#00ffe0",
    "id": "#ff55db italic",
    "date": "#249cff italic",
    "category": "#ffa22c italic",
    "category2": "#ffa22c",
    "amount": "#76ab2c italic",
    "amount2": "#ff4646 italic",
    "budget": "#00974e italic",
    "budget2": "#ccff00 italic",
    "description": "#ffec20 italic",
})

console = Console(theme=custom_theme)
