import os, sys
import time
import streamlit as st
import requests

# --------------------------------------------------------------------------------

API_HOST='localhost'
API_PORT=8000
API_BASE_URL='http://localhost:8000'

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
        st.markdown(f'''
            The LRP API is running. If you\'d like to terminate the LRP click the button below.
            ### API docs
            - [**http://{API_HOST}:{API_PORT}/docs**](http://{API_HOST}:{API_PORT}/docs)
            - [**http://{API_HOST}:{API_PORT}/redoc**](http://{API_HOST}:{API_PORT}/redoc)
        ''')

        if st.button('\U0001F525 Shutdown LRP'):
            requests.get(f'{API_BASE_URL}/shutdown')

            state.API_STARTED = False

            st.experimental_rerun()

def sidebar():
    # ABOUT
    st.sidebar.header('About')
    st.sidebar.info('FastAPI Wrapper to run and stop a long running process (LRP)!\n\n' + \
        '(c) 2022. CloudOpti Ltd. All rights reserved.')
    st.sidebar.markdown('---')


if __name__ == '__main__':
    main()
    sidebar()
