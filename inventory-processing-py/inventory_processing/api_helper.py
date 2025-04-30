import json
import requests
import re


class ApiHelper:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.csrf_token = None
        self.session = requests.Session()
        self._get_csrf_token()

    def _clean_endpoint(self, endpoint: str) -> str:
        """Clean the endpoint by removing leading/trailing slashes and ensuring no double slashes anywhere in the path."""
        # Remove leading/trailing slashes
        endpoint = endpoint.strip('/')
        # Replace any occurrence of multiple slashes with a single slash
        endpoint = re.sub(r'/+', '/', endpoint)
        return endpoint

    def _get_csrf_token(self):
        """Get CSRF token from the Rails application."""
        try:
            # Try to get token from the new inventory unit page
            response = self.session.get(f"{self.base_url}/inventory_units/new")
            print(f"Initial response status: {response.status_code}")
            print(f"Response cookies: {dict(self.session.cookies)}")
            print(f"Response headers: {dict(response.headers)}")

            # Try multiple ways to get the token
            # 1. From meta tag
            csrf_token_match = re.search(
                r'<meta name="csrf-token" content="([^"]+)"', response.text)
            if csrf_token_match:
                self.csrf_token = csrf_token_match.group(1)
                print(f"Found CSRF token in meta tag: {self.csrf_token}")

            # 2. From cookies
            if not self.csrf_token and 'XSRF-TOKEN' in self.session.cookies:
                self.csrf_token = self.session.cookies['XSRF-TOKEN']
                print(f"Found CSRF token in cookies: {self.csrf_token}")

            # 3. From authenticity_token input
            if not self.csrf_token:
                auth_token_match = re.search(
                    r'<input[^>]+name="authenticity_token"[^>]+value="([^"]+)"', response.text)
                if auth_token_match:
                    self.csrf_token = auth_token_match.group(1)
                    print(
                        f"Found CSRF token in input field: {self.csrf_token}")

            if not self.csrf_token:
                print(
                    "Warning: Could not find CSRF token in meta tag, cookies, or input field")
                # Print first 500 chars of response
                print(f"Response text: {response.text[:500]}...")
        except Exception as e:
            print(f"Warning: Could not get CSRF token: {e}")

    def get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}/{self._clean_endpoint(endpoint)}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data, chunk_size: int = 50):
        """
        Post data to the endpoint, splitting large batches into smaller chunks.

        Args:
            endpoint: The API endpoint
            data: List of items to post
            chunk_size: Number of items to send in each request (default: 75)
        """
        url = f"{self.base_url}/{self._clean_endpoint(endpoint)}"

        # Clean up the data
        cleaned_data = []
        for item in data:
            cleaned_item = item.copy()

            # Convert "NONE" to None for department_id
            if cleaned_item.get('department_id') == 'NONE':
                cleaned_item['department_id'] = None

            # Clean up internal_id
            if cleaned_item.get('internal_id') and cleaned_item['internal_id'].startswith('biz_id_'):
                cleaned_item['internal_id'] = cleaned_item['internal_id'].replace(
                    'biz_id_', '')

            # Clean up properties
            if 'properties' in cleaned_item:
                properties = cleaned_item['properties'].copy()
                for key, value in properties.items():
                    if value == 'NULL':
                        properties[key] = None
                cleaned_item['properties'] = properties

            cleaned_data.append(cleaned_item)

        # Split data into chunks
        chunks = [cleaned_data[i:i + chunk_size]
                  for i in range(0, len(cleaned_data), chunk_size)]
        print(
            f"Splitting {len(cleaned_data)} items into {len(chunks)} chunks of {chunk_size} items each")

        results = []
        for i, chunk in enumerate(chunks, 1):
            print(f"Processing chunk {i}/{len(chunks)}")

            # Refresh CSRF token before each chunk
            self._get_csrf_token()

            headers = {
                'Content-Type': 'application/json',
                'X-CSRF-Token': self.csrf_token if self.csrf_token else '',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
            print(f"Sending chunk {i} with headers: {headers}")

            # Send each chunk with the correct parameter name
            payload = {
                'inventory_units': chunk  # Send as a direct array instead of a dictionary
            }
            print(f"Sending chunk {i} with {len(chunk)} items")

            try:
                response = self.session.post(
                    url, json=payload, headers=headers)
                print(f"Chunk {i} response status: {response.status_code}")
                print(f"Chunk {i} response headers: {dict(response.headers)}")

                # Debug the response content
                response_text = response.text
                print(
                    f"Chunk {i} response text (first 500 chars): {response_text[:500]}")

                if not response_text.strip():
                    print("Warning: Empty response received")
                    continue

                # Check if response is HTML (indicating an error)
                if response_text.strip().startswith('<!DOCTYPE html>'):
                    print("Warning: Received HTML response instead of JSON")
                    # Try to extract error message from HTML
                    error_match = re.search(
                        r'<div class="error">(.*?)</div>', response_text, re.DOTALL)
                    if error_match:
                        error_message = error_match.group(1).strip()
                        print(f"Error message from HTML: {error_message}")
                    raise ValueError(
                        "Server returned HTML instead of JSON response")

                try:
                    response_json = response.json()
                    results.append(response_json)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON response: {e}")
                    print(f"Response content: {response_text}")
                    raise

            except Exception as e:
                print(f"Error processing chunk {i}: {str(e)}")
                print(f"Request URL: {url}")
                print(f"Request headers: {headers}")
                print(
                    f"Request payload size: {len(json.dumps(payload))} bytes")
                raise

        return results
