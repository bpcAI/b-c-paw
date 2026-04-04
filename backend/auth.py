import hmac, hashlib, sqlite3, secrets, datetime

SECRET_KEY = b"super_secret_key"

def validate_serial(serial: str):
    uid = serial[:3]
    date = serial[3:9]
    sig = serial[9:]

    # 驗證 HMAC
    msg = uid + date
    expected_sig = hmac.new(SECRET_KEY, msg.encode(), hashlib.sha256).hexdigest()[:6]
    if sig != expected_sig:
        return None

    # SQLite 驗證
    conn = sqlite3.connect("licenses.db")
    cur = conn.cursor()
    cur.execute("SELECT status, expiry FROM licenses WHERE uid=?", (uid,))
    row = cur.fetchone()
    if not row or row[0] != "active":
        return None
    if datetime.date.today() > datetime.datetime.strptime(row[1], "%Y-%m-%d").date():
        return None

    return secrets.token_hex(16)

