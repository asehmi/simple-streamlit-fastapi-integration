"""
Simple bootstrapper intended to be used used to start the API as a daemon process
"""
import sys
import uvicorn

from lrp_fastapi_wrapper import FastAPI_Wrapper

API_HOST='localhost'
API_PORT=5000

def stand_up(host=API_HOST, port=API_PORT):
    app = FastAPI_Wrapper()
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    stand_up(host=sys.argv[1], port=int(sys.argv[2]))
