"""
app/templates.py
BASE DE DADES DE PLANTILLES - THE GAME CRAFTER (TGC)
Conté totes les mides oficials, regles de Bleed (1/8") i Safe Zones.
"""

import math

# ==============================================================================
# ⚙️ CONFIGURACIÓ GLOBAL
# ==============================================================================
DPI = 300
# 1/8" és l'estàndard obligatori per a TGC
BLEED_INCHES = 0.125 
SAFE_ZONE_MARGIN_INCHES = 0.125
GLUE_ZONE_INCHES = 0.5  # Per a Dual Layer Boards

def inches_to_pixels(inches: float) -> int:
    """Converteix polzades a píxels enters (arrodonint per seguretat)"""
    return int(math.ceil(inches * DPI))

def get_standard_bleed_px() -> int:
    """Retorna el sagnat estàndard en píxels"""
    return inches_to_pixels(BLEED_INCHES)

# ==============================================================================
# 🃏 1. CARTES (CARDS)
# Són superfícies planes 2D amb un Bleed al voltant.
# ==============================================================================
CARDS = {
    # Estàndards
    "poker":          {"w": 2.5,  "h": 3.5,  "shape": "rect", "desc": "Estàndard Poker"},
    "square":         {"w": 3.5,  "h": 3.5,  "shape": "rect", "desc": "Carta Quadrada"},
    "small_square":   {"w": 2.5,  "h": 2.5,  "shape": "rect", "desc": "Carta Quadrada Petita"},
    "tarot":          {"w": 2.75, "h": 4.75, "shape": "rect", "desc": "Tarot Estàndard"},
    
    # Variacions
    "mini":           {"w": 1.75, "h": 2.5,  "shape": "rect", "desc": "Mini Card"},
    "micro":          {"w": 1.25, "h": 1.75, "shape": "rect", "desc": "Micro Card"},
    "jumbo":          {"w": 3.5,  "h": 5.5,  "shape": "rect", "desc": "Jumbo Card"},
    "domino":         {"w": 1.75, "h": 3.5,  "shape": "rect", "desc": "Carta Dominó"},
    "divider":        {"w": 3.5,  "h": 3.0,  "shape": "rect", "desc": "Carta Separadora"},
    "trading":        {"w": 2.5,  "h": 3.5,  "shape": "rect", "desc": "Trading Card (TCG)"},
    
    # Internacionals
    "euro_poker":     {"w": 2.48, "h": 3.46, "shape": "rect", "desc": "Euro Poker (63x88mm)"},
    "euro_square":    {"w": 2.76, "h": 2.76, "shape": "rect", "desc": "Euro Square (70x70mm)"},
    "us_game":        {"w": 2.20, "h": 3.43, "shape": "rect", "desc": "US Game Card"},
    
    # Formes especials
    "hex":            {"w": 3.75, "h": 3.75, "shape": "hex",  "desc": "Carta Hexagonal"},
    "circle":         {"w": 3.5,  "h": 3.5,  "shape": "circle","desc": "Carta Circular (diàmetre)"},
    "mint_tin":       {"w": 2.05, "h": 3.43, "shape": "rect", "desc": "Carta per a Caixa Llauna"},
    "crafting_clear": {"w": 2.66, "h": 4.7,  "shape": "rect", "desc": "Carta Transparent (Custom)"},
}

