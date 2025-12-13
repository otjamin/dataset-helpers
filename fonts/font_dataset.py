import argparse
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

IMG_SIZE = 1024
MAX_CHARS_PER_LINE = 22
PADDING = 100

text_content = [
    "The quick brown fox jumps over the lazy dog.",
]


def get_fitted_font_and_text(
    text: str,
    font_path: str,
    max_width: int,
    max_height: int,
    draw: ImageDraw.ImageDraw = None,
) -> tuple[ImageFont.FreeTypeFont, str]:
    wrapped_text = textwrap.fill(text, width=MAX_CHARS_PER_LINE)

    font_size = 576
    min_size = 16

    font = ImageFont.truetype(font_path, font_size)

    while font_size > min_size:
        if draw:
            bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        else:
            bbox = font.getbbox(wrapped_text)
        print(bbox)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width < max_width and text_height < max_height:
            return font, wrapped_text

        font_size -= 16
        font = ImageFont.truetype(font_path, font_size)

    return font, wrapped_text


def create_dataset_image(
    text: str,
    font_path: str,
    color: tuple[int, int, int] = (0, 0, 0),
    background: tuple[int, int, int] = (255, 255, 255),
    invert_colors: bool = False,
) -> Image.Image:
    image = Image.new(
        "RGB", (IMG_SIZE, IMG_SIZE), background if not invert_colors else color
    )
    d = ImageDraw.Draw(image)

    max_w = IMG_SIZE - 2 * PADDING
    max_h = max_w
    font, fitted_text = get_fitted_font_and_text(text, font_path, max_w, max_h, d)

    d.text(
        (IMG_SIZE // 2, IMG_SIZE // 2),
        fitted_text,
        font=font,
        fill=color if not invert_colors else background,
        anchor="mm",
    )

    caption = (
        f'[trigger], text saying "{text}", text color '
        + "#%02x%02x%02x" % (color if not invert_colors else background)
        + ", background color "
        + "#%02x%02x%02x" % (background if not invert_colors else color)
    )

    return image, caption


def generate_dataset(font_path: str):
    font_name = Path(font_path).stem
    output_dir = Path("datasets") / font_name
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, text in enumerate(text_content):
        img, cap = create_dataset_image(text, font_path)
        img.save(output_dir / f"{font_name}_{i}.png")

        with open(output_dir / f"{font_name}_{i}.txt", "w") as f:
            f.write(cap)

    for i, text in enumerate(text_content):
        img, cap = create_dataset_image(text, font_path, invert_colors=True)
        img.save(output_dir / f"{font_name}_{i}i.png")

        with open(output_dir / f"{font_name}_{i}i.txt", "w") as f:
            f.write(cap)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate font dataset.")
    parser.add_argument("font_file", type=str, help="Path to the ttf font file.")
    args = parser.parse_args()

    generate_dataset(args.font_file)
