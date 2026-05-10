"""
Dimensions oficials de TheGameCrafter a 300 DPI
Format: {nom: {'w': amplada_polzades, 'h': alçada_polzades, 'bleed': sagnat_polzades}}
"""

DPI = 300
BLEED_DEFAULT = 0.125  # 1/8" (estàndard TGC)

CARDS = {
    'poker': {'w': 2.5, 'h': 3.5, 'bleed': BLEED_DEFAULT},
    'tarot': {'w': 2.75, 'h': 4.75, 'bleed': BLEED_DEFAULT},
    'square': {'w': 3.5, 'h': 3.5, 'bleed': BLEED_DEFAULT},
    'small_square': {'w': 2.5, 'h': 2.5, 'bleed': BLEED_DEFAULT},
    'euro_poker': {'w': 2.48, 'h': 3.46, 'bleed': BLEED_DEFAULT},  # 63x88mm
    'mini': {'w': 1.75, 'h': 2.5, 'bleed': BLEED_DEFAULT},
    'micro': {'w': 1.25, 'h': 1.75, 'bleed': BLEED_DEFAULT},
    'domino': {'w': 1.75, 'h': 3.5, 'bleed': BLEED_DEFAULT},
    'trading': {'w': 2.5, 'h': 3.5, 'bleed': BLEED_DEFAULT},
    'jumbo': {'w': 3.5, 'h': 5.5, 'bleed': BLEED_DEFAULT},
    'divider': {'w': 3.5, 'h': 3.0, 'bleed': BLEED_DEFAULT},
    'circle': {'w': 3.5, 'h': 3.5, 'bleed': BLEED_DEFAULT},  # Diàmetre
    'hex': {'w': 3.75, 'h': 3.75, 'bleed': BLEED_DEFAULT},  # Aprox
}

BOARDS = {
    'square': {'w': 8.0, 'h': 8.0, 'bleed': BLEED_DEFAULT},
    'large': {'w': 10.0, 'h': 10.0, 'bleed': BLEED_DEFAULT},
    'small': {'w': 4.0, 'h': 4.0, 'bleed': BLEED_DEFAULT},
    'quarter': {'w': 5.0, 'h': 5.0, 'bleed': BLEED_DEFAULT},
    'half': {'w': 5.0, 'h': 10.0, 'bleed': BLEED_DEFAULT},
    'domino_board': {'w': 4.0, 'h': 8.0, 'bleed': BLEED_DEFAULT},
    'skinny': {'w': 4.0, 'h': 10.0, 'bleed': BLEED_DEFAULT},
    'sliver': {'w': 2.0, 'h': 8.0, 'bleed': BLEED_DEFAULT},
    'bifold': {'w': 9.0, 'h': 18.0, 'bleed': BLEED_DEFAULT, 'folds': 1},
    'accordion': {'w': 8.0, 'h': 16.0, 'bleed': BLEED_DEFAULT, 'folds': 3},
    'sixfold': {'w': 27.0, 'h': 18.0, 'bleed': BLEED_DEFAULT, 'folds': 5},
    'quadfold': {'w': 18.0, 'h': 18.0, 'bleed': BLEED_DEFAULT, 'folds': 3},
}

DUAL_LAYER = {
    'small': {'w': 3.5, 'h': 5.5, 'glue_zone': 0.5},  # 1/2"
    'medium': {'w': 4.0, 'h': 8.0, 'glue_zone': 0.5},
    'large': {'w': 8.0, 'h': 10.0, 'glue_zone': 0.5},
}
