import os
from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)

# Load your master key (preferably via environment variables)
MASTER_KEY = os.environ.get("MASTER_KEY", "default_master_key")

# Directory for images (if used)
IMAGES_DIR = os.path.join(os.getcwd(), "images")
if not os.path.exists(IMAGES_DIR):
  os.makedirs(IMAGES_DIR)

# Root route to serve your homepage (index.html)
@app.route('/')
def home():
  return render_template('index.html')

# Example delete_image endpoint
@app.route('/delete_image', methods=['POST'])
def delete_image():
  data = request.get_json()
  if not data:
    return jsonify({"error": "Missing JSON data"}), 400

  password = data.get("password")
  filename = data.get("filename")

  if password != MASTER_KEY:
    return jsonify({"error": "Unauthorized"}), 401

  if "/" in filename or "\\" in filename:
    return jsonify({"error": "Invalid filename"}), 400

  file_path = os.path.join(IMAGES_DIR, filename)
  if not os.path.exists(file_path):
    return jsonify({"error": "File not found"}), 404

  try:
    os.remove(file_path)
    return jsonify({"success": True})
  except Exception as e:
    return jsonify({"error": str(e)}), 500

# Serve images if needed
@app.route('/images/<path:filename>')
def serve_image(filename):
  return send_from_directory(IMAGES_DIR, filename)

# Optional health check endpoint
@app.route('/healthz')
def healthz():
  return 'OK', 200

if __name__ == '__main__':
  app.run(debug=True)
