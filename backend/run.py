from app import create_app, socketio
from app.config import HOST, PORT, DEBUG

if __name__ == "__main__":
    app = create_app()
    app.run(host=HOST, port=PORT, debug=DEBUG)
