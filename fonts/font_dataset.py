import argparse
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

IMG_SIZE = 1024
MAX_CHARS_PER_LINE = 22
PADDING = 100

text_content = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "Ä",
    "Ö",
    "Ü",
    "ä",
    "ö",
    "ü",
    "ß",
    "&",
    "@",
    "!",
    "?",
    "$",
    "%",
    "€",
    "#",
    "+",
    "-",
    "=",
    "_",
    "/",
    "\\",
    "(",
    ")",
    "In the year 2025.",
    "Call 0123-456-7890 now.",
    "Meeting at 12:30 PM.",
    "Section 7, Page 4.",
    "Price: $19.99 USD",
    "Total: 50% off",
    "Cost: 100€ Euro",
    "Value: £50.00 GBP",
    "Contact user@domain.com",
    "Follow #trending now",
    "http://www.website.com",
    "Hello, world!",
    "Wait; what?",
    "End of sentence.",
    'Quote: "Graphic Design"',
    "(Parentheses test)",
    "[Bracket test]",
    "Äpfel und Öl sind teuer.",
    "Über den Straßen.",
    "Die Straße ist weiß.",
    "Schöne Grüße aus München.",
    "AV",
    "Ta",
    "Vo",
    "Ly",
    "We",
    "Yo",
    "fi",
    "fl",
    "ff",
    "ffi",
    "ffl",
    "Ty",
    "Tw",
    "Va",
    "Ye",
    "The quick brown fox jumps over the lazy dog",
    "Sphinx of black quartz, judge my vow",
    "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern",
    "Victor jagt zwölf Boxkämpfer quer über den großen Sylter Deich",
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
        f"The text '{text}' written in [trigger] typeface, graphic design style. The text is in color "
        + "#%02x%02x%02x" % (color if not invert_colors else background)
        + " on a background of hex "
        + "#%02x%02x%02x" % (background if not invert_colors else color)
        + "."
    )

    return image, caption


def generate_dataset(font_path: str):
    font_name = Path(font_path).stem
    output_dir = Path("datasets") / font_name
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, text in enumerate(text_content):
        img, cap = create_dataset_image(text, font_path)
        img.save(output_dir / f"{font_name}_{i}.png")

        with open(output_dir / f"{font_name}_{i}.txt", "w", encoding="utf-8") as f:
            f.write(cap)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate font dataset.")
    parser.add_argument("font_file", type=str, help="Path to the ttf font file.")
    args = parser.parse_args()

    generate_dataset(args.font_file)
