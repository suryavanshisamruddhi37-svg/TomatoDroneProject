import hashlib
from pathlib import Path


DATASET_DIR = Path("dataset")

SPLITS = ["train", "valid", "test"]

EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


def get_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            data = f.read(8192)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def collect_images(split):

    split_path = DATASET_DIR / split

    results = {}

    for file_path in split_path.rglob("*"):

        if file_path.suffix.lower() not in EXTENSIONS:
            continue

        image_hash = get_hash(file_path)

        results.setdefault(
            image_hash,
            []
        ).append(
            str(file_path)
        )

    return results


print("\n==========================================")
print("       ORIGINAL DATASET CHECK")
print("==========================================\n")


all_data = {}

for split in SPLITS:

    print(f"Scanning {split}...")

    data = collect_images(split)

    all_data[split] = data

    total = sum(
        len(files)
        for files in data.values()
    )

    unique = len(data)

    print(f"Images found : {total}")
    print(f"Unique images: {unique}")
    print()


# ==========================================
# CROSS SPLIT CHECK
# ==========================================

train = set(all_data["train"].keys())
valid = set(all_data["valid"].keys())
test = set(all_data["test"].keys())


print("==========================================")
print("       ORIGINAL CROSS-SPLIT CHECK")
print("==========================================\n")


print(
    f"Train ∩ Valid : {len(train & valid)} duplicates"
)

print(
    f"Train ∩ Test  : {len(train & test)} duplicates"
)

print(
    f"Valid ∩ Test  : {len(valid & test)} duplicates"
)


print("\n==========================================")