import uvicorn

from fastapi import FastAPI

from pydantic import BaseSettings

class Settings(BaseSettings):
    back_token: str
    tg_token: str
    class Config:
        env_file = ".env"

settings = Settings()
 
app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7777, reload = True)