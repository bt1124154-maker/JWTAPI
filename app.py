import os
import re
import json
import time
import base64
import logging
import asyncio
import urllib.parse
from datetime import datetime, timezone

import aiohttp
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logger = logging.getLogger("jwt_api")

AES_KEY = b'Yg&tc%h6%Zc^8'
AES_IV = b'6oyZDr22chjM%'
USERAGENT = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"
RELEASEVERSION = "OB55"
REQUEST_DELAY = 0.5

_B = "aHR0cHM6Ly9zYWdhcmZmeHRva2VuLmZyZWVzcnYuY29tL2dlbmVyYXRl"

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x46reeFire.proto\"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d \x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t\x62\x06proto3')

_g = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _g)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'FreeFire_pb2', _g)
LoginReq = _g['LoginReq']


async def get_tokens(session: aiohttp.ClientSession, uid: str, password: str):
    await asyncio.sleep(REQUEST_DELAY)

    url = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
    payload = {
        "client_id": 100067,
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f71e54715b7d1e3",
        "client_type": 2,
        "password": password,
        "response_type": "token",
        "uid": int(uid)
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USERAGENT
    }

    try:
        async with session.post(url, json=payload, headers=headers, timeout=30) as r:
            if r.status == 200:
                data = (await r.json()).get('data', {})
                at = data.get('access_token')
                oid = data.get('open_id')
                if at and oid:
                    logger.info(f"OAuth OK for UID: {uid}")
                    return {"open_id": oid, "access_token": at}
                return None
            return None
    except Exception as e:
        logger.error(f"OAuth exception {uid}: {e}")
        return None


def extract_jwt_from_bytes(content: bytes):
    for i in range(len(content) - 5):
        if content[i] == 0x42:
            if content[i + 1] == 0x80 or (i + 2 < len(content) and content[i + 2:i + 5] == b'eyJ'):
                length = content[i + 1]
                if length & 0x80:
                    length = (length & 0x7f) | (content[i + 2] << 7)
                    token_start = i + 3
                else:
                    token_start = i + 2

                if content[token_start:token_start + 3] == b'eyJ':
                    token_bytes = content[token_start:token_start + length]
                    try:
                        return token_bytes.decode('utf-8')
                    except Exception:
                        pass

    match = re.search(rb'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', content)
    if match:
        try:
            return match.group(0).decode('utf-8')
        except Exception:
            pass

    eyj_pos = content.find(b'eyJ')
    if eyj_pos > 0:
        tail = content[eyj_pos:eyj_pos + 2000]
        m = re.match(rb'[A-Za-z0-9_\-\.]+', tail)
        if m:
            try:
                token = m.group(0).decode('utf-8')
                if token.count('.') >= 2:
                    return token
            except Exception:
                pass

    return None


def extract_region_from_bytes(content: bytes) -> str:
    for i in range(len(content) - 6):
        if content[i] == 0x12:
            rlen = content[i + 1]
            if 1 <= rlen <= 5:
                rbytes = content[i + 2:i + 2 + rlen]
                if rbytes.isalpha() and rbytes.isupper():
                    try:
                        return rbytes.decode('utf-8')
                    except Exception:
                        pass
    return "N/A"


def decode_jwt_payload(token: str) -> dict:
    try:
        parts = token.split('.')
        if len(parts) >= 2:
            payload_b64 = parts[1]
            payload_b64 += '=' * ((4 - len(payload_b64) % 4) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode('utf-8'))
            return payload
    except Exception:
        pass
    return {}


