from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "welcome to application"}


@app.get("/health")
def health_check():
    return {"status": "ok"}