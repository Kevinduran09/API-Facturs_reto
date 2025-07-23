
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

url_factus = os.getenv("URL_FACTUS")
email_factus = os.getenv("EMAIL_FACTUS")
password_factus = os.getenv("PASSWORD_FACTUS")
client_id = os.getenv("CLIENT_ID_FACTUS")
client_secret = os.getenv("CLIENT_SECRET_FACTUS")
grant_type = os.getenv("GRANT_TYPE_FACTUS")

async def get_token_From_factus():
    async with httpx.AsyncClient() as client:
        respuesta = await client.post(f"{url_factus}/oauth/token",
                                      data={
                                          "grant_type": grant_type,
                                          "client_id": client_id,
                                          "client_secret": client_secret,
                                          "username": email_factus,
                                          "password": password_factus
                                      })
        return respuesta.json()


async def auth_factus_middleware():
    response = await get_token_From_factus()
    return response


