# Color Story Generator Microservice

A microservice for [Chromatic Tales](https://github.com/mirna-lopez/chromatic-tales.git) that accepts a [color palette](https://developer.mozilla.org/en-US/docs/Web/CSS/color) and an optional genre, then uses the [Anthropic Claude API](https://docs.anthropic.com/en/api/getting-started) to generate a short creative story inspired by the mood and atmosphere of those colors.

---

## 1. What this microservice does

Given a palette of 1–5 [HEX colors](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) and an optional genre, the microservice returns a 2–3 paragraph AI-generated story whose tone, atmosphere, and imagery are influenced by the provided colors.

**Supported genres:**

| Genre | Description |
|-------|-------------|
| fantasy | Magic, myth, and wonder (default) |
| noir | Dark, moody, detective atmosphere |
| romance | Emotional, warm, relationship-driven |
| horror | Unsettling, tense, frightening |
| sci-fi | Futuristic, technological, space-age |

---

## 2. How to REQUEST data from the microservice

The microservice must be running before any request is made.

### Setup

Install the required dependencies and set your API key before starting the server.

```bash
# Install dependencies
pip install flask anthropic

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_api_key_here

# Start the microservice
python app.py
```

The microservice runs on `http://localhost:5001`.

### Endpoint

Send an [HTTP GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET) request to:http://localhost:5001/story
with these query parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| palette | string ([HEX](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color)) | Yes | One or more HEX colors (e.g. `#FF5733`). Pass multiple by repeating the param. Max 5. |
| genre | string | No | One of: `fantasy`, `noir`, `romance`, `horror`, `sci-fi`. Defaults to `fantasy`. |

### Example requests

**Single color, default genre**

This example sends one color with no genre specified. The microservice defaults to `fantasy` and returns a story based on that color's mood.

```python
import requests

response = requests.get(
    "http://localhost:5001/story",
    params={"palette": "#FF5733"}
)
```

**Multiple colors with a specific genre**

This example sends three dark HEX colors with the `horror` genre. The microservice reads all three colors together and uses their combined atmosphere to shape the story's tone.

```python
import requests

response = requests.get(
    "http://localhost:5001/story",
    params={
        "palette": ["#0D0D0D", "#C70039", "#900C3F"],
        "genre": "horror"
    }
)
```

**Max palette with sci-fi genre**

This example sends the maximum of five colors with the `sci-fi` genre. Using a full palette gives the AI more color context to work with, which tends to produce more varied and detailed imagery.

```python
import requests

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

The microservice always responds with [JSON](https://www.json.org/json-en.html).

### Success response : HTTP 200

When the request is valid, you get back the generated story along with the palette and genre that were used.

```json
{
  "story": "The plains burned amber and rust as Kira stepped beyond the village walls...",
  "palette": ["#FF5733", "#C70039", "#900C3F"],
  "genre": "fantasy"
}
```

| Field | Type | Description |
|-------|------|-------------|
| story | string | The AI-generated story, 2–3 paragraphs long |
| palette | array of strings | The HEX colors that were passed in |
| genre | string | The genre that was used (including the default if none was specified) |

### Error response: HTTP 400

When a parameter is invalid or missing, you get back an error message describing what went wrong.

```json
{
  "error": "'notacolor' is not a valid HEX color (e.g. #FF5733)."
}
```

### Full example: sending a request and using the response

This example shows a complete request and response flow. It sends three colors with the `fantasy` genre, checks the [HTTP status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status), and either prints the story or the error message depending on what came back.

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

A [UML Sequence Diagram](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-sequence-diagram/) shows how the different parts of a system communicate with each other over time, in order. This one maps out the full lifecycle of a request to the Color Story Generator.

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
| `palette is required.` | No palette param provided |
| `palette accepts a maximum of 5 colors.` | More than 5 colors passed |
| `'X' is not a valid HEX color.` | A color does not match HEX format |
| `genre must be one of: ...` | Unrecognized genre string |