# ==============================================================================
# 📜 2. TAULERS (BOARDS) & MATS
# Requereixen gestió de Fold Lines (plecs).
# ==============================================================================
BOARDS = {
    # Taulers Simples (Sense plecs)
    "square_8":       {"w": 8.0,  "h": 8.0,  "folds": 0, "type": "chipboard"},
    "square_10":      {"w": 10.0, "h": 10.0, "folds": 0, "type": "chipboard"},
    "square_4":       {"w": 4.0,  "h": 4.0,  "folds": 0, "type": "chipboard"},
    "quarter":        {"w": 5.0,  "h": 5.0,  "folds": 0, "type": "chipboard"},
    "half":           {"w": 5.0,  "h": 10.0, "folds": 0, "type": "chipboard"},
    "domino_board":   {"w": 4.0,  "h": 8.0,  "folds": 0, "type": "chipboard"},
    "skinny":         {"w": 4.0,  "h": 10.0, "folds": 0, "type": "chipboard"},
    "sliver":         {"w": 2.0,  "h": 8.0,  "folds": 0, "type": "chipboard"},
    
    # Taulers Plegables (Fold Lines)
    "bifold":         {"w": 9.0,  "h": 18.0, "folds": 1, "type": "chipboard", "axis": "vertical"},
    "accordion":      {"w": 8.0,  "h": 16.0, "folds": 3, "type": "chipboard", "axis": "vertical"},
    "sixfold":        {"w": 27.0, "h": 18.0, "folds": 5, "type": "chipboard", "axis": "vertical"},
    "quadfold":       {"w": 18.0, "h": 18.0, "folds": 3, "type": "chipboard", "axis": "cross"},
    "large_quadfold": {"w": 20.0, "h": 20.0, "folds": 3, "type": "chipboard", "axis": "cross"},
    
    # Taulers Dual Layer (2 cares: Exterior Face + Interior Face)
    # IMPORTANT: La 'Interior Face' té Glue Zone de 1/2" on no va art.
    "dual_small":     {"w": 3.5,  "h": 5.5,  "type": "dual_layer", "glue_zone": GLUE_ZONE_INCHES},
    "dual_medium":    {"w": 4.0,  "h": 8.0,  "type": "dual_layer", "glue_zone": GLUE_ZONE_INCHES},
    "dual_large":     {"w": 8.0,  "h": 10.0, "type": "dual_layer", "glue_zone": GLUE_ZONE_INCHES},
    
    # Mats (Tapets de neoprè)
    "mat_square":     {"w": 8.0,  "h": 8.0,  "folds": 0, "type": "mat"},
    "mat_large":      {"w": 10.0, "h": 16.0, "folds": 0, "type": "mat"},
    "mat_neoprene":   {"w": 24.0, "h": 14.0, "folds": 0, "type": "neoprene"},
}

