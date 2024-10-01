import os
class Config(object):
    SECRET_KEY=os.environ.get("mongodb://localhost:27017/retail_banking") or b'\x1d\xe6\xf23=\xebr\x9a\xf17\xb8<4\x08\x9cf'
    MONGODB_SETTINGS = { 'db' : 'retail_banking'}
