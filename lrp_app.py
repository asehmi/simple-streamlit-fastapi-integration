import os, sys, json, base64
import time
import requests
import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------------------------------------

API_HOST='127.0.0.1'
API_PORT=5000
API_BASE_URL=f'http://{API_HOST}:{API_PORT}'

# Session State variables:
state = st.session_state
if 'API_APP' not in state:
    state.API_APP = None
if 'API_STARTED' not in state:
    state.API_STARTED=False

# --------------------------------------------------------------------------------

# NOTE: Design point... only main() is allowed to mutate state. All supporting functions should not mutate state.
def main():
    st.title('Long Running Process Manager')

    # RUN LRP
    if not state.API_STARTED:
        st.write('To launch your LRP click the button below.')
        if st.button('🚀 Launch'):

            import subprocess
            import threading

            def run(job):
                print (f"\nRunning job: {job}\n")
                proc = subprocess.Popen(job)
                proc.wait()
                return proc

            job = [f'{sys.executable}', os.path.join('.', 'lrp_bootstrapper.py'), API_HOST, str(API_PORT)]

            # server thread will remain active as long as streamlit thread is running, or is manually shutdown
            thread = threading.Thread(name='FastAPI-LRP-Bootstrapper', target=run, args=(job,), daemon=True)
            thread.start()

            time.sleep(2)

            # !! Start the LRP !!
            requests.get(f'{API_BASE_URL}/run')

            state.API_STARTED = True

            st.experimental_rerun()

    if state.API_STARTED:
        message = {}
        c1, c2, _, c4 = st.columns([1,1,1,1])
        with c1:
            if st.button('👋 Hello'):
                resp = requests.get(f'{API_BASE_URL}/hello')
                message = json.loads(resp.content)
        with c2:
            st.json(message)
        with c4:
            if st.button('🔥 Shutdown LRP'):
                requests.get(f'{API_BASE_URL}/shutdown')
                state.API_STARTED = False
                st.experimental_rerun()

        st.markdown(f'''
            #### Notes
            - `The long running process (LRP) and FastAPI is running.`
            - `To terminate the LRP, click the Shutdown button above.`
            - `To invoke the /hello endpoint, click the Hello button above.`
            #### API doc links
            `These FastAPI links only work in a localhost environment or if the FastAPI server
            is configured on an external domain reachable from this browser window!`
            - [**http://{API_HOST}:{API_PORT}/docs**](http://{API_HOST}:{API_PORT}/docs)
            - [**http://{API_HOST}:{API_PORT}/redoc**](http://{API_HOST}:{API_PORT}/redoc)
        ''')
        # st.markdown('''
        #     #### Embedded API docs
        #     `Displays but works only in localhost environment!`
        # ''')
        # st.markdown('##### Swagger UI')
        # components.iframe(f'http://{API_HOST}:{API_PORT}/docs', height=600, scrolling=True)
        # st.markdown('##### Swagger Docs')
        # components.iframe(f'http://{API_HOST}:{API_PORT}/redoc', height=600, scrolling=True)

def sidebar():
    # ABOUT
    st.sidebar.header('About')
    st.sidebar.info('FastAPI Wrapper to run and stop a long running process (LRP)!\n\n' + \
        '(c) 2023. CloudOpti Ltd. All rights reserved.')
    st.sidebar.markdown('---')


if __name__ == '__main__':
    main()
    sidebar()
