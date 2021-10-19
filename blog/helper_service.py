from flask import Flask

app = Flask(__name__)


@app.get("/rate")
def rate_endpoint():
    return "10"


if __name__ == "__main__":
    app.run("localhost", 8080)
