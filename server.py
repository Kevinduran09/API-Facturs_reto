
import uvicorn
from app.main import app

def run(host="127.0.0.1", port=8000):

    uvicorn.run('app.main:app', host=host, port=port, reload=True)

if __name__ == '__main__':
    run()