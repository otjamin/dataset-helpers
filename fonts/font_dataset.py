import argparse
import textwrap
from PIL import Image, ImageDraw, ImageFont

IMAGE_SIZE = (1024, 1024)
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

DESCRIPTION_TEMPLATE = "{}, text saying \"{}\""

TEST_TEXT = "Größe: 176cm, Gewicht: 78kg, Preis: $99.99 (Sonderangebot!)"

FULL_ALPHABET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ"
    "abcdefghijklmnopqrstuvwxyzäöüß"
    "0123456789"
    "!\"$%&?@€#,.:;'()/+-"
)

SAMPLE_WORDS = (
    "Hallo", "Welt", "Fähigkeit", "Überraschung", "Straße",
    "Python3", "Programmierung", "Datenanalyse", "Künstliche"
)

SAMPLE_TEXTS = (
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump!",
    "Sphinx of black quartz, judge my vow.",
    "Äpfel, Öl & Übung: Das kostet 42€ + 15% = 48,30€.",
    "Test123: 50% off! Call @555-7890 or visit example.com/shop.",
    "Größe: 176cm, Gewicht: 78kg, Preis: $99.99 (Sonderangebot!)",
    "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern."
)

def calc_font_size(letter_count, image_width, target_coverage=1.1):
    base_size = image_width // letter_count
    return int(base_size * target_coverage)

def split_text_into_lines(text, max_line_length=28):
    return textwrap.fill(text, width=max_line_length)

def draw_test(font_file):
    img = Image.new("RGB", IMAGE_SIZE, BACKGROUND_COLOR)
    w, h = img.size

    text = split_text_into_lines(TEST_TEXT)

    fnt_size = calc_font_size(len(text.split("\n")[0]), w)
    fnt = ImageFont.truetype(font_file, fnt_size)
    
    d = ImageDraw.Draw(img)

    d.text((w//2, h//2), text, font=fnt, fill=TEXT_COLOR, anchor="mm")

    img.show()

def create_font_dataset(font_file, trigger_word):
    draw_test(font_file)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create font dataset.")
    parser.add_argument("font_file", type=str, help="Path to the ttf font file.")
    parser.add_argument("--trigger-word", "-t", type=str, default="[trigger]", help="Trigger word for the font.")
    args = parser.parse_args()

    create_font_dataset(args.font_file, args.trigger_word)