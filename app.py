import os
from flask import Flask, request, jsonify, send_from_directory, abort
from dotenv import load_dotenv

# Load environment variables from suji.env instead of .env
load_dotenv('suji.env')

app = Flask(__name__)

# Get your master key from the environment
MASTER_KEY = os.environ.get("MASTER_KEY")
if not MASTER_KEY:
  raise Exception("MASTER_KEY environment variable is not set.")

# Directory where images are stored (adjust as needed)
IMAGES_DIR = os.path.join(os.getcwd(), "images")

@app.route('/delete_image', methods=['POST'])
def delete_image():
  data = request.get_json()
  if not data:
    return jsonify({"error": "Missing JSON data"}), 400

  # Get the password and image filename from the request
  password = data.get("password")
  filename = data.get("filename")

  if password != MASTER_KEY:
    return jsonify({"error": "Unauthorized"}), 401

  # Basic check: the filename should not be a path trying to escape IMAGES_DIR
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

@app.route('/images/<path:filename>')
def serve_image(filename):
  # Serve images from the directory – useful if your client code references these files.
  return send_from_directory(IMAGES_DIR, filename)

if __name__ == '__main__':
  # Ensure images directory exists
  if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)
  app.run(debug=True)
