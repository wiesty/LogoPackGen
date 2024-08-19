
# 🌟 SVG to Multi-Format Logo Converter

Convert your SVG logos to various formats effortlessly, including PDF, DXF, AI, PNG, JPG, WebP, and specialized formats for social media, favicons, and more. This tool is designed to make your logo adaptable to any platform or requirement with just a few commands!

## 🚀 Features

-   **Multi-Format Conversion**: Converts SVG logos to PDF, DXF, AI, PNG, JPG, and WebP formats.
-   **High-Quality Output**: Ensures that your images are sharp with adjustable DPI settings and minimal compression.
-   **Social Media Ready**: Generates logos in the perfect dimensions for various social media platforms like Facebook, Instagram, LinkedIn, Twitter, YouTube, Pinterest, TikTok, and X (formerly Twitter).
-   **Favicons**: Creates favicon packs in both `nospace` and `space` variants with adjustable padding.
-   **1x1 Ratio Images**: Produces square images with custom padding for consistent branding.
-   **Background Color Customization**: Define the background color for JPG and WebP images, ensuring your logo looks perfect on any background.
-   **Easy Configuration**: Customize file prefixes, output folders, logo variants, and more through a `.env` file.

## 🛠️ Installation

Before you start, ensure you have the following dependencies installed on your system:

### 1. Install GTK for Windows (if using Windows)

To enable CairoSVG, you'll need the GTK runtime environment. You can install it using the following link:

[GTK for Windows Runtime Environment Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer) 🖥️

### 2. Install Python Packages

Make sure you have Python installed (version 3.6+). Then, install the required Python packages using pip:

bash

Code kopieren

    pip install cairosvg pillow python-dotenv 

## 📝 Configuration

All configurations are done via a `.env` file. Here’s a sample configuration:

bash

Code kopieren

    SVG_FILE=logo.svg
    FILE_PREFIX=MyLogo
    LOGO_VARIANT=dark
    JPG_BACKGROUND_COLOR=255,255,255
    BASE_WIDTH=979
    BASE_HEIGHT=202

-   **`SVG_FILE`**: The path to your SVG file.
-   **`FILE_PREFIX`**: Prefix for the output files.
-   **`LOGO_VARIANT`**: Specify the logo variant (e.g., dark, light).
-   **`JPG_BACKGROUND_COLOR`**: Background color for JPG and WebP images in RGB format.
-   **`BASE_WIDTH`** & **`BASE_HEIGHT`**: The base dimensions of your SVG logo.

## ⚙️ Usage

Run the script using Python:

bash

Code kopieren

    python main.py 

This script will generate the following:

-   **Multi-format logo files**: PDF, PNG, JPG, WebP, etc.
-   **Social media optimized images**: Perfectly sized and padded logos for Facebook, Instagram, LinkedIn, Twitter, YouTube, Pinterest, TikTok, and X.
-   **Favicons**: In both `nospace` and `space` variants with sizes ranging from 16x16 to 128x128.
-   **1x1 ratio images**: With configurable padding.

## 🗂️ Output Structure

Your output files will be organized into the following structure:

    MyLogo_dark/
    │
    ├── MyLogo_normal/
    │   ├── MyLogo_dark_72dpi.png
    │   ├── MyLogo_dark_144dpi.png
    │   ├── MyLogo_dark_300dpi.png
    │   ├── MyLogo_dark.pdf
    │   └── ...
    │
    ├── MyLogo_1x1/
    │   ├── MyLogo_dark_1x1_128px.png
    │   ├── MyLogo_dark_1x1_512px.png
    │   ├── MyLogo_dark_1x1_2048px.png
    │   └── ...
    │
    ├── MyLogo_favicon/
    │   ├── nospace/
    │   │   ├── MyLogo_dark_favicon_16px.png
    │   │   ├── MyLogo_dark_favicon_32px.ico
    │   │   └── ...
    │   └── space/
    │       ├── MyLogo_dark_favicon_16px.png
    │       ├── MyLogo_dark_favicon_32px.ico
    │       └── ...
    │
    └── MyLogo_social_media/
     ├── MyLogo_dark_Facebook_Profile_180x180_72dpi.jpg
        ├── MyLogo_dark_Instagram_Post_1080x1080_96dpi.webp
        └── ...

## 💡 Tips

-   **Adjust Compression**: Modify the `quality` parameter in the script for different levels of JPEG compression to match your quality needs.
-   **Use `.env` Variables**: Easily switch between different configurations by modifying the `.env` file.

## 📜 License

This project is licensed under the MIT License.