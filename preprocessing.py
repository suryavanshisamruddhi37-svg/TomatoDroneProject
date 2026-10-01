import cv2
import os
import shutil


INPUT_DIR = "dataset_clean"
OUTPUT_DIR = "dataset_processed"

IMAGE_SIZE = (224, 224)

SPLITS = ["train", "valid", "test"]

SUPPORTED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

def resize_image(image, size=IMAGE_SIZE):
    """
    Resize image to 224 x 224.
    """

    return cv2.resize(
        image,
        size,
        interpolation=cv2.INTER_AREA
    )


def convert_rgb(image):
    """
    Convert BGR image to RGB.
    """

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )


def convert_grayscale(image):
    """
    Convert image to grayscale.
    """

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


def convert_hsv(image):
    """
    Convert image to HSV.
    """

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )


def rotate_image(image, angle):
    """
    Rotate image around its center.
    """

    height, width = image.shape[:2]

    center = (
        width // 2,
        height // 2
    )

    matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    rotated = cv2.warpAffine(
        image,
        matrix,
        (width, height)
    )

    return rotated


def flip_image(image):
    """
    Flip image horizontally.
    """

    return cv2.flip(
        image,
        1
    )


def crop_image(image, crop_ratio=0.9):
    """
    Crop the central region of the image.
    """

    height, width = image.shape[:2]

    new_height = int(
        height * crop_ratio
    )

    new_width = int(
        width * crop_ratio
    )

    start_x = (
        width - new_width
    ) // 2

    start_y = (
        height - new_height
    ) // 2

    cropped = image[
        start_y:start_y + new_height,
        start_x:start_x + new_width
    ]

    return cropped

def preprocess_image(image_path):
    """
    Read and resize a single image.
    """

    image = cv2.imread(
        image_path
    )

    if image is None:
        return None

    # Resize
    image = resize_image(
        image
    )

    return image


def process_dataset():

    
    if os.path.exists(
        OUTPUT_DIR
    ):

        print(
            "\nRemoving old processed dataset..."
        )

        shutil.rmtree(
            OUTPUT_DIR
        )

   
    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    total_images = 0
    processed_images = 0
    failed_images = 0


    print(" TOMATO LEAF DATASET PREPROCESSING")

    print(
        f"\nInput directory : {INPUT_DIR}"
    )

    print(
        f"Output directory: {OUTPUT_DIR}"
    )

    print(
        f"Image size      : {IMAGE_SIZE}"
    )

    for split in SPLITS:

        input_split = os.path.join(
            INPUT_DIR,
            split
        )

        output_split = os.path.join(
            OUTPUT_DIR,
            split
        )

        if not os.path.exists(
            input_split
        ):

            print(
                f"\nSkipping {split}: "
                f"folder not found."
            )

            continue

        print(
            f"\nProcessing: {split}"
        )

      
        class_names = os.listdir(
            input_split
        )

        for class_name in class_names:

            input_class_dir = os.path.join(
                input_split,
                class_name
            )

      
            if not os.path.isdir(
                input_class_dir
            ):
                continue

            output_class_dir = os.path.join(
                output_split,
                class_name
            )

            os.makedirs(
                output_class_dir,
                exist_ok=True
            )

            print(
                f"  Class: {class_name}"
            )

        
            for filename in os.listdir(
                input_class_dir
            ):

                if not filename.lower().endswith(
                    SUPPORTED_EXTENSIONS
                ):
                    continue

                total_images += 1

                input_path = os.path.join(
                    input_class_dir,
                    filename
                )

                output_path = os.path.join(
                    output_class_dir,
                    filename
                )

                image = preprocess_image(
                    input_path
                )

                # Failed image
                if image is None:

                    failed_images += 1

                    print(
                        f"    Failed: {filename}"
                    )

                    continue

                success = cv2.imwrite(
                    output_path,
                    image
                )

                if success:

                    processed_images += 1

                else:

                    failed_images += 1

                    print(
                        f"    Failed to save: "
                        f"{filename}"
                    )



    print(" PREPROCESSING COMPLETE")
  
    print(
        f"Total images found : {total_images}"
    )

    print(
        f"Processed images   : {processed_images}"
    )

    print(
        f"Failed images      : {failed_images}"
    )

    print(
        f"\nProcessed dataset:"
    )

    print(
        f"{OUTPUT_DIR}/"
    )

    print("\n==========================================")
    if failed_images == 0:

        print(
            "RESULT: All images processed successfully."
        )

    else:

        print(
            f"RESULT: {failed_images} "
            f"images could not be processed."
        )

    print("==========================================")


if __name__ == "__main__":

    print(
        "Tomato Leaf Image Preprocessing"
    )

    print(
        "--------------------------------"
    )

    process_dataset()
