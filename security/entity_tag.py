import hashlib
from icecream import ic

def generate_entity_tag(data:str):
    etag=hashlib.sha256(data.encode()).hexdigest()

    ic(etag)
    return etag