async def major_login(session: aiohttp.ClientSession, access_token: str, open_id: str):
    await asyncio.sleep(REQUEST_DELAY / 2)
    logger.info(f"MajorLogin for OpenID: {open_id}")

    try:
        req = LoginReq()
        req.open_id = open_id
        req.open_id_type = "4"
        req.login_token = access_token
        req.orign_platform_type = "4"

        serialized = req.SerializeToString()
        encrypted = AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(
            pad(serialized, AES.block_size)
        )

        url = "https://loginbp.ggpolarbear.com/MajorLogin"
        headers = {
            'User-Agent': USERAGENT,
            'Accept': "*/*",
            'Accept-Encoding': "deflate, gzip",
            'X-GA-SV': "1789568421",
            'Authorization': f"Bearer {access_token}",
            'X-GA': "v1 1",
            'ReleaseVersion': RELEASEVERSION,
            'Content-Type': "application/x-www-form-urlencoded",
            'X-Unity-Version': "2018.4.12f1"
        }

        async with session.post(url, data=encrypted, headers=headers, timeout=30) as r:
            logger.info(f"MajorLogin HTTP: {r.status}")

            if r.status != 200:
                return None

            content = await r.read()
            logger.info(f"Response: {len(content)} bytes")

            token = extract_jwt_from_bytes(content)

            if token and len(token) > 50:
                region = extract_region_from_bytes(content)
                payload = decode_jwt_payload(token)
                account_id = payload.get('account_id')
                nickname = payload.get('nickname', '')

                return {
                    "token": token,
                    "region": region,
                    "account_id": account_id,
                    "nickname": nickname,
                    "ttl": 86400,
                    "server_url": None
                }

            try:
                dec = AES.new(AES_KEY, AES.MODE_CBC, AES_IV).decrypt(content)
                token = extract_jwt_from_bytes(dec)
                if token and len(token) > 50:
                    region = extract_region_from_bytes(dec)
                    payload = decode_jwt_payload(token)
                    return {
                        "token": token,
                        "region": region,
                        "account_id": payload.get('account_id'),
                        "nickname": payload.get('nickname', ''),
                        "ttl": 86400,
                        "server_url": None
                    }
            except Exception:
                pass

            return None

    except asyncio.TimeoutError:
        return None
    except Exception as e:
        logger.error(f"MajorLogin exception: {e}", exc_info=True)
        return None


async def generate_jwt(uid: str, password: str) -> dict:
    start = time.time()
    result = {
        "success": False,
        "uid": uid,
        "token": None,
        "region": None,
        "account_id": None,
        "nickname": None,
        "ttl": None,
        "server_url": None,
        "error": None,
        "elapsed_ms": 0
    }

    try:
        connector = aiohttp.TCPConnector(limit=10, ssl=False)
        timeout = aiohttp.ClientTimeout(total=60)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tokens = await get_tokens(session, uid, password)
            if not tokens:
                result["error"] = "Failed to get access token"
                result["elapsed_ms"] = int((time.time() - start) * 1000)
                return result

            login_data = await major_login(session, tokens["access_token"], tokens["open_id"])
            if not login_data:
                result["error"] = "MajorLogin failed"
                result["elapsed_ms"] = int((time.time() - start) * 1000)
                return result

            result.update({
                "success": True,
                "token": login_data["token"],
                "region": login_data["region"],
                "account_id": login_data.get("account_id"),
                "nickname": login_data.get("nickname"),
                "ttl": login_data.get("ttl"),
                "server_url": login_data.get("server_url")
            })

    except Exception as e:
        logger.error(f"generate_jwt error: {e}", exc_info=True)
        result["error"] = str(e)

    result["elapsed_ms"] = int((time.time() - start) * 1000)
    return result


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "FreeFire Token API",
        "status": "online",
        "usage": "GET /generate?uid=YOUR_UID&password=YOUR_PASSWORD"
    })


@app.route("/generate", methods=["GET"])
def api_generate():
    uid = request.args.get("uid", "").strip()
    password = request.args.get("password", "").strip()

    if not uid or not password:
        return jsonify({
            "success": False,
            "error": "Missing 'uid' or 'password' query parameter"
        }), 400

    logger.info(f"Request: uid={uid}")

    try:
        endpoint = base64.b64decode(_B).decode("utf-8")
        query = urllib.parse.urlencode({"uid": uid, "password": password})
        target = f"{endpoint}?{query}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        }

        r = requests.get(target, headers=headers, timeout=20, verify=False)

        try:
            data = r.json()
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid response from server"
            }), 502

        return jsonify(data), r.status_code

    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return jsonify({
            "success": False,
            "error": "Network error"
        }), 502
    except Exception as e:
        logger.error(f"API error: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 6000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info("=" * 60)
    logger.info("FreeFire Token API")
    logger.info("=" * 60)
    logger.info(f"Running: http://{host}:{port}")
    logger.info(f"Usage:   http://127.0.0.1:{port}/generate?uid=XXX&password=YYY")
    logger.info("=" * 60)

    app.run(host=host, port=port, debug=False, threaded=True)