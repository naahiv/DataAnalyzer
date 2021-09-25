from enc_key import KEY
from cryptography.fernet import Fernet

def get_key_and_token():
    fernet = Fernet(KEY)
    f = open('td_auth.txt', 'r')
    lines = f.readlines()
    api_key = lines[0].strip()
    enc_oauth = lines[1].strip()
    oauth_token = fernet.decrypt(enc_oauth.encode()).decode()
    f.close()
    return api_key, oauth_token
