import os
from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in allowed_extensions


def save_file(file, upload_folder):

    filename = secure_filename(file.filename)

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        filename
    )

    file.save(file_path)

    return filename