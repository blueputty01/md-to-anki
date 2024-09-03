import hashlib

def hash_file(path):
    BUFF_SIZE = 65536  # read in 64kb chunks

    sha1 = hashlib.sha1()
    with open(path, "rb") as f:
        while True:
            data = f.read(BUFF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()