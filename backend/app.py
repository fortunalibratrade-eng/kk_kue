from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, json, uuid

app = Flask(__name__)
CORS(app)

DATA_FILE = "data/items.json"
UPLOAD_FOLDER = "uploads"

os.makedirs("data", exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ===============================
# PUBLIC: ambil data
# ===============================
@app.get("/api/items")
def get_items():
    return jsonify(load_data())

# ===============================
# ADMIN: tambah item
# ===============================
@app.post("/api/items")
def add_item():
    data = load_data()

    name = request.form.get("name")
    file = request.files.get("image")

    if not file:
        return {"error": "image required"}, 400

    filename = f"{uuid.uuid4()}_{file.filename}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    item = {
        "id": str(uuid.uuid4()),
        "name": name,
        "image": f"/uploads/{filename}"
    }

    data.append(item)
    save_data(data)

    return item

# ===============================
# ADMIN: hapus item
# ===============================
@app.delete("/api/items/<id>")
def delete_item(id):
    data = load_data()
    data = [i for i in data if i["id"] != id]
    save_data(data)
    return {"status": "deleted"}

# ===============================
# serve gambar
# ===============================
@app.get("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ===============================
if __name__ == "__main__":
    app.run()