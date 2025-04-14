import os
import sqlite3
from wsgidav.server.run_server import run

DATABASE = 'PyMediaServer.db'
BASE_PATH = "/NAS/MediaNet"

def get_users():
    users = {}
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("SELECT username, password FROM users")
    for username, password in cursor.fetchall():
        users[username] = password
    conn.close()
    return users

def start_dav_server(port=7077):
    user_data = get_users()
    provider_mapping = {}

    for user in user_data:
        user_dir = os.path.join(BASE_PATH, user)
        os.makedirs(user_dir, exist_ok=True)
        provider_mapping[f"/{user}"] = user_dir

    config = {
        "host": "0.0.0.0",
        "port": port,
        "provider_mapping": provider_mapping,
        "simple_dc": {
            "user_mapping": {
                "*": user_data
            }
        },
        "accept_basic_auth": True,
        "accept_digest_auth": False,
        "verbose": 1,
        "logging": {
            "enable_loggers": [],
        },
    }

    print(f"✅ WebDAV running at http://localhost:{port}")
    run(config)
