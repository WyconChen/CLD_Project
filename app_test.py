from fastapi import FastAPI
from Router.AppRouter import AppRouter

app = FastAPI()
app.include_router(AppRouter.appRouter)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=9000)