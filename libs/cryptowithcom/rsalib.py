import rsa, os
from base64 import b64encode, b64decode
 
import fileio, systemInfo

KEY_FOLDER = fileio.get_data_directory() + "/keys"
PUBLIC_KEY_FILENAME = KEY_FOLDER + "/" + systemInfo.get_hostname() + ".pub"
PRIVATE_KEY_FILENAME = KEY_FOLDER + "/" + systemInfo.get_hostname() + ".pem"

key_cache = {}
private_key_data = ""

def generate_keys():
    if not fileio.file_exists(PUBLIC_KEY_FILENAME) or not fileio.file_exists(PRIVATE_KEY_FILENAME):
        print("Generating RSA Keys")
        publicKey, privateKey = rsa.newkeys(512)

        # Write the keys to a folder
        fileio.create_folder("keys")
        fileio.write_to_file(PUBLIC_KEY_FILENAME, publicKey.save_pkcs1().decode('ascii'))
        fileio.write_to_file(PRIVATE_KEY_FILENAME, privateKey.save_pkcs1().decode('ascii'))
        
        # TODO:  Upload the public key to the website
    else:
        print("RSA Keys Already Exist")


def getPublicKey(deviceID=None):
    global key_cache
    
    if deviceID == None:
        key_file = PUBLIC_KEY_FILENAME
    else:
        # TODO:  Download the public key from website if it doesn't exist
        # OR too much time has elapsed
        key_file = KEY_FOLDER + "/" + deviceID + ".pub"

    if deviceID not in key_cache:
        data = fileio.get_file_contents_as_string(key_file)
        key_cache[deviceID] = data
    else:
        data = key_cache[deviceID]
    
    try:
        return rsa.PublicKey.load_pkcs1(data)
    except:
        raise ValueError("Invalid Public Key File")


def getPrivateKey():
    global private_key_data

    if private_key_data == "":
        private_key_data = fileio.get_file_contents_as_string(PRIVATE_KEY_FILENAME)

    try:
        return rsa.PrivateKey.load_pkcs1(private_key_data)
    except:
        raise ValueError("Invalid Private Key File")


def encrypt_public_key(plaintext, key):
    return b64encode(rsa.encrypt(plaintext.encode(), key))


def decrypt_private_key(ciphertext, key):
    return rsa.decrypt(b64decode(ciphertext), key).decode()


def sign_message(message, privateKey):
    return b64encode(rsa.sign(message.encode("utf-8"), privateKey, 'SHA-1'))


def verify_message(message, signatureAsBase64, publicKey):
    try:
<<<<<<< HEAD
        print(message.encode(), b64decode(signatureAsBase64), publicKey)
        rsa.verify(message.encode(), b64decode(signatureAsBase64), publicKey)
        return True
    except rsa.VerificationError:
        print(":(")
        return False


generate_keys()
publicKey = getPublicKey()
privateKey = getPrivateKey()

# this is the string that we will be encrypting
message = "hello geeks"

signature = sign_message(message, privateKey)
print(signature)

print("Verification:", verify_message(message, signature, publicKey))
=======
        rsa.verify(message.encode(), b64decode(signatureAsBase64), publicKey)
        return True
    except rsa.VerificationError:
        return False


# generate_keys()
# publicKey = getPublicKey()
# privateKey = getPrivateKey()
# 
# # this is the string that we will be encrypting
# message = "hello geeks"
# 
# signature = sign_message(message, privateKey)
# print(signature)
# 
# print("Verification:", verify_message(message, signature, publicKey))
>>>>>>> 040fe299933550475daa49b629bfc2eb1e9eca54