# ==============================================================================
# 📦 3. CAIXES (BOXES)
# Són plantilles planes (nets) abans de muntar.
# 'panels' defineix les cares que necessiten art (Front, Back, Top, Bottom, Left, Right).
# ==============================================================================
BOXES = {
    # Tuck Boxes (Caixes amb pestanya)
    "poker_tuck_36":  {"w": 2.6, "h": 3.6, "depth": 0.65, "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    "poker_tuck_54":  {"w": 2.6, "h": 3.6, "depth": 0.91, "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    "poker_tuck_72":  {"w": 2.6, "h": 3.6, "depth": 1.18, "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    "poker_tuck_90":  {"w": 2.6, "h": 3.6, "depth": 1.45, "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    "poker_tuck_108": {"w": 2.6, "h": 3.6, "depth": 1.72, "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    
    # Square Tuck
    "square_tuck_48": {"w": 3.6, "h": 3.85,"depth": 0.82, "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    "square_tuck_96": {"w": 3.6, "h": 3.85,"depth": 1.54, "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    
    # Tarot Tuck
    "tarot_tuck_40":  {"w": 2.85,"h": 4.85, "depth": 0.7,  "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    "tarot_tuck_90":  {"w": 2.85,"h": 4.85, "depth": 1.45, "type": "tuck", "panels": ["front", "back", "top", "bottom"]},
    
    # Hook Boxes (Tapa i Base separades)
    # Requereixen 2 fitxers PNG: 'lid' (tapa) i 'base'.
    "poker_hook_54":  {"w": 2.6, "h": 3.6, "depth": 0.8,  "type": "hook", "parts": ["lid", "base"]},
    "poker_hook_72":  {"w": 2.6, "h": 3.6, "depth": 1.0,  "type": "hook", "parts": ["lid", "base"]},
    "poker_hook_108": {"w": 2.58,"h": 3.62, "depth": 1.59, "type": "hook", "parts": ["lid", "base"]},
    "square_hook_48": {"w": 3.58,"h": 3.78, "depth": 0.83, "type": "hook", "parts": ["lid", "base"]},
    "square_hook_96": {"w": 3.57,"h": 3.84, "depth": 1.48, "type": "hook", "parts": ["lid", "base"]},
    "tarot_hook_40":  {"w": 2.79,"h": 4.79, "depth": 0.63, "type": "hook", "parts": ["lid", "base"]},
    "tarot_hook_90":  {"w": 2.79,"h": 4.79, "depth": 1.3,  "type": "hook", "parts": ["lid", "base"]},
    
    # Stout Boxes (Caixes robustes - Requereixen Wrap complet)
    "stout_large":    {"w": 11.0, "h": 11.0, "depth": 3.23, "type": "wrap", "panels": ["lid", "base_sides"]},
    "stout_medium":   {"w": 6.13, "h": 9.0,  "depth": 2.25, "type": "wrap", "panels": ["lid", "base_sides"]},
    "stout_small":    {"w": 4.0,  "h": 6.0,  "depth": 2.25, "type": "wrap", "panels": ["lid", "base_sides"]},
    
    # Especials
    "mint_tin":       {"w": 2.46, "h": 3.88, "depth": 0.85, "type": "wrap", "panels": ["lid", "base_sides"]},
}

# ==============================================================================
# 📚 4. LLIBRES (BOOKLETS & BOOKS)
# Requereixen generació seqüencial (Pàgines, Portades).
# ==============================================================================
BOOKS = {
    # Booklets (Grapats / Saddle Stitch)
    "small_booklet":      {"w": 2.5,  "h": 3.5,  "binding": "saddle_stitch", "bleed": BLEED_INCHES},
    "medium_booklet":     {"w": 3.5,  "h": 5.0,  "binding": "saddle_stitch", "bleed": BLEED_INCHES},
    "large_booklet":      {"w": 5.0,  "h": 8.0,  "binding": "saddle_stitch", "bleed": BLEED_INCHES},
    "jumbo_booklet":      {"w": 8.0,  "h": 10.0, "binding": "saddle_stitch", "bleed": BLEED_INCHES},
    "tall_booklet":       {"w": 4.5,  "h": 8.0,  "binding": "saddle_stitch", "bleed": BLEED_INCHES},
    "tarot_booklet":      {"w": 2.75, "h": 4.75, "binding": "saddle_stitch", "bleed": BLEED_INCHES},
    
    # Llibres Encunyats (Perfect Bound) - Necessiten càlcul de llomada
    "letter_perfect":     {"w": 8.51, "h": 11.0, "binding": "perfect", "bleed": BLEED_INCHES},
    
    # Coil Books (Espiral)
    "medium_coil":        {"w": 5.61, "h": 7.5,  "binding": "coil", "bleed": BLEED_INCHES},
    
    # Documents i Folios
    "document":           {"w": 8.5,  "h": 11.0, "binding": "single", "bleed": BLEED_INCHES},
    "poker_folio":        {"w": 10.0, "h": 3.5,  "binding": "folded", "bleed": BLEED_INCHES},
}

# ==============================================================================
# 🎲 5. ALTRES PARTS (OTHER PARTS)
# Majoritàriament textures o formes simples.
# ==============================================================================
OTHER_PARTS = {
    "dice_d6":      {"size": "16mm", "faces": 6, "type": "dice"},
    "dice_d4":      {"size": "19mm", "faces": 4, "type": "dice"},
    "dice_d8":      {"size": "23mm", "faces": 8, "type": "dice"},
    "meeple":       {"size": "17x16mm", "type": "token"},
    "acrylic_large":{"size": "267x229mm", "type": "token"},
    "play_money":   {"w": 2.0, "h": 3.5, "type": "card_like"},
}

# ==============================================================================
# 🛠️ UTILITATS DE CÀLCUL
# ==============================================================================

def get_dimensions_px(item_dict: dict) -> dict:
    """
    Calcula les dimensions exactes en píxels (Canvas i Safe Zone)
    per a un component donat.
    """
    w = item_dict.get("w", 0)
    h = item_dict.get("h", 0)
    
    # Si l'element no té mides directes (com una caixa que usa 'panels'), retorna 0
    if w == 0 and h == 0:
        return {"canvas_w": 0, "canvas_h": 0}

    bleed = item_dict.get("bleed", BLEED_INCHES)
    
    # Canvas total = Mida + Bleed per tots dos costats
    total_w_in = w + (bleed * 2)
    total_h_in = h + (bleed * 2)
    
    canvas_w = inches_to_pixels(total_w_in)
    canvas_h = inches_to_pixels(total_h_in)
    
    # Safe Zone = Mida real + marges interiors
    safe_margin_px = inches_to_pixels(bleed + SAFE_ZONE_MARGIN_INCHES)
    
    return {
        "canvas_w": canvas_w,
        "canvas_h": canvas_h,
        "trim_w": inches_to_pixels(w),
        "trim_h": inches_to_pixels(h),
        "safe_margin_px": safe_margin_px,
        "safe_area_w": canvas_w - (safe_margin_px * 2),
        "safe_area_h": canvas_h - (safe_margin_px * 2),
    }

def find_best_box(card_count: int, card_type: str) -> str:
    """
    Recomana la millor caixa segons el nombre de cartes.
    Lògica aproximada de TGC.
    """
    prefix = card_type.split("_")[0] # ex: 'poker', 'square'
    
    if prefix == "poker":
        if card_count <= 36: return "poker_tuck_36"
        elif card_count <= 54: return "poker_tuck_54"
        elif card_count <= 72: return "poker_tuck_72"
        elif card_count <= 90: return "poker_tuck_90"
        else: return "poker_tuck_108"
    elif prefix == "square":
        if card_count <= 48: return "square_tuck_48"
        else: return "square_tuck_96"
    elif prefix == "tarot":
        if card_count <= 40: return "tarot_tuck_40"
        else: return "tarot_tuck_90"
    
    return "poker_tuck_54" # Default
