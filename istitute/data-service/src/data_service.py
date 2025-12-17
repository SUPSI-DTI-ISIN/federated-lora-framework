import argparse

from flask import Flask

from routes import bp

def create_app() -> Flask:
    app = Flask("Data server")

    app.register_blueprint(bp)

    return app

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", type=int, default=8080, help="The port the server is listening")
    args = parser.parse_args()
    app = create_app()

    app.run( host="0.0.0.0", port=args.port, debug=True, use_reloader=False )