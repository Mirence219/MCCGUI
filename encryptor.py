'''
用于加密和解密文本（密码）
'''

from cryptography.fernet import Fernet, InvalidToken
import os

#密钥存储路径
KEY_PATH = os.path.join("config","fernet_key")

#代码文件名
FILE_NAME = os.path.basename(__file__) 



def create_key() -> bytes | None:
    '''创建密钥文件并返回密钥'''
    try:
        key = Fernet.generate_key() #生成密钥
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        print(f"[DEBUG:{FILE_NAME}]已创建密钥文件")
        return key
    except Exception as e:
        print(f"[ERROR:{FILE_NAME}]生成密钥失败，报错{e}")
        return


def get_key() -> bytes | None:
    '''返回密钥（不存在则会创建）'''
    try:
        with open(KEY_PATH, "rb") as f:
            key = f.read()
        print(f"[DEBUG:{FILE_NAME}]已获取密钥")

    except FileNotFoundError:
        print(f"[DEBUG:{FILE_NAME}]密钥不存在，将生成新密钥")
        key = create_key()

    except Exception as e:
        print(f"[ERROR:{FILE_NAME}]获取密钥失败，报错{e}")
        return

    return key


#密钥
key = get_key()


def encrypt(plain_text, key = key) -> str:
    '''加密'''
    fernet = Fernet(key)
    plain_text_bytes = plain_text.encode("utf-8")
    encrypted_text_bytes = fernet.encrypt(plain_text_bytes)
    encrypted_text = encrypted_text_bytes.decode("utf-8") 
    print(f"[DEBUG:{FILE_NAME}]已加密：{encrypted_text}")
    return encrypted_text


def decrypt(encrypted_text, key = key) -> str:
    '''解密'''
    fernet = Fernet(key)
    encrypted_text_bytes = encrypted_text.encode("utf-8")
    try:
        plain_text_bytes = fernet.decrypt(encrypted_text_bytes)
    except InvalidToken:
        print(f"[WANRNING]该文本不是密文，将直接返回原内容：{encrypted_text}")
        return encrypted_text
    plain_text = plain_text_bytes.decode("utf-8")
    print(f"[DEBUG:{FILE_NAME}]已解密：{plain_text}")
    return plain_text
        





