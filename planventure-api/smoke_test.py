import urllib.request, json, time, uuid

BASE = 'http://127.0.0.1:5000'


def req(path, method='GET', data=None, headers=None):
    if headers is None:
        headers = {}
    url = BASE + path
    data_bytes = None
    if data is not None:
        data_bytes = json.dumps(data).encode()
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data_bytes, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode()
            try:
                parsed = json.loads(body)
            except Exception:
                parsed = body
            return resp.getcode(), parsed
    except Exception as e:
        return None, str(e)


def main():
    # wait for server
    for i in range(15):
        code, body = req('/health')
        if code == 200:
            print('Health OK')
            break
        print('Waiting for server...')
        time.sleep(1)
    else:
        print('Server did not respond. Aborting.')
        return

    username = 'smoketest_' + uuid.uuid4().hex[:6]
    email = username + '@example.com'
    password = 'StrongPass1!'

    code, body = req('/auth/register', 'POST', {'username': username, 'email': email, 'password': password})
    print('register:', code, body)

    # If user already exists from seeding, continue to login
    code, body = req('/auth/login', 'POST', {'username': username, 'password': password})
    if code != 200:
        # try seeded user
        print('user not created during register; trying seeded user login...')
        # pick a known seeded user
        code, body = req('/auth/login', 'POST', {'username': 'alice', 'password': 'Password123!'})

    print('login:', code, body)
    if code != 200:
        print('Login failed, aborting.')
        return

    token = body.get('access_token') if isinstance(body, dict) else None
    if not token:
        print('No token returned, aborting.')
        return

    headers = {'Authorization': f'Bearer {token}'}
    code, body = req('/trips', 'GET', None, headers)
    print('trips GET:', code, body)


if __name__ == '__main__':
    main()
