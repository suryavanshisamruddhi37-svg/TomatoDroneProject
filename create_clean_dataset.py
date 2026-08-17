import hashlib
import shutil
import random
from pathlib import Path
from collections import defaultdict


# ==========================================
# CONFIGURATION
# ==========================================

SOURCE_DIR = Path("dataset")
OUTPUT_DIR = Path("dataset_clean")

SPLITS = ["train", "valid", "test"]

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

TRAIN_RATIO = 0.70
VALID_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42


# ==========================================
# CALCULATE IMAGE HASH
# ==========================================

def get_image_hash(file_path):
    """
    Generate SHA-256 hash for an image.
    Identical files will have the same hash.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(8192)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


# ==========================================
# COLLECT UNIQUE IMAGES
# ==========================================

def collect_unique_images():

    unique_images = {}

    print("\n==========================================")
    print(" COLLECTING UNIQUE TOMATO IMAGES")
    print("==========================================\n")

    for split in SPLITS:

        split_dir = SOURCE_DIR / split

        if not split_dir.exists():

            print(f"Skipping missing folder: {split}")
            continue

        print(f"Scanning: {split}")

        for class_dir in split_dir.iterdir():

            if not class_dir.is_dir():
                continue

            class_name = class_dir.name

            for image_path in class_dir.rglob("*"):

                if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                    continue

                image_hash = get_image_hash(image_path)

                # Keep only the first copy
                if image_hash not in unique_images:

                    unique_images[image_hash] = {
                        "path": image_path,
                        "class": class_name
                    }

    print()
    print(
        f"Unique images found: {len(unique_images)}"
    )

    return unique_images


# ==========================================
# GROUP IMAGES BY CLASS
# ==========================================

def group_by_class(unique_images):

    grouped = defaultdict(list)

    for image_data in unique_images.values():

        grouped[
            image_data["class"]
        ].append(
            image_data["path"]
        )

    return grouped


# ==========================================
# CREATE CLEAN DATASET
# ==========================================

def create_clean_dataset(grouped):

    random.seed(RANDOM_SEED)

    # Remove previous clean dataset if it exists
    if OUTPUT_DIR.exists():

        print("\nRemoving previous dataset_clean folder...")

        shutil.rmtree(OUTPUT_DIR)

    print("\n==========================================")
    print(" CREATING CLEAN DATASET")
    print("==========================================\n")

    total_train = 0
    total_valid = 0
    total_test = 0

    for class_name in sorted(grouped.keys()):

        images = grouped[class_name]

        # Shuffle images randomly
        random.shuffle(images)

        total_images = len(images)

        # Calculate split sizes
        train_count = int(
            total_images * TRAIN_RATIO
        )

        valid_count = int(
            total_images * VALID_RATIO
        )

        train_images = images[
            :train_count
        ]

        valid_images = images[
            train_count:
            train_count + valid_count
        ]

        test_images = images[
            train_count + valid_count:
        ]

        print(
            f"{class_name}: "
            f"Total={total_images}, "
            f"Train={len(train_images)}, "
            f"Valid={len(valid_images)}, "
            f"Test={len(test_images)}"
        )

        # Create directories
        train_dir = (
            OUTPUT_DIR
            / "train"
            / class_name
        )

        valid_dir = (
            OUTPUT_DIR
            / "valid"
            / class_name
        )

        test_dir = (
            OUTPUT_DIR
            / "test"
            / class_name
        )

        train_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        valid_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        test_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # Copy images
        copy_images(
            train_images,
            train_dir
        )

        copy_images(
            valid_images,
            valid_dir
        )

        copy_images(
            test_images,
            test_dir
        )

        total_train += len(train_images)
        total_valid += len(valid_images)
        total_test += len(test_images)

    print("\n==========================================")
    print(" DATASET SPLIT SUMMARY")
    print("==========================================")

    print(f"Training images   : {total_train}")
    print(f"Validation images : {total_valid}")
    print(f"Testing images    : {total_test}")
    print(
        f"Total images      : "
        f"{total_train + total_valid + total_test}"
    )


# ==========================================
# COPY IMAGES
# ==========================================

def copy_images(images, destination):

    for index, image_path in enumerate(images):

        # Keep original extension
        extension = image_path.suffix.lower()

        new_name = (
            f"{index:05d}{extension}"
        )

        destination_path = (
            destination / new_name
        )

        shutil.copy2(
            image_path,
            destination_path
        )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print("\n==========================================")
    print(" TOMATO CLEAN DATASET CREATION")
    print("==========================================")

    print("\nSource:")
    print(SOURCE_DIR)

    print("\nDestination:")
    print(OUTPUT_DIR)

    # Step 1: Collect unique images
    unique_images = collect_unique_images()

    if len(unique_images) == 0:

        print("\nERROR: No images found.")
        print("Check your dataset folder.")

        raise SystemExit

    # Step 2: Group by disease
    grouped_images = group_by_class(
        unique_images
    )

    # Step 3: Create clean split
    create_clean_dataset(
        grouped_images
    )

    print("\n==========================================")
    print(" CLEAN DATASET CREATED SUCCESSFULLY")
    print("==========================================")

    print("\nLocation:")
    print(OUTPUT_DIR)

    print("\nSplit ratio:")
    print("70% Training")
    print("15% Validation")
    print("15% Testing")

    print("\nOriginal dataset was NOT modified.")

    print("\nNext step:")
    print("Verify the new dataset for duplicates.")