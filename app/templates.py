"""
TheGameCrafter Templates Database
Mides oficials i especificacions d'impressió per a generació automàtica.
"""

# Constant de resolució
DPI = 300

# Marges estàndard TGC (en polzades)
BLEED = 0.125       # 1/8" - Sagnat obligatori
SAFE_ZONE = 0.125   # 1/8" dins del trim line per a text/elements crítics
GLUE_ZONE = 0.5     # 1/2" per a Dual Layer Boards

def in_to_px(inches: float) -> int:
    """Converteix polzades a píxels a 300 DPI"""
    return int(inches * DPI)

def mm_to_in(mm: float) -> float:
    """Converteix mm a polzades"""
    return mm / 25.4

# ==============================================================================
# 🃏 CARTES (Requireixen PNG amb bleed + safe zone)
# ==============================================================================
CARDS = {
    "poker":          {"w": 2.5,   "h": 3.5,   "folds": 0},
    "tarot":          {"w": 2.75,  "h": 4.75,  "folds": 0},
    "square":         {"w": 3.5,   "h": 3.5,   "folds": 0},
    "small_square":   {"w": 2.5,   "h": 2.5,   "folds": 0},
    "euro_poker":     {"w": 2.48,  "h": 3.46,  "folds": 0},  # 63x88mm
    "euro_square":    {"w": 2.76,  "h": 2.76,  "folds": 0},  # 70x70mm
    "mini":           {"w": 1.75,  "h": 2.5,   "folds": 0},
    "micro":          {"w": 1.25,  "h": 1.75,  "folds": 0},
    "domino":         {"w": 1.75,  "h": 3.5,   "folds": 0},
    "jumbo":          {"w": 3.5,   "h": 5.5,   "folds": 0},
    "divider":        {"w": 3.5,   "h": 3.0,   "folds": 0},
    "circle":         {"w": 3.5,   "h": 3.5,   "folds": 0, "shape": "circle"},
    "hex":            {"w": 3.75,  "h": 3.75,  "folds": 0, "shape": "hex"},
    "mint_tin":       {"w": 2.05,  "h": 3.43,  "folds": 0},  # 52x87mm
    "trading":        {"w": 2.5,   "h": 3.5,   "folds": 0},
    "us_game":        {"w": 2.2,   "h": 3.43,  "folds": 0},  # 56x87mm
    "crafting_clear": {"w": 2.66,  "h": 4.7,   "folds": 0, "notes": "Clear card - white ink = transparent"},
}

# ==============================================================================
# 📜 TAULERS & TAPETS (Requireixen PNG amb bleed + fold lines)
# ==============================================================================
BOARDS = {
    # Taulers rígids
    "square_8":       {"w": 8.0,   "h": 8.0,   "folds": 0},
    "square_10":      {"w": 10.0,  "h": 10.0,  "folds": 0},
    "square_4":       {"w": 4.0,   "h": 4.0,   "folds": 0},
    "quarter":        {"w": 5.0,   "h": 5.0,   "folds": 0},
    "half":           {"w": 5.0,   "h": 10.0,  "folds": 0},
    "domino_board":   {"w": 4.0,   "h": 8.0,   "folds": 0},
    "skinny":         {"w": 4.0,   "h": 10.0,  "folds": 0},
    "sliver":         {"w": 2.0,   "h": 8.0,   "folds": 0},
    "bifold":         {"w": 9.0,   "h": 18.0,  "folds": 1},
    "accordion":      {"w": 8.0,   "h": 16.0,  "folds": 3},
    "sixfold":        {"w": 27.0,  "h": 18.0,  "folds": 5},
    "quadfold":       {"w": 18.0,  "h": 18.0,  "folds": 3},
    "large_quadfold": {"w": 20.0,  "h": 20.0,  "folds": 3},
    # Tapets (mates) - Mateixa lògica de bleed, material diferent
    "mat_square":     {"w": 8.0,   "h": 8.0,   "folds": 0, "material": "mat"},
    "mat_large":      {"w": 10.0,  "h": 16.0,  "folds": 0, "material": "mat"},
    "mat_hex":        {"w": 5.25,  "h": 4.5,   "folds": 0, "material": "mat"},
    "mat_neoprene":   {"w": 24.0,  "h": 14.0,  "folds": 0, "material": "neoprene"},
    "mat_spinner":    {"w": 8.0,   "h": 8.0,   "folds": 0, "material": "mat"},
}

# ==============================================================================
# 📦 TAULERS DUAL LAYER (Requereixen 2 PNGs: exterior + interior + glue zone)
# ==============================================================================
DUAL_LAYER = {
    "small_dl":  {"w": 3.5,  "h": 5.5,  "glue_zone": GLUE_ZONE},
    "medium_dl": {"w": 4.0,  "h": 8.0,  "glue_zone": GLUE_ZONE},
    "large_dl":  {"w": 8.0,  "h": 10.0, "glue_zone": GLUE_ZONE},
}

