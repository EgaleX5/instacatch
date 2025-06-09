import json
import subprocess

def load_secret():
    result = subprocess.run(
        [
            "openssl", "enc", "-aes-256-cbc", "-d",
            "-pbkdf2", "-iter", "100000",  # ✅ Important!
            "-in", ".secret.enc", "-k", "ShadowHive234892"
        ],
        capture_output=True
    )

    if result.returncode != 0:
        raise Exception("OpenSSL Error:\n" + result.stderr.decode("utf-8", errors="ignore"))

    try:
        return json.loads(result.stdout.decode("utf-8"))
    except Exception as e:
        raise Exception("Decrypted output is not valid JSON.\n" + str(e))
