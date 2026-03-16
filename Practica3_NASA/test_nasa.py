import requests
import sys

NASA_API_KEY = 'DEMO_KEY'
URL_BASE = "https://api.nasa.gov/planetary/apod"

def test_api():
    params = {'api_key': NASA_API_KEY}
    try:
        print(f"Testing NASA API with {NASA_API_KEY}...")
        response = requests.get(URL_BASE, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Image URL: {data.get('url')}")
        else:
            print(f"Error Body: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_api()
