import base64
import json
import os
import sqlite3
from shutil import copyfile

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from win32crypt import CryptUnprotectData


def get_string(LocalState):
    with open(LocalState, 'r', encoding='utf-8') as f:
        s = json.load(f)['os_crypt']['encrypted_key']
    return s


def pull_the_key(base64_encrypted_key):
    encrypted_key_with_header = base64.b64decode(base64_encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key


def DecryptString(key, data):
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)
    plaintext = plainbytes.decode('utf-8')
    return plaintext


def get_local_cookie(cookie_url):
    UserDataDir = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data'
    LocalStateFilePath = UserDataDir + r'\Local State'
    CookiesFilePath = UserDataDir + r'\Default\Cookies'
    if not os.path.exists('./Local'):
        os.mkdir('./Local')
    copyfile(CookiesFilePath, './Local/Cookies')

    con = sqlite3.connect('./Local/Cookies')

    # con.text_factory = bytes
    res = con.execute('select host_key,name,encrypted_value from cookies').fetchall()
    con.close()

    u17k_cookies = []
    key = pull_the_key(get_string(LocalStateFilePath))
    for i in res:
        cookie_value = DecryptString(key, i[2])
        if i[0] == cookie_url:
            if i[1] == 'ptag':
                continue
            u17k_cookies.append(i[1] + "=" + cookie_value)
    cookie = '; '.join(u17k_cookies)
    return cookie


if __name__ == '__main__':
    print(get_local_cookie('.v.qq.com')+'; '+get_local_cookie('.qq.com'))
