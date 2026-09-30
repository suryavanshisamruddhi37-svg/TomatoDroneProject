import os
import sys
from pathlib import Path

from flask import Blueprint, request, jsonify, current_app
from utils.file_utils import allowed_file, save_file
from utils.database import get_db_connection
from utils.model_predictor import predict_image
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from severity import analyze_infection

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
    image_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    connection = None
    cursor = None

    try:
        predicted_class, confidence = predict_image(image_path)
        quality = analyze_infection(image_path)

        # Convert, for example, Septoria_leaf_spot to Septoria_leaf_spot.
        disease_label = predicted_class.split("___")[-1].strip()
        result = "Healthy" if "healthy" in disease_label.lower() else "Infected"

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT crop_id FROM crops WHERE crop_name = %s",
            ("Tomato",)
        )
        crop_row = cursor.fetchone()

        if crop_row is None:
            return jsonify({
                "success": False,
                "message": "Tomato was not found in the crops table"
            }), 500

        crop_id = crop_row[0]
        disease_id = None

        if result == "Infected":
            cursor.execute(
                """
                SELECT disease_id
                FROM diseases
                WHERE LOWER(REPLACE(disease_name, ' ', '_')) = LOWER(%s)
                """,
                (disease_label,)
            )
            disease_row = cursor.fetchone()

            if disease_row is None:
                return jsonify({
                    "success": False,
                    "message": (
                        f"{disease_label} is not in the diseases table. "
                        "Add it there, then try again."
                    )
                }), 422

            disease_id = disease_row[0]

        cursor.execute(
            """
            INSERT INTO leaf_assessments
                (crop_id, disease_id, image_path, result, confidence)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (crop_id, disease_id, filename, result, confidence)
        )
        cursor.execute(
            """
            INSERT INTO leaf_assessments
                (crop_id, disease_id, image_path, result, confidence)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (crop_id, disease_id, filename, result, confidence)
        )

        cursor.execute(
            """
            INSERT INTO quality_assessments
                (crop_id, image_path, quality_grade, notes,
                 infection_percentage, severity)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                crop_id,
                filename,
                None,
                f"Estimated infected area: {quality['infection_percentage']:.2f}%",
                quality["infection_percentage"],
                quality["severity"]
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "filename": filename,
            "result": result,
            "disease": disease_label,
            "confidence": round(confidence, 2),
            "infection_percentage": round(quality["infection_percentage"], 2),
            "severity": quality["severity"],
            "message": "Prediction saved to the database"
        })  

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()