import os, sys, json
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
        if st.button('\U0001F680 Launch'):

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
        c1, _, c3 = st.columns([1,1,8])
        with c1:
            if st.button('👋 Hello'):
                resp = requests.get(f'{API_BASE_URL}/hello')
                st.json(json.loads(resp.content))
        with c3:
            if st.button('🔥 Shutdown LRP'):
                requests.get(f'{API_BASE_URL}/shutdown')
                state.API_STARTED = False
                st.experimental_rerun()

        st.markdown(f'''
            The LRP API is running. If you\'d like to terminate the LRP click the Shutdown button above.
            ### Links to API docs (works in localhost environment only!)
            - [**http://{API_HOST}:{API_PORT}/docs**](http://{API_HOST}:{API_PORT}/docs)
            - [**http://{API_HOST}:{API_PORT}/redoc**](http://{API_HOST}:{API_PORT}/redoc)
        ''')
        # st.markdown('### Embedded API docs (works in localhost environment only!)')
        # components.iframe(f'http://{API_HOST}:{API_PORT}/docs', height=600, scrolling=True)
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
