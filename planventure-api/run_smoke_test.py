#!/usr/bin/env python
"""
Full smoke test runner that starts the server and tests it.
"""
import subprocess
import time
import json
import urllib.request
import urllib.error
import sys
import os

BASE_URL = 'http://127.0.0.1:5000'
VENV_PYTHON = 'C:/Users/HP/OneDrive/Documents/GitHub/planventure/.venv/Scripts/python.exe'
APP_PATH = 'C:/Users/HP/OneDrive/Documents/GitHub/planventure/planventure-api/app.py'

def make_request(endpoint, method='GET', data=None, token=None):
    """Make an HTTP request and return status, response."""
    url = BASE_URL + endpoint
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
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

# Start server
print("Starting Flask server...")
server_proc = subprocess.Popen([VENV_PYTHON, APP_PATH], cwd='C:/Users/HP/OneDrive/Documents/GitHub/planventure/planventure-api')

# Wait for server to be ready
print("Waiting for server to start...")
for i in range(10):
    try:
        status, _ = make_request('/health')
        if status == 200:
            print("✓ Server is ready!\n")
            break
    except:
        pass
    time.sleep(1)
else:
    print("✗ Server failed to start")
    server_proc.kill()
    sys.exit(1)

try:
    # Test 1: Health check
    print("=" * 60)
    print("TEST 1: GET /health")
    print("=" * 60)
    status, response = make_request('/health')
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}\n")

    # Test 2: Register a new user
    print("=" * 60)
    print("TEST 2: POST /auth/register (new user)")
    print("=" * 60)
    user_data = {
        'username': 'testuser789',
        'email': 'test789@example.com',
        'password': 'StrongPass1!'
    }
    print(f"Request: {json.dumps(user_data, indent=2)}")
    status, response = make_request('/auth/register', 'POST', user_data)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}\n")

    # Test 3: Login
    print("=" * 60)
    print("TEST 3: POST /auth/login")
    print("=" * 60)
    login_data = {
        'username': 'testuser789',
        'password': 'StrongPass1!'
    }
    print(f"Request: {json.dumps(login_data, indent=2)}")
    status, response = make_request('/auth/login', 'POST', login_data)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")

    access_token = None
    if status == 200 and isinstance(response, dict):
        access_token = response.get('access_token')
        print(f"\n✓ Access Token Received: {access_token[:30]}...\n")

    if access_token:
        # Test 4: Get profile
        print("=" * 60)
        print("TEST 4: GET /profile (with auth)")
        print("=" * 60)
        status, response = make_request('/profile', 'GET', token=access_token)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}\n")

        # Test 5: Get trips
        print("=" * 60)
        print("TEST 5: GET /trips (with auth)")
        print("=" * 60)
        status, response = make_request('/trips', 'GET', token=access_token)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}\n")

        # Test 6: Create a trip
        print("=" * 60)
        print("TEST 6: POST /trips (create new trip)")
        print("=" * 60)
        trip_data = {
            'title': 'Weekend Getaway',
            'destination': 'Mountain Retreat',
            'description': 'A relaxing weekend trip'
        }
        print(f"Request: {json.dumps(trip_data, indent=2)}")
        status, response = make_request('/trips', 'POST', trip_data, access_token)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}\n")

        if status == 201 and isinstance(response, dict) and 'trip' in response:
            trip_id = response['trip'].get('id')
            print(f"✓ Trip Created with ID: {trip_id}\n")

            # Test 7: Add itinerary to trip
            if trip_id:
                print("=" * 60)
                print(f"TEST 7: POST /trips/{trip_id}/itinerary (add activity)")
                print("=" * 60)
                itinerary_data = {
                    'day': 1,
                    'title': 'Morning Hike',
                    'description': 'Scenic mountain hike',
                    'location': 'Trail Head'
                }
                print(f"Request: {json.dumps(itinerary_data, indent=2)}")
                status, response = make_request(f'/trips/{trip_id}/itinerary', 'POST', itinerary_data, access_token)
                print(f"Status: {status}")
                print(f"Response: {json.dumps(response, indent=2)}\n")

finally:
    # Stop server
    print("=" * 60)
    print("Shutting down server...")
    server_proc.terminate()
    server_proc.wait(timeout=5)
    print("✓ Server stopped")
