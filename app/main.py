from fastapi import FastAPI
from dotenv import load_dotenv

from .routes import router

# load environment variables once
load_dotenv()

app = FastAPI()
app.include_router(router)


# keep a convenience entrypoint if run directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
