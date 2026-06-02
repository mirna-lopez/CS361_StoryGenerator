from dotenv import load_dotenv
load_dotenv()

import anthropic
from flask import Flask, request, jsonify

app = Flask(__name__)
client = anthropic.Anthropic()

VALID_GENRES = ["fantasy", "noir", "romance", "horror", "sci-fi"]


def is_valid_hex(color):
    """Check if a string is a valid HEX color (e.g. #FF5733)."""
    if not color.startswith("#"):
        return False
    hex_part = color[1:]
    if len(hex_part) not in (3, 6):
        return False
    try:
        int(hex_part, 16)
        return True
    except ValueError:
        return False

def validate_params(palette_raw, genre):
    """Validate palette and genre inputs. Returns an error string, or None if valid."""
    if not palette_raw:
        return "palette is required. Provide at least one HEX color (e.g. palette=%23FF5733)."
    if len(palette_raw) > 5:
        return "palette accepts a maximum of 5 colors."
    for color in palette_raw:
        if not is_valid_hex(color):
            return f"'{color}' is not a valid HEX color (e.g. #FF5733)."
    if genre not in VALID_GENRES:
        return f"genre must be one of: {', '.join(VALID_GENRES)}."
    return None

def build_prompt(palette_raw, genre):
    """Build the story generation prompt from palette and genre. Returns a prompt string."""
    palette_str = ", ".join(palette_raw)
    return (
        f"You are a creative story writer. Given the following color palette: {palette_str}, "
        f"write a short {genre} story (2-3 paragraphs) inspired by the mood, tone, and feeling "
        f"these colors evoke. Do not mention the hex codes directly — let the colors influence "
        f"the atmosphere and imagery instead."
    )

def call_claude(prompt):
    """Send prompt to Claude API. Returns the generated story text."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text

@app.route("/story", methods=["GET"])
def generate_story():
    # Parse & validate parameters
    palette_raw = request.args.getlist("palette")
    genre = request.args.get("genre", "fantasy").lower()

    error = validate_params(palette_raw,genre)
    if error:
        return jsonify({"error":error}),400

    # Build prompt
    prompt = build_prompt(palette_raw,genre)

    #Call Anthropic API
    story_text = call_claude(prompt)

    return jsonify({
        "story": story_text,
        "palette": palette_raw,
        "genre": genre
    }), 200


if __name__ == "__main__":
    app.run(port=5001, debug=True)
