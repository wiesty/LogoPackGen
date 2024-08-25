import os
import sys
import shutil
from PIL import Image
import cairosvg
from dotenv import load_dotenv

load_dotenv()

svg_file = os.getenv('SVG_FILE', 'logo.svg')
file_prefix = os.getenv('FILE_PREFIX', 'FilePrefix')
logo_variant = os.getenv('LOGO_VARIANT', 'dark')
jpg_background_color = tuple(map(int, os.getenv('JPG_BACKGROUND_COLOR', '255,255,255').split(',')))
base_width = int(os.getenv('BASE_WIDTH', 979))
base_height = int(os.getenv('BASE_HEIGHT', 202))

output_folder = os.path.join(f'{file_prefix}_{logo_variant}')
os.makedirs(output_folder, exist_ok=True)

normal_folder = os.path.join(output_folder, f'{file_prefix}_normal')
os.makedirs(normal_folder, exist_ok=True)

one_by_one_folder = os.path.join(output_folder, f'{file_prefix}_1x1')
os.makedirs(one_by_one_folder, exist_ok=True)

favicon_folder = os.path.join(output_folder, f'{file_prefix}_favicon')
favicon_nospace_folder = os.path.join(favicon_folder, 'nospace')
favicon_space_folder = os.path.join(favicon_folder, 'space')
os.makedirs(favicon_nospace_folder, exist_ok=True)
os.makedirs(favicon_space_folder, exist_ok=True)

social_media_folder = os.path.join(output_folder, f'{file_prefix}_social_media')
os.makedirs(social_media_folder, exist_ok=True)

shutil.copyfile(svg_file, os.path.join(normal_folder, f'{file_prefix}_{logo_variant}.svg'))

def update_progress(current, total, message="Processing"):
    progress = f"{message}: {current}/{total}"
    sys.stdout.write(f"\r{progress}")
    sys.stdout.flush()

def convert_svg_to_formats(svg_path, output_folder):
    cairosvg.svg2pdf(url=svg_path, write_to=os.path.join(output_folder, f'{file_prefix}_{logo_variant}.pdf'))

def create_raster_versions(svg_path, output_folder, dpis=[72, 144, 300]):
    formats = ['png', 'jpg', 'webp']
    total_steps = len(dpis) * len(formats)
    current_step = 0
    
    for dpi in dpis:
        width = int(base_width * dpi / 72)
        height = int(base_height * dpi / 72)
        for fmt in formats:
            current_step += 1
            update_progress(current_step, total_steps, "Rendering DPI versions")
            output_path = os.path.join(output_folder, f'{file_prefix}_{logo_variant}_{dpi}dpi.{fmt}')
            cairosvg.svg2png(url=svg_path, write_to=output_path, output_width=width, output_height=height)
            
            img = Image.open(output_path)
            if fmt == 'jpg':
                img = img.convert('RGBA')
                background = Image.new('RGB', img.size, jpg_background_color)
                background.paste(img, mask=img.split()[3])
                background.save(output_path, 'JPEG', dpi=(dpi, dpi), quality=100)
            elif fmt == 'png' or fmt == 'webp':
                img.save(output_path, fmt.upper(), dpi=(dpi, dpi))

