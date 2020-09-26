import uvicorn
from Api.common_api import app

if __name__ == "__main__":
 	uvicorn.run(app=app, host="0.0.0.0", port=8001)