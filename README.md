# Story Generator Microservice

A microservice for **Chromatic Tales** that accepts a color palette and an optional genre, then uses the Anthropic Claude API to generate a short creative story inspired by the mood and atmosphere of those colors.

---

## 1. What this microservice does

Given a palette of 1–5 HEX colors and an optional genre, the microservice returns a 2–3 paragraph AI-generated story whose tone, atmosphere, and imagery are influenced by the provided colors.

**Supported genres:**

| Genre | Description |
|-------|-------------|
| `fantasy` | Magic, myth, and wonder (default) |
| `noir` | Dark, moody, detective atmosphere |
| `romance` | Emotional, warm, relationship-driven |
| `horror` | Unsettling, tense, frightening |
| `sci-fi` | Futuristic, technological, space-age |

---

## 2. How to REQUEST data from the microservice

The microservice must be running before any request is made.

```bash
# Install dependencies
pip install flask anthropic

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_api_key_here

# Start the microservice
python app.py
```

The microservice runs on **`http://localhost:5001`**.

Send an **HTTP GET** request to:

```
http://localhost:5001/story
```

with these query parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `palette` | string (HEX) | ✅ Yes | One or more HEX colors (e.g. `#FF5733`). Pass multiple by repeating the param. Max 5. |
| `genre` | string | ❌ No | One of: `fantasy`, `noir`, `romance`, `horror`, `sci-fi`. Defaults to `fantasy`. |

### Example requests

```python
import requests

# Single color, default genre (fantasy)
response = requests.get(
    "http://localhost:5001/story",
    params={"palette": "#FF5733"}
)

# Three colors, horror genre
response = requests.get(
    "http://localhost:5001/story",
    params={
        "palette": ["#0D0D0D", "#C70039", "#900C3F"],
        "genre": "horror"
    }
)

# Five colors, sci-fi genre
response = requests.get(
    "http://localhost:5001/story",
    params={
        "palette": ["#0D0D0D", "#1A1AFF", "#00FFFF", "#FF00FF", "#FFFFFF"],
        "genre": "sci-fi"
    }
)
```

---

## 3. How to RECEIVE data from the microservice

The microservice always responds with JSON.

### Success response — HTTP 200

```json
{
  "story": "The plains burned amber and rust as Kira stepped beyond the village walls...",
  "palette": ["#FF5733", "#C70039", "#900C3F"],
  "genre": "fantasy"
}
```

### Error response — HTTP 400

```json
{
  "error": "'notacolor' is not a valid HEX color (e.g. #FF5733)."
}
```

### Example: receiving and using the data

```python
import requests

response = requests.get(
    "http://localhost:5001/story",
    params={
        "palette": ["#FF5733", "#C70039", "#900C3F"],
        "genre": "fantasy"
    }
)

if response.status_code == 200:
    data = response.json()
    story = data["story"]       # The generated story string
    palette = data["palette"]   # List of HEX strings that were used
    genre = data["genre"]       # Genre that was used
    print(story)
else:
    error = response.json()["error"]
    print(f"Error: {error}")
```

---

## 4. UML Sequence Diagram

See `uml_sequence_diagram.png` in this repository.

The diagram covers:
- Microservice startup requirement
- HTTP GET request with parameters
- Parameter validation
- Anthropic API call
- Success path (HTTP 200 + JSON story)
- Error path (HTTP 400 + JSON error message)

---

## 5. Error Reference

| Error | Cause |
|-------|-------|
| `palette is required.` | No `palette` param provided |
| `palette accepts a maximum of 5 colors.` | More than 5 colors passed |
| `'X' is not a valid HEX color.` | A color doesn't match HEX format |
| `genre must be one of: ...` | Unrecognized genre string |
