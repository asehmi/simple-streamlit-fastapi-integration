"""
Simple bootstrapper intended to be used used to start the API as a daemon process
"""
import sys
import uvicorn

from lrp_fastapi_wrapper import FastAPI_Wrapper

def stand_up(host='127.0.0.1', port=8000):
    app = FastAPI_Wrapper()
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    stand_up(host=sys.argv[1], port=int(sys.argv[2]))
