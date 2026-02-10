from flask import Flask, render_template, request
import os
import pickle
from feature_extractor import extract_features, perform_ela, get_metadata

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

model = pickle.load(open("model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["image"]
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
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
            image=file.filename,
            ela_image=os.path.basename(ela_path),
            metadata=metadata,
            software=software
        )

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
