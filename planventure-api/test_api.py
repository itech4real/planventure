#!/usr/bin/env python
import json
import urllib.request
import urllib.error
import sys

BASE_URL = 'http://127.0.0.1:5000'

def make_request(endpoint, method='GET', data=None):
    """Make an HTTP request and return status, response."""
    url = BASE_URL + endpoint
    headers = {'Content-Type': 'application/json'}
    
    req_data = None
    if data:
        req_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=req_data, method=method, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8')
            try:
                parsed = json.loads(body)
            except:
                parsed = body
            return response.status, parsed
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            parsed = json.loads(body)
        except:
            parsed = body
        return e.code, parsed
    except Exception as e:
        return None, str(e)

# Test 1: Health check
print("=" * 50)
print("TEST 1: GET /health")
print("=" * 50)
status, response = make_request('/health')
print(f"Status: {status}")
print(f"Response: {json.dumps(response, indent=2)}\n")

# Test 2: Register a new user
print("=" * 50)
print("TEST 2: POST /auth/register")
print("=" * 50)
user_data = {
    'username': 'testuser456',
    'email': 'test456@example.com',
    'password': 'StrongPass1!'
}
print(f"Request Body: {json.dumps(user_data, indent=2)}")
status, response = make_request('/auth/register', 'POST', user_data)
print(f"Status: {status}")
print(f"Response: {json.dumps(response, indent=2)}\n")

# Test 3: Login
print("=" * 50)
print("TEST 3: POST /auth/login")
print("=" * 50)
login_data = {
    'username': 'testuser456',
    'password': 'StrongPass1!'
}
print(f"Request Body: {json.dumps(login_data, indent=2)}")
status, response = make_request('/auth/login', 'POST', login_data)
print(f"Status: {status}")
print(f"Response: {json.dumps(response, indent=2)}")

if status == 200 and isinstance(response, dict) and 'access_token' in response:
    access_token = response['access_token']
    print(f"\nAccess Token: {access_token[:20]}...\n")
    
    # Test 4: Get trips with token
    print("=" * 50)
    print("TEST 4: GET /trips (with auth)")
    print("=" * 50)
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    url = BASE_URL + '/trips'
    req = urllib.request.Request(url, method='GET', headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode('utf-8')
            parsed = json.loads(body)
            print(f"Status: {resp.status}")
            print(f"Response: {json.dumps(parsed, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("\nCould not extract access token from login response, skipping /trips test.")
