from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import pickle
from feature_extractor import extract_features, perform_ela, get_metadata

app = Flask(__name__)

# Upload folder (Fly-safe)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load ML model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "image" not in request.files:
            return "No file uploaded", 400

        file = request.files["image"]
        if file.filename == "":
            return "No selected file", 400

        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        # ML prediction
        features = extract_features(path)
        prediction = model.predict([features])[0]
        result = "Tampered" if prediction == 1 else "Original"

        # ELA + Metadata
        ela_path = perform_ela(path)
        metadata, software = get_metadata(path)

        return render_template(
            "result.html",
            result=result,
            image=filename,
            ela_image=os.path.basename(ela_path),
            metadata=metadata,
            software=software
        )

    return render_template("upload.html")


if __name__ == "__main__":
    app.run()
