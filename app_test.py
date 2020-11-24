from fastapi import FastAPI
from Router.App import AppRouter
from Router import SaveDataRouter, GetDataRouter
from starlette.staticfiles import StaticFiles
import os,platform

app = FastAPI()
app.include_router(AppRouter.appRouter)
app.include_router(SaveDataRouter.SaveDataRouter)
app.include_router(GetDataRouter.GetDataRouter)

if platform.system() == "Windows":
    path = '{}/../../webapp/'.format(os.path.dirname(__file__))
else:
    path = './webapp/'
app.mount("/static", StaticFiles(directory=path), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8002, reload = True)