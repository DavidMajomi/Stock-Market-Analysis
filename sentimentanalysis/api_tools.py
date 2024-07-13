import os

def write_api_key_to_file(key, file):
    f = open(file, "w")
    f.write(key)
    f.close()


def read_api_key_from_file(path_to_file : str) -> str:
    if os.path.exists(path_to_file):
        with open(path_to_file, "r") as file:
            api_key = file.readline()
    else:
        raise Exception("File with api key does not exist")
    
    return api_key 