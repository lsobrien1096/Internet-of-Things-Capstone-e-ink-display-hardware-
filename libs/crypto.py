from cryptography.fernet import Fernet  
import rsa
from Crypto.Random import get_random_bytes
#import fileio, systemInfo


# Fernet Variables
key = bytes("CsVt3jfXyZ5UXY88q6xgEn7SjieU1AOEsq_rDpMYtLY=", 'utf-8')
fernet_salt = b'\xbd\xc0,\x16\x87\xd7G\xb5\xe5\xcc\xdb\xf9\x07\xaf\xa0\xfa'
f = Fernet(key)

#KEY_FOLDER_NAME = fileio.get_data_directory() + "/fernetkey"


# RSA Variables
#publicKey, privateKey = rsa.newkeys(512)
#publicKey = [7255956301400914559993456773373614924514929412497587459907943968883315628925975229822396235982110692044560428101011991526824823351348720640578527046777479, 65537]

#how do I store these keys
# gives me stupid attribute error: AttributeError: 'tuple' object has no attribute 'n'
def encrypt_test(payload):
    return "ENCRYPTED" + payload


def decrypt_test(payload):
    payload = payload.replace("ENCRYPTED", "")
    return payload


def encrypt_fernet(payload):
    print("fernet starting")
    payload = f._encrypt_from_parts(bytes(payload, 'utf-8'), 0, fernet_salt)
    print("fernet done")
    return bytes.decode(payload)


def decrypt_fernet(payload):
    arr = bytes(payload, 'utf-8')
    payload = f.decrypt(arr)
    return bytes.decode(payload)


