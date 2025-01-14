from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    # Serve the index.html file from the static folder
    return send_from_directory('static', 'index.html')

# This will serve any other files (like .pck, .js, .wasm) from the static folder
@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
