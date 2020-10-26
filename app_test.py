from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from Router.AppRouter import AppRouter

app = FastAPI()
app.include_router(AppRouter)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=9000)