"""
app/generator.py
MOTOR DE GENERACIÓ D'IMATGES PER A THE GAME CRAFTER
Utilitza Pillow per crear PNGs d'alta resolució (300 DPI)
respectant els marges de sagnat (Bleed) i zones de seguretat.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from app.templates import get_dimensions_px, CARDS, BOARDS, inches_to_pixels

# RUTA ON ES GUARDARAN ELS ARXIUS
OUTPUT_DIR = "output"

def get_font(size):
    """
    Intenta carregar una font truetype. 
    Si falla, utilitza la font per defecte de Pillow.
    """
    try:
        # Intenta carregar Arial o una font del sistema
        # Ajusta aquesta ruta si tens una font específica al teu projecte
        return ImageFont.truetype("arial.ttf", size) 
    except IOError:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    """
    Parteix el text en múltiples línies perquè no s'escapi de la zona segura.
    """
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        # Mesura l'amplada del text
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width < max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    lines.append(" ".join(current_line))
    return lines

def generate_card(component_key: str, title: str, description: str) -> str:
    """
    Genera un fitxer PNG per a una carta.
    
    Args:
        component_key: Clau del diccionari CARDS (ex: "poker", "tarot")
        title: Títol de la carta
        description: Text o efecte de la carta
    """
    if component_key not in CARDS:
        raise ValueError(f"Component '{component_key}' no trobat a templates.py")

    template = CARDS[component_key]
    dims = get_dimensions_px(template)
    
    # 1. Crear Canvas (Inclou Bleed)
    # Fons blanc per defecte
    img = Image.new('RGB', (dims['canvas_w'], dims['canvas_h']), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 2. Dibuixar un marc decoratiu (DINS de la Safe Zone per demostrar que funciona)
    # El marc és a 20px dins de la zona segura
    margin = dims['safe_margin_px'] + 20
    border_x0 = margin
    border_y0 = margin
    border_x1 = dims['canvas_w'] - margin
    border_y1 = dims['canvas_h'] - margin
    
    draw.rectangle([border_x0, border_y0, border_x1, border_y1], outline="black", width=3)
    
    # 3. Dibuixar Text (Títol i Descripció)
    # Títol
    title_font = get_font(40)
    desc_font = get_font(24)
    
    # Mesurar títol per centrar-lo
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (dims['canvas_w'] - title_w) // 2
    
    # Posició Y del títol (una mica més avall de la vora superior segura)
    title_y = dims['safe_margin_px'] + 40
    
    draw.text((title_x, title_y), title, fill="black", font=title_font, anchor="mm")
    
    # Descripció (Text amb salt de línia)
    # Amplada màxima = Amplada zona segura
    safe_w = dims['safe_area_w']
    
    # Calculem on comença el text de descripció (al centre vertical aprox)
    desc_y_start = dims['canvas_h'] // 2 + 40
    
    lines = wrap_text(draw, description, desc_font, safe_w - 40)
    
    line_height = 30
    for i, line in enumerate(lines):
        # Centrar línia
        line_bbox = draw.textbbox((0, 0), line, font=desc_font)
        line_w = line_bbox[2] - line_bbox[0]
        line_x = (dims['canvas_w'] - line_w) // 2
        line_y = desc_y_start + (i * line_height)
        
        draw.text((line_x, line_y), line, fill="black", font=desc_font)

    # 4. Guardar PNG
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{component_key}_{title.lower().replace(' ', '_')}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Guardem amb qualitat màxima i informació DPI
    img.save(filepath, dpi=(300, 300))
    print(f"✅ Generat: {filepath}")
    return filepath

def generate_board(component_key: str, board_name: str) -> str:
    """
    Genera un fitxer PNG per a un tauler.
    """
    if component_key not in BOARDS:
        raise ValueError(f"Component '{component_key}' no trobat a templates.py")

    template = BOARDS[component_key]
    dims = get_dimensions_px(template)
    
    # 1. Crear Canvas
    # Fons verd clar (simulant gespa o taula)
    img = Image.new('RGB', (dims['canvas_w'], dims['canvas_h']), color=(144, 238, 144))
    draw = ImageDraw.Draw(img)
    
    # 2. Dibuixar línies de referència (Opcional, per veure les zones)
    # Línia de tall (Trim Line)
    margin_bleed = dims['safe_margin_px'] - inches_to_pixels(0.125) # Restem el safe zone per tornar al trim
    draw.rectangle([margin_bleed, margin_bleed, dims['canvas_w']-margin_bleed, dims['canvas_h']-margin_bleed], outline="red", width=2)

    # 3. Títol del tauler
    title_font = get_font(60)
    draw.text((dims['canvas_w']/2, dims['canvas_h']/2), board_name, fill="white", font=title_font, anchor="mm")

    # 4. Guardar
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"board_{component_key}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    img.save(filepath, dpi=(300, 300))
    print(f"✅ Generat: {filepath}")
    return filepath

# ==============================================================================
# 🧪 PROVES RÀPIDES (Executa això per provar)
# ==============================================================================
if __name__ == "__main__":
    print("--- Iniciant generador de proves ---")
    try:
        # Prova 1: Carta Poker
        generate_card(
            component_key="poker",
            title="DRAC DE FOC",
            description="Llança 3 daus de foc. Si surt 6, l'enemic perd 10 vides."
        )
        
        # Prova 2: Tauler Bifold
        generate_board(
            component_key="bifold",
            board_name="TAULER DE BATALLA"
        )
        print("--- Generació completada! ---")
    except Exception as e:
        print(f"❌ Error: {e}")
