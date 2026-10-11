###Hey baby 🍼 If you leak this file under your own name and claim the credit, I'll fuck you with salt. 🥱


import os
import time
import json
import base64

import httpx
from flask import Flask, request, jsonify
from flask_cors import CORS
from Crypto.Cipher import AES

from google.protobuf import json_format
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.protobuf.message import Message


# ============================================================
#  PART 1 — FreeFire_pb2 (inlined)
# ============================================================

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 6, 30, 0, "", "FreeFire.proto",
)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x46reeFire.proto"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t'
    b'\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d '
    b'\x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t"]\n\x10\x42lacklist'
    b'InfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason\x12\x17\n'
    b'\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 '
    b'\x01(\r"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08\x12'
    b'\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18'
    b'\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08"\xa0\x03\n\x08'
    b'LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region'
    b'\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_'
    b'region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t'
    b'\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_'
    b'regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl'
    b'\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mul'
    b'ator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.'
    b'BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueue'
    b'Info\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18'
    b'\x0f \x01(\r\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city'
    b'\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n'
    b'\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17'
    b'\x42\x41N_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11\x42\x41N_REASON_'
    b'REFUND\x10\x02\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03\x12\x16\n'
    b'\x12\x42\x41N_REASON_SKINMOD\x10\x04\x12 \n\x1b\x42\x41N_REASON_IN_GAME'
    b'_AUTO_NEW\x10\xf6\x07\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "FreeFire_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_BANREASON"]._serialized_start = 738
    _globals["_BANREASON"]._serialized_end = 906
    _globals["_LOGINREQ"]._serialized_start = 18
    _globals["_LOGINREQ"]._serialized_end = 117
    _globals["_BLACKLISTINFORES"]._serialized_start = 119
    _globals["_BLACKLISTINFORES"]._serialized_end = 212
    _globals["_LOGINQUEUEINFO"]._serialized_start = 214
    _globals["_LOGINQUEUEINFO"]._serialized_end = 316
    _globals["_LOGINRES"]._serialized_start = 319
    _globals["_LOGINRES"]._serialized_end = 735

LoginReq = _globals["LoginReq"]
LoginRes = _globals["LoginRes"]


# ============================================================
#  PART 2 — Settings
# ============================================================

MAIN_KEY = base64.b64decode("WWcmdGMlREV1aDYlWmNeOA==")
MAIN_IV = base64.b64decode("Nm95WkRyMjJFM3ljaGpNJQ==")
API_KEY = os.getenv("API_KEY", "")  # agar set hai to ?key=... zaroori hoga
RELEASEVERSION = "OB55"
USERAGENT = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"
LOGIN_URL = "https://loginbp.ppmainecoonghj.com/"

# Fast HTTP client (connection pooling + keep-alive)
HTTP_LIMITS = httpx.Limits(max_keepalive_connections=20, max_connections=50)
HTTP_TIMEOUT = httpx.Timeout(15.0, connect=5.0)
_http_client = httpx.Client(limits=HTTP_LIMITS, timeout=HTTP_TIMEOUT)


# ============================================================
#  PART 3 — Flask App
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
#  PART 4 — Helpers
# ============================================================

class AuthError(Exception):
    """UID/password galat hai."""

class UpstreamError(Exception):
    """Garena server ne sahi response nahi diya (timeout, rate limit, parse error)."""

class QueueError(Exception):
    """Garena login queue (temporary) - dobara try karne par chal sakta hai."""

class AccountError(Exception):
    """Account banned/blacklisted ya login queue me hai."""


def pad(text: bytes) -> bytes:
    padding_length = AES.block_size - (len(text) % AES.block_size)
    return text + bytes([padding_length] * padding_length)


def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(plaintext))


def json_to_proto(json_data: str, proto_message: Message) -> bytes:
    json_format.ParseDict(json.loads(json_data), proto_message)
    return proto_message.SerializeToString()


def try_parse_login_res(data: bytes):
    try:
        msg = LoginRes()
        msg.ParseFromString(data)
        if msg.account_id and msg.account_id > 0:
            return json.loads(json_format.MessageToJson(msg))
    except Exception:
        pass
    return None


def extract_login_res(raw: bytes) -> dict:
    candidates = []

    # Attempt 1: from index 0
    parsed = try_parse_login_res(raw)
    if parsed:
        if parsed.get("token"):
            return parsed
        candidates.append(parsed)

    # Attempt 2: scan each \x08
    idx = 0
    while True:
        idx = raw.find(b"\x08", idx)
        if idx == -1:
            break
        parsed = try_parse_login_res(raw[idx:])
        if parsed:
            if parsed.get("token"):
                return parsed
            candidates.append(parsed)
        idx += 1

    # Attempt 3: JWT marker prefix
    jwt_marker = raw.find(b"eyJhbGciOiJIUzI1NiIs")
    if jwt_marker != -1:
        for i in range(jwt_marker - 1, max(jwt_marker - 300, -1), -1):
            if raw[i] == 0x42:
                parsed = try_parse_login_res(raw[i:])
                if parsed:
                    if parsed.get("token"):
                        return parsed
                    candidates.append(parsed)
                break

    if candidates:
        # token wala nahi mila; sabse zyada fields wala parse wapas do (debug ke liye)
        return max(candidates, key=lambda m: len(m))

    raise Exception(f"Could not parse LoginRes. Raw: {raw[:200]}")


