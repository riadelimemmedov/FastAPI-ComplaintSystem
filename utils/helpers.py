#

# ?FastApi
# ?Python modules and function
import base64

from fastapi import Depends, FastAPI, HTTPException, Request, status


#!decode_photo
def decode_photo(path, encoded_string):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_string.encode("utf-8")))
        except HTTPException as ex:
            raise HTTPException(400, "Invalid photo encoding")
