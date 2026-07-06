
import threading

import uvicorn
# Import the polling entry function from the poller module.
#
# Unlike executing a module directly (e.g., `python -m app.poller`),
# importing a module only loads its definitions into memory and does
# not execute the module's main application logic.
from app.poller import start_polling_loop
from app.poller import start_polling_loop

# Launch the Uvicorn ASGI server.
#
# Uvicorn hosts the FastAPI application and listens
# for incoming HTTP requests on the specified host
# and port.
def start_api():
    """
    Start the FastAPI application using the Uvicorn ASGI server.

    Uvicorn is responsible for:

    - Listening for incoming HTTP requests.
    - Dispatching requests to FastAPI route handlers.
    - Returning HTTP responses to clients.

    FastAPI implements the application logic,
    while Uvicorn provides the web server runtime.
    """
    uvicorn.run(
    # Launch the FastAPI application using Uvicorn.
    #
    # "app.api:app" is an import string interpreted by Uvicorn:
    #
    #   app.api  -> Python module (app/api.py)
    #   app      -> FastAPI application instance
    #
    # Uvicorn imports the specified module, locates the FastAPI
    # application object, and serves it as an ASGI web application.
        "app.api:app",

        host="0.0.0.0",

        port=8000,

        reload=False

    )


if __name__=="__main__":
    # Start the weather polling service in a background thread.
    #
    # The polling loop continuously collects weather observations
    # from the external API without blocking the REST API server.
    #
    # Running the poller in a separate thread allows the platform
    # to perform data collection and API request handling concurrently.    

    poller_thread=threading.Thread(

        target=start_polling_loop,
    # Run the polling thread as a background daemon.
    # The thread will automatically terminate when the
    # main application exits.
        daemon=True

    )
    # Start the polling thread.
    # The polling loop runs concurrently with the FastAPI server,
    # allowing background data collection without blocking API requests.
    poller_thread.start()

    # Start the FastAPI application using the Uvicorn ASGI server.
    #
    # The main thread remains dedicated to serving HTTP requests,
    # while the weather poller continues running in the background.
    start_api()

"""
Engineering Note

This project uses `run.py` as the application entry point.

Although Python modules can be executed using:

    python -m app.poller ==== if __name__ == "__main__":

the poller module is designed to be imported rather than executed
directly. The application lifecycle is managed centrally by run.py,
which starts both the polling service and the FastAPI server.
"""