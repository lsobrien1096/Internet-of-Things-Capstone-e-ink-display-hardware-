import rsa, os, requests, json
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
        password = input("Enter Password: ")
        
        publicKey, privateKey = rsa.newkeys(512)

        # Write the keys to a folder
        fileio.create_folder("keys")
        fileio.write_to_file(PUBLIC_KEY_FILENAME, publicKey.save_pkcs1().decode('ascii'))
        fileio.write_to_file(PRIVATE_KEY_FILENAME, privateKey.save_pkcs1().decode('ascii'))
        
        # TODO:  Upload the public key to the website
        # use the password
        d = {
            "pi_id": systemInfo.get_hostname(),
            "public_key": publicKey.save_pkcs1().decode('ascii')
            }
        r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data={'api_key' : '12345', 'api_function' : 'upload_rsa', 'data' : json.dumps(d)})

        print(r.text)
    else:
        print("RSA Keys Already Exist")


def getPublicKey(deviceID=None):
    global key_cache
    
    print("Getting public Key For", deviceID)
    
    if deviceID == None:
        key_file = PUBLIC_KEY_FILENAME
    else:
        # TODO:  Download the public key from website if it doesn't exist
        # OR too much time has elapsed
        key_file = KEY_FOLDER + "/" + deviceID + ".pub"
        
        if not fileio.file_exists(key_file):
            r = requests.post('https://iot.dfcs-cloud.net/api_v1.php', data= {'api_key' : '12345','api_function' : 'get_rsa', 'pi_id': deviceID})
            key = json.loads(r.text)
            print("REQUESTING KEY:", r.text)
            fileio.write_to_file(key_file, key['public_key'])
        
    if deviceID not in key_cache:
        data = fileio.get_file_contents_as_string(key_file)
        key_cache[deviceID] = data
    else:
        data = key_cache[deviceID]
    
    try:
        print("returning key:", data)
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
    signatureAsBase64 = b64encode(rsa.sign(message.encode("utf-8"), privateKey, 'SHA-1'))
    signatureAsString = str(signatureAsBase64)[2:-1]
    return signatureAsString


def verify_message(message, signatureAsString, publicKey):
    try:
        print("\n*** ATTEMPTING TO VERIFY MESSAGE ***")
        
        # Converts the String Signature Into a Base64 Object (Whew!)
        signatureAsBase64 = b64decode(b64encode(bytes(signatureAsString, "utf-8")))
        
        # Verifies that the signature was created by the private key
        x = rsa.verify(message.encode(), b64decode(signatureAsBase64), publicKey)
        
        # If we make it here, everything worked!
        return True
    
    except:
        return False
    
    return False


generate_keys()
publicKey = getPublicKey()
privateKey = getPrivateKey()

if __name__ == '__main__':
    # this is the string that we will be encrypting
    message = "{}"
    signature = sign_message(message, privateKey)    
    print("Verification:", verify_message(message, signature, publicKey))


