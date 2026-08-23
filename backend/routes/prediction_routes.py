from flask import Blueprint, request, jsonify, current_app

from utils.file_utils import allowed_file, save_file


prediction_bp = Blueprint(
    "prediction",
    __name__,
    url_prefix="/api/predictions"
)


@prediction_bp.route("/test", methods=["GET"])
def test_prediction():

    return jsonify({
        "success": True,
        "message": "Prediction API is working"
    })


@prediction_bp.route("/upload", methods=["POST"])
def upload_image():

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "message": "No image uploaded"
        }), 400

    image = request.files["image"]

    if image.filename == "":

        return jsonify({
            "success": False,
            "message": "No image selected"
        }), 400

    if not allowed_file(
        image.filename,
        current_app.config["ALLOWED_EXTENSIONS"]
    ):

        return jsonify({
            "success": False,
            "message": "Invalid image format"
        }), 400

    filename = save_file(
        image,
        current_app.config["UPLOAD_FOLDER"]
    )

    return jsonify({
        "success": True,
        "message": "Image uploaded successfully",
        "filename": filename
    })