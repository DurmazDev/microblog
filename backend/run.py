from app import app
from app.config import Config

if __name__ == "__main__":
    app.run(port=Config.PORT)
