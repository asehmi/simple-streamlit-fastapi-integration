# Simple Streamlit + FastAPI Integration
A minimal Streamlit app showing how to launch and stop a FastAPI process on demand. The FastAPI `/run` route simulates a long-running process which is launched on a separate thread. 

Ensure the required packages are installed:

```bash
pip install -r requirements.txt
```

To run the app:

```bash
streamlit run lrp_app.py
```

## Demo
![demo](./fastapi_wrapper_simple_demo.gif)