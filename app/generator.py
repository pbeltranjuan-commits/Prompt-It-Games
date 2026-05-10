"""
Generador automàtic de components per a TheGameCrafter
Genera PNGs amb bleed, safe zone i text correctament posicionat
"""

from PIL import Image, ImageDraw, ImageFont
from app.templates import CARDS, BOARDS, DUAL_LAYER, DPI
import os

def inches_to_pixels(inches):
    """Converteix polzades a píxels a 300 DPI"""
    return int(inches * DPI)

def create_card(card_type: str, title: str, description: str, art_path: str = None) -> str:
    """
    Genera una carta amb el format especificat
    Retorna la ruta del PNG generat
    """
    template = CARDS.get(card_type)
    if not template:
        raise ValueError(f"Tipus de carta desconegut: {card_type}")
    
    # Mides amb bleed
    width_px = inches_to_pixels(template['w'] + template['bleed'] * 2)
    height_px = inches_to_pixels(template['h'] + template['bleed'] * 2)
    
    # Crear canvas
    img = Image.new('RGB', (width_px, height_px), 'white')
    draw = ImageDraw.Draw(img)
    
    # Afegir art de fons si n'hi ha
    if art_path and os.path.exists(art_path):
        art = Image.open(art_path).resize((width_px, height_px))
        img.paste(art, (0, 0))
        draw = ImageDraw.Draw(img)
    
    # Safe zone margins (1/8" inside trim line)
    margin = inches_to_pixels(template['bleed'] + template['bleed'])
    
    # Configuració de text
    try:
        title_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 36)
        text_font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Dibuixar títol (part superior)
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width_px - title_width) // 2
    draw.text((title_x, margin + 10), title, fill='black', font=title_font)
    
    # Dibuixar descripció (part inferior)
    y_pos = height_px - margin - 50
    # Wrap text simple
    words = description.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=text_font)
        if bbox[2] - bbox[0] < width_px - (margin * 2):
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    
    for i, line in enumerate(lines[-3:]):  # Màxim 3 línies
        line_bbox = draw.textbbox((0, 0), line, font=text_font)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = (width_px - line_width) // 2
        draw.text((line_x, y_pos + i*28), line, fill='black', font=text_font)
    
    # Guardar PNG
    output_dir = f"output/{card_type}_cards"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{title.lower().replace(' ', '_')}.png"
    img.save(filename)
    
    return filename

def create_board(board_type: str, design_type: str = 'simple') -> str:
    """
    Genera un tauler amb el format especificat
    design_type: 'simple', 'bifold', 'accordion'
    """
    template = BOARDS.get(board_type)
    if not template:
        raise ValueError(f"Tipus de tauler desconegut: {board_type}")
    
    width_px = inches_to_pixels(template['w'] + template['bleed'] * 2)
    height_px = inches_to_pixels(template['h'] + template['bleed'] * 2)
    
    img = Image.new('RGB', (width_px, height_px), '#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Afegir zones de referència (opcional, per depuració)
    # Bleed zone (gris)
    bleed_px = inches_to_pixels(template['bleed'])
    draw.rectangle([0, 0, width_px, height_px], fill='#e0e0e0')
    
    # Trim zone (blanc)
    trim_x0, trim_y0 = bleed_px, bleed_px
    trim_x1, trim_y1 = width_px - bleed_px, height_px - bleed_px
    draw.rectangle([trim_x0, trim_y0, trim_x1, trim_y1], fill='white')
    
    # Safe zone (verd clar)
    safe_margin = inches_to_pixels(template['bleed'])
    safe_x0, safe_y0 = trim_x0 + safe_margin, trim_y0 + safe_margin
    safe_x1, safe_y1 = trim_x1 - safe_margin, trim_y1 - safe_margin
    draw.rectangle([safe_x0, safe_y0, safe_x1, safe_y1], outline='#00ff00', width=2)
    
    # Dibuixar fold lines si cal
    if template.get('folds'):
        fold_color = '#00aa00'
        if board_type == 'bifold':
            mid_x = width_px // 2
            draw.line([(mid_x, 0), (mid_x, height_px)], fill=fold_color, width=4)
        elif board_type == 'accordion':
            fold_positions = [width_px // 4, width_px // 2, width_px * 3 // 4]
            for x in fold_positions:
                draw.line([(x, 0), (x, height_px)], fill=fold_color, width=4)
    
    # Guardar PNG
    output_dir = f"output/{board_type}_boards"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{board_type}_board.png"
    img.save(filename)
    
    return filename

if __name__ == "__main__":
    # Proves ràpides
    print("Generant carta Poker...")
    card_path = create_card('poker', "Dragó de Foc", "Ataca 3 punts de dany a tots els enemics adjacents")
    print(f"✅ Carta generada: {card_path}")
    
    print("\nGenerant tauler Square...")
    board_path = create_board('square')
    print(f"✅ Tauler generat: {board_path}")
