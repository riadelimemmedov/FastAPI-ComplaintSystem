#

# ?FastApi
from fastapi import FastAPI, APIRouter


# ?Custom router
from resources.routes import api_router

# ?Database properties
from db import database


# Create FastApi object from FastAPI class
app = FastAPI()
app.include_router(api_router)


#!startup
# When open localhost,work this view automatically and close database connection
@app.on_event("startup")
async def startup():
    print("Connect database successfully")
    await database.connect()


#!shutdown
# When closed port,work this view automatically and close database connection
@app.on_event("shutdown")
async def shutdown():
    print("Disconnect database successfully")
    await database.disconnect()
