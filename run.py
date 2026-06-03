
import threading

import uvicorn

from app.poller import start_polling_loop


def start_api():

    uvicorn.run(

        "app.api:app",

        host="0.0.0.0",

        port=8000,

        reload=False

    )


if __name__=="__main__":

    poller_thread=threading.Thread(

        target=start_polling_loop,

        daemon=True

    )

    poller_thread.start()


    start_api()

