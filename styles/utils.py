from PIL import Image, ImageDraw, ImageFont
import os
import random

def generate_flyer(
    product,
    entreprise="Adora Care Style",
    contact="690389086",
    promo="-50%",
):
    """Génère un flyer simple et stylé avec grande image et numéro WhatsApp visible"""
    
    # Configuration
    flyer_size = (1080, 1350)  # Format vertical
    margin = 30
    colors = {
        'bg': '#1a659e',     # Bleu foncé
        'accent': '#ffd60a', # Jaune vif
        'text': '#ffffff'   # Blanc
    }
    
    # Création du fond
    flyer = Image.new('RGB', flyer_size, color=colors['bg'])
    draw = ImageDraw.Draw(flyer)
    
    # Polices
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 50)
        font_medium = ImageFont.truetype("arial.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Grande image produit (90% de la hauteur)
    if product.images.exists():
        img = Image.open(product.images.first().image.path).convert("RGB")
        
        # Calcul de la taille pour prendre 90% de la hauteur
        target_height = int(flyer_size[1] * 0.9)
        ratio = target_height / img.height
        new_width = int(img.width * ratio)
        
        img = img.resize((new_width, target_height), Image.LANCZOS)
        img_pos = ((flyer_size[0] - new_width)//2, margin)
        flyer.paste(img, img_pos)
    
    # Zone inférieure avec les informations
    info_height = flyer_size[1] - int(flyer_size[1] * 0.9) - margin
    info_y = flyer_size[1] - info_height
    
    # Fond semi-transparent pour les infos
    info_bg = Image.new('RGBA', (flyer_size[0], info_height), (0, 0, 0, 150))
    flyer.paste(info_bg, (0, info_y), info_bg)
    
    # Nom de l'entreprise
    draw.text(
        (flyer_size[0]//2, info_y + 20),
        entreprise.upper(),
        font=font_large,
        fill=colors['accent'],
        anchor='mt'
    )
    
    # Promotion
    draw.text(
        (flyer_size[0]//2, info_y + 80),
        f"PROMO {promo}",
        font=font_medium,
        fill=colors['text'],
        anchor='mt'
    )
    
    # Numéro WhatsApp avec icône
    whatsapp_text = f""
    draw.text(
        (flyer_size[0]//2, info_y + info_height - 50),
        whatsapp_text,
        font=font_medium,
        fill=colors['accent'],
        anchor='mb'
    )
    
    # Sauvegarde
    output_path = f"media/campaigns/flyer_{product.id}_{random.randint(1000, 9999)}.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    flyer.save(output_path, quality=95)
    
    return output_path