def get_access_token(account: str):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    payload = (
        account
        + "&response_type=token&client_type=2"
        + "&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
        + "&client_id=100067"
    )
    headers = {
        "User-Agent": USERAGENT,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    last_err = None
    for attempt in range(3):
        try:
            resp = _http_client.post(url, data=payload, headers=headers)
            data = resp.json()
            if isinstance(data, dict):
                return data.get("access_token", "0"), data.get("open_id", "0")
            last_err = "unexpected response from Garena"
        except (httpx.HTTPError, ValueError) as e:  # timeout / network / non-JSON
            last_err = str(e)
        time.sleep(1.5 * (attempt + 1))
    raise UpstreamError(f"Garena access-token server error: {last_err}")


def generate_jwt_token(uid: str, password: str):
    start_time = time.time()

    token_val, open_id = get_access_token(f"uid={uid}&password={password}")
    if token_val == "0" or open_id == "0":
        raise AuthError("Invalid UID or Password — access token not received")

    body = json.dumps({
        "open_id": open_id,
        "open_id_type": "4",
        "login_token": token_val,
        "orign_platform_type": "4",
    })
    proto_bytes = json_to_proto(body, LoginReq())
    payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)

    headers = {
        "User-Agent": USERAGENT,
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "X-Ga-Sv": "1789534056",
        "Authorization": "Bearer",
        "X-Ga": "v1 1",
        "Releaseversion": RELEASEVERSION,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.12f1",
        "PlAy_VeR": "1.132.1",
        "Ob_VeR": RELEASEVERSION,
    }

    try:
        resp = _http_client.post(f"{LOGIN_URL}MajorLogin", data=payload, headers=headers)
        msg = extract_login_res(resp.content)
    except httpx.HTTPError as e:
        raise UpstreamError(f"MajorLogin request failed: {e}")
    except Exception as e:
        raise UpstreamError(f"MajorLogin response parse failed (status {getattr(resp, 'status_code', '?')}): {str(e)[:150]}")

    jwt_token = msg.get("token", "")
    if not jwt_token:
        bl = msg.get("blacklist") or {}
        q = msg.get("queueInfo") or {}
        if bl:
            raise AccountError(f"Account blacklisted/banned: {bl.get('banReason', 'UNKNOWN')}")
        if q:
            raise QueueError(f"Login queue active, try later [queueInfo={json.dumps(q, default=str)[:120]}]")
        fields = ",".join(sorted(k for k, v in msg.items() if v not in ("", 0, None, [], {})))
        extra = ""
        if msg.get("recommendRegions") or msg.get("newActiveRegion"):
            extra = " (account ka region set nahi hai / region select karna baaki hai)"
        raw_dbg = ""
        if os.getenv("DEBUG_RAW"):
            raw_dbg = f" raw_len={len(resp.content)} raw_hex={resp.content[:160].hex()}"
        raise AccountError(
            f"Login OK but server returned empty token{extra} [http={resp.status_code} fields={fields}{raw_dbg}]"
        )

    region = (msg.get("lockRegion") or msg.get("notiRegion") or "").upper() or None
    elapsed = time.time() - start_time

    return {
        "access_token": token_val,
        "open_id": open_id,
        "real_uid": str(msg.get("accountId", "")),
        "region": region,
        "status": "success",
        "time": f"{elapsed:.2f}s",
        "token": jwt_token,
    }


# ============================================================
#  PART 5 — Routes
# ============================================================

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "endpoint": "/token?uid=UID&password=PASS",
        "example": "/token?uid=18097039025&password=yourpass",
    }), 200


@app.route("/token", methods=["GET"])
def get_jwt_token():
    if API_KEY and request.args.get("key") != API_KEY:
        return jsonify({"status": "error", "error": "Invalid API key"}), 401

    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify({
            "status": "error",
            "error": "Both uid and password parameters are required"
        }), 400

    try:
        return jsonify(generate_jwt_token(uid, password)), 200
    except AuthError as e:
        return jsonify({"status": "error", "error": str(e)}), 401
    except AccountError as e:
        return jsonify({"status": "error", "error": str(e)}), 403
    except QueueError as e:
        return jsonify({"status": "error", "error": str(e)}), 503
    except UpstreamError as e:
        return jsonify({"status": "error", "error": str(e)}), 502
    except Exception as e:
        return jsonify({"status": "error", "error": f"Failed to generate token: {str(e)}"}), 500


# ============================================================
#  ENTRY POINT
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
    
    
### Hey baby 🍼 If you leak this file under your own name and claim the credit, I'll fuck you with salt. 🥱