def create_one_by_one_versions(svg_path, output_folder, sizes=[128, 512, 2048, 4096]):
    total_steps = len(sizes) * 2  
    current_step = 0
    
    for size in sizes:
        current_step += 1
        update_progress(current_step, total_steps, "Rendering 1x1 versions")
        output_path = os.path.join(output_folder, f'{file_prefix}_{logo_variant}_1x1_{size}px.png')
        cairosvg.svg2png(url=svg_path, write_to=output_path, output_width=size, output_height=size)
        img = Image.open(output_path)
        width, height = img.size
        new_size = int(size * 1.15)
        new_img = Image.new('RGBA', (new_size, new_size), (255, 255, 255, 0))
        new_img.paste(img, ((new_size - width) // 2, (new_size - height) // 2))
        new_img.save(output_path)

        for fmt in ['jpg', 'webp']:
            current_step += 1
            update_progress(current_step, total_steps, "Rendering 1x1 versions")
            fmt_path = os.path.join(output_folder, f'{file_prefix}_{logo_variant}_1x1_{size}px.{fmt}')
            if fmt == 'jpg':
                background = Image.new('RGB', new_img.size, jpg_background_color)
                alpha = new_img.split()[3]
                background.paste(new_img, mask=alpha)
                background.save(fmt_path, 'JPEG', dpi=(300, 300), quality=100)
            elif fmt == 'webp':
                new_img.save(fmt_path, 'WEBP', dpi=(300, 300)) 

def create_favicon_pack(svg_path, nospace_folder, space_folder):
    favicon_sizes = [16, 32, 48, 64, 128]
    total_steps = len(favicon_sizes) * 3
    current_step = 0
    
    for size in favicon_sizes:
        current_step += 1
        update_progress(current_step, total_steps, "Rendering favicons")
        
        output_path = os.path.join(nospace_folder, f'{file_prefix}_{logo_variant}_favicon_{size}px.png')
        cairosvg.svg2png(url=svg_path, write_to=output_path, output_width=size, output_height=size)
        
        ico_path = os.path.join(nospace_folder, f'{file_prefix}_{logo_variant}_favicon_{size}px.ico')
        img = Image.open(output_path)
        img.save(ico_path, format='ICO', sizes=[(size, size)])

        webp_path = os.path.join(nospace_folder, f'{file_prefix}_{logo_variant}_favicon_{size}px.webp')
        img.save(webp_path, 'WEBP')

        new_size = int(size * 1.15)
        output_path = os.path.join(space_folder, f'{file_prefix}_{logo_variant}_favicon_{size}px.png')
        cairosvg.svg2png(url=svg_path, write_to=output_path, output_width=size, output_height=size)
        img = Image.open(output_path)
        new_img = Image.new('RGBA', (new_size, new_size), (255, 255, 255, 0)) 
        new_img.paste(img, ((new_size - size) // 2, (new_size - size) // 2))
        new_img.save(output_path)

        ico_path = os.path.join(space_folder, f'{file_prefix}_{logo_variant}_favicon_{size}px.ico')
        new_img.save(ico_path, format='ICO', sizes=[(new_size, new_size)])

        webp_path = os.path.join(space_folder, f'{file_prefix}_{logo_variant}_favicon_{size}px.webp')
        new_img.save(webp_path, 'WEBP')

def create_social_media_versions(svg_path, output_folder, dpis=[72, 96]):
    social_media_formats = {
        "Facebook_Profile": {"size": (180, 180), "padding": 0.20},
        "Facebook_Title": {"size": (820, 312), "padding": (0.15, 0.20), "banner": True},
        "Instagram_Profile": {"size": (320, 320), "padding": 0.25},
        "Instagram_Post": {"size": (1080, 1080), "padding": 0.15},
        "Instagram_Story": {"size": (1080, 1920), "padding": (0.10, 0.15)},
        "LinkedIn_Profile": {"size": (400, 400), "padding": 0.20},
        "LinkedIn_Banner": {"size": (1584, 396), "padding": (0.10, 0.15), "banner": True},
        "Twitter_Profile": {"size": (400, 400), "padding": 0.25},
        "Twitter_Banner": {"size": (1500, 500), "padding": (0.10, 0.15), "banner": True},
        "YouTube_Channel": {"size": (2560, 1440), "padding": (0.10, 0.15), "banner": True},
        "Pinterest_Profile": {"size": (165, 165), "padding": 0.25},
        "Pinterest_Board": {"size": (1000, 1500), "padding": (0.10, 0.15)},
        "TikTok_Profile": {"size": (200, 200), "padding": 0.25},
        "TikTok_Cover": {"size": (1920, 1080), "padding": (0.10, 0.15)},
        "X_Profile": {"size": (400, 400), "padding": 0.25},
        "X_Banner": {"size": (1500, 500), "padding": (0.10, 0.15), "banner": True},
    }

    total_steps = len(social_media_formats) * len(dpis) * 2  
    current_step = 0
    
    for name, params in social_media_formats.items():
        size = params["size"]
        padding = params["padding"]
        banner = params.get("banner", False)
        if isinstance(padding, tuple):
            pad_width = int(size[0] * padding[1])
            pad_height = int(size[1] * padding[0])
        else:
            pad_width = int(size[0] * padding)
            pad_height = int(size[1] * padding)

        new_size = (size[0] + 2 * pad_width, size[1] + 2 * pad_height)
        
        if banner:
            adjusted_size = (int(size[0] * 0.5), int(size[1] * 0.5)) 
        else:
            adjusted_size = size
        
        for dpi in dpis:
            current_step += 1
            update_progress(current_step, total_steps, "Rendering social media versions")
            
            output_path = os.path.join(output_folder, f'{file_prefix}_{logo_variant}_{name}_{size[0]}x{size[1]}_{dpi}dpi.png')
            cairosvg.svg2png(url=svg_path, write_to=output_path, output_width=adjusted_size[0], output_height=adjusted_size[1], dpi=dpi)
            
            img = Image.open(output_path)
            new_img = Image.new('RGBA', new_size, (255, 255, 255, 0))
            centered_position = (
                (new_size[0] - adjusted_size[0]) // 2,
                (new_size[1] - adjusted_size[1]) // 2
            )
            new_img.paste(img, centered_position)

            for fmt in ['jpg', 'webp']:
                fmt_path = os.path.join(output_folder, f'{file_prefix}_{logo_variant}_{name}_{size[0]}x{size[1]}_{dpi}dpi.{fmt}')
                background = Image.new('RGB', new_img.size, jpg_background_color) if fmt == 'jpg' else new_img.convert('RGB')
                alpha = new_img.split()[3]
                background.paste(new_img, mask=alpha)
                if fmt == 'jpg':
                    background.save(fmt_path, 'JPEG', dpi=(dpi, dpi), quality=100)
                else:
                    new_img.save(fmt_path, 'WEBP', dpi=(dpi, dpi))

if __name__ == "__main__":
    convert_svg_to_formats(svg_file, normal_folder)
    create_raster_versions(svg_file, normal_folder)
    create_one_by_one_versions(svg_file, one_by_one_folder)
    create_favicon_pack(svg_file, favicon_nospace_folder, favicon_space_folder)
    create_social_media_versions(svg_file, social_media_folder)
    print("\nRendering complete.")
