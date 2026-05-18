"""
test_program.py — Test program for the Story Generator Microservice
Demonstrates: making a request, receiving a response, and handling errors.

Make sure the microservice is running before executing this file:
    python app.py
"""

import requests

BASE_URL = "http://localhost:5001/story"


def print_divider(label):
    print(f"\n{'=' * 55}")
    print(f"  {label}")
    print('=' * 55)


# Test 1: Valid request:fantasy genre, 3-color palette
print_divider("Test 1: Fantasy story from a warm palette")
response = requests.get(
    BASE_URL,
    params={
        "palette": ["#FF5733", "#C70039", "#900C3F"],
        "genre": "fantasy"
    }
)
if response.status_code == 200:
    data = response.json()
    print(f"Genre  : {data['genre']}")
    print(f"Palette: {data['palette']}")
    print(f"\nStory:\n{data['story']}")
else:
    print(f"Error {response.status_code}: {response.json()['error']}")


#Test 2: Valid request: sci-fi genre, 5-color palette
print_divider("Test 2: Sci-fi story from a cool/neon palette")
response = requests.get(
    BASE_URL,
    params={
        "palette": ["#0D0D0D", "#1A1AFF", "#00FFFF", "#FF00FF", "#FFFFFF"],
        "genre": "sci-fi"
    }
)
if response.status_code == 200:
    data = response.json()
    print(f"Genre  : {data['genre']}")
    print(f"Palette: {data['palette']}")
    print(f"\nStory:\n{data['story']}")
else:
    print(f"Error {response.status_code}: {response.json()['error']}")


# Test 3: Default genre (no genre param)
print_divider("Test 3: Default genre (fantasy) — monochromatic palette")
response = requests.get(
    BASE_URL,
    params={"palette": ["#6A0DAD", "#8B00FF", "#9B30FF"]}
)
if response.status_code == 200:
    data = response.json()
    print(f"Genre  : {data['genre']}")
    print(f"Palette: {data['palette']}")
    print(f"\nStory:\n{data['story']}")
else:
    print(f"Error {response.status_code}: {response.json()['error']}")


#Test 4: Error:invalid HEX color
print_divider("Test 4: Error — invalid HEX color")
response = requests.get(
    BASE_URL,
    params={"palette": ["notacolor"], "genre": "horror"}
)
print(f"Status : {response.status_code}")
print(f"Response: {response.json()}")


#Test 5: Error: missing palette
print_divider("Test 5: Error — missing palette")
response = requests.get(BASE_URL, params={"genre": "noir"})
print(f"Status : {response.status_code}")
print(f"Response: {response.json()}")


# Test 6: Error:invalid genre 
print_divider("Test 6: Error — invalid genre")
response = requests.get(
    BASE_URL,
    params={"palette": ["#FF5733"], "genre": "western"}
)
print(f"Status : {response.status_code}")
print(f"Response: {response.json()}")