# ==============================================================================
# 📦 CAIXES (NO generen PNG amb bleed. TGC usa dielines oficials. Només referència)
# ==============================================================================
BOXES = {
    "poker_hook_18":    {"w": 2.6, "h": 3.6, "depth": 0.37, "cards": 18},
    "poker_hook_36":    {"w": 2.57,"h": 3.59,"depth": 0.61, "cards": 36},
    "poker_hook_54":    {"w": 2.6, "h": 3.6, "depth": 0.8,  "cards": 54},
    "poker_hook_72":    {"w": 2.6, "h": 3.6, "depth": 1.0,  "cards": 72},
    "poker_hook_90":    {"w": 2.56,"h": 3.62,"depth": 1.35, "cards": 90},
    "poker_hook_108":   {"w": 2.58,"h": 3.62,"depth": 1.59, "cards": 108},
    "poker_tuck_36":    {"w": 2.6, "h": 3.6, "depth": 0.65, "cards": 36},
    "poker_tuck_54":    {"w": 2.6, "h": 3.6, "depth": 0.91, "cards": 54},
    "poker_tuck_72":    {"w": 2.6, "h": 3.6, "depth": 1.18, "cards": 72},
    "poker_tuck_90":    {"w": 2.6, "h": 3.6, "depth": 1.45, "cards": 90},
    "poker_tuck_108":   {"w": 2.6, "h": 3.6, "depth": 1.72, "cards": 108},
    "square_hook_48":   {"w": 3.58,"h": 3.78,"depth": 0.83, "cards": 48},
    "square_hook_96":   {"w": 3.57,"h": 3.84,"depth": 1.48, "cards": 96},
    "tarot_hook_40":    {"w": 2.79,"h": 4.79,"depth": 0.63, "cards": 40},
    "tarot_hook_90":    {"w": 2.79,"h": 4.79,"depth": 1.3,  "cards": 90},
    "large_stout":      {"w": 11.0,"h": 11.0,"depth": 3.23, "type": "stout"},
    "medium_stout":     {"w": 6.13,"h": 9.0, "depth": 2.25, "type": "stout"},
    "small_stout":      {"w": 4.0, "h": 6.0, "depth": 2.25, "type": "stout"},
    "mint_tin":         {"w": 2.46,"h": 3.88,"depth": 0.85, "type": "tin"},
    "vhs":              {"w": 7.9, "h": 4.82,"depth": 1.08, "type": "vhs"},
}

# ==============================================================================
# 🎲 ALTRES COMPONENTS (Catàleg TGC - No generen PNG)
# ==============================================================================
OTHER_PARTS = {
    "dice_d6":   {"size": "16mm", "shape": "cube"},
    "dice_d4":   {"size": "19x17mm", "shape": "tetrahedron"},
    "dice_d8":   {"size": "23x17mm", "shape": "octahedron"},
    "meeple":    {"size": "17x16mm", "material": "wood"},
    "acrylic_large": {"size": "267x229mm", "thickness": "3mm"},
    "acrylic_small": {"size": "203x102mm", "thickness": "6mm"},
    "play_money":{"size": "2x3.5in", "material": "paper"},
}

# ==============================================================================
# 🛠️ UTILITATS PER AL GENERADOR
# ==============================================================================
def get_template(category: str, name: str) -> dict | None:
    """Retorna la plantilla o None si no existeix"""
    cat_map = {
        "card": CARDS,
        "board": BOARDS,
        "dual_layer": DUAL_LAYER,
        "box": BOXES,
        "other": OTHER_PARTS
    }
    return cat_map.get(category, {}).get(name)

def get_png_dimensions(template: dict) -> dict:
    """Calcula les dimensions en píxels incloent bleed"""
    if not template:
        raise ValueError("Template no trobat")
    
    w_px = in_to_px(template["w"] + (BLEED * 2))
    h_px = in_to_px(template["h"] + (BLEED * 2))
    safe_x = in_to_px(BLEED + SAFE_ZONE)
    safe_y = in_to_px(BLEED + SAFE_ZONE)
    safe_w = w_px - (safe_x * 2)
    safe_h = h_px - (safe_y * 2)
    
    return {
        "canvas_w": w_px,
        "canvas_h": h_px,
        "safe_x": safe_x,
        "safe_y": safe_y,
        "safe_w": safe_w,
        "safe_h": safe_h,
        "trim_w": in_to_px(template["w"]),
        "trim_h": in_to_px(template["h"]),
    }
