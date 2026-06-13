import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
from PIL import Image
import io
from deepface import DeepFace

app = Flask(__name__)
CORS(app)

def base64_to_image(base64_string):
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    return np.array(img)

@app.route("/match-face", methods=["POST"])
def match_face():
    try:
        data = request.get_json()
        probe = base64_to_image(data["probeImage"])
        for person in data["knownFaces"]:
            if not person["EmployeeImage"]:
                continue
            known = base64_to_image(person["EmployeeImage"])
            result = DeepFace.verify(
                probe, known,
                model_name="Facenet",
                enforce_detection=False
            )
            if result["verified"]:
                return jsonify({
                    "matched": True,
                    "EmployeeId": person["EmployeeId"],
                    "EmployeeName": person["EmployeeName"],
                    "EmployeeMobile": person["EmployeeMobile"]
                })
        return jsonify({"matched": False})
    except Exception as e:
        return jsonify({"matched": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)