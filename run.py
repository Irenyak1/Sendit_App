from api.views import app
from flask import Flask

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
