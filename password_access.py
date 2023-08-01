import password_processing
import pathlib
import base64
import hashlib
from fernet import Fernet

userpath = pathlib.Path(__name__).parent.resolve()


def gen_fernet_key(passcode: bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))


def save_password(_name, _webpage, _username, _password):
    password = password_processing.Password()
    setattr(password, "webpage", _webpage)
    setattr(password, "password_loc", f"{userpath}/passwords/{_name}.passfile")
    setattr(password, "username", _username)
    setattr(password, "password", _password)

    f = Fernet(gen_fernet_key(password_processing.user_details.encode("utf-8")))
    with open(getattr(password, "password_loc"), "+ab") as file:
        file.write(f.encrypt(bytes(_username, 'utf-8')))
        file.write(b"\n")
        file.write(f.encrypt(bytes(_password, 'utf-8')))
        file.close()
    with open(f"{userpath}/passwords/{_name}.data", "w") as file:
        file.write(_webpage)

    password_processing.passwords.append(password)


def read_password(_name):
    fernet = Fernet(gen_fernet_key(password_processing.user_details.encode("utf-8")))

    with open(f"{userpath}/passwords/{_name}.data", "r") as f:
        website = f.readline()
        f.close()

    with open(f"{userpath}/passwords/{_name}.passfile", "r") as file:
        data = file.readlines()
        file.close()

    username = (fernet.decrypt(data[0].strip("\n").encode())).decode()
    password = (fernet.decrypt(data[1].encode())).decode()

    return {
        "name": _name,
        "website": website,
        "username": username,
        "password": password
    }
