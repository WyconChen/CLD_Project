from fastapi import FastAPI
from Router.App import AppRouter
from starlette.staticfiles import StaticFiles
import os,platform


app = FastAPI()
app.include_router(AppRouter.appRouter)
if platform.system() == "Windows":
    path = '{}/../../webapp/'.format(os.path.dirname(__file__))
else:
    path = './webapp/'.format(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=path), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=9000)