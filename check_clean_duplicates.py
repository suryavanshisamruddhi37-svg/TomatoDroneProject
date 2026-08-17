import hashlib
from pathlib import Path


DATASET_DIR = Path("dataset_clean")

SPLITS = ["train", "valid", "test"]

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


def get_image_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(8192)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def collect_hashes(split):

    split_dir = DATASET_DIR / split

    hashes = {}

    for image_path in split_dir.rglob("*"):

        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        image_hash = get_image_hash(image_path)

        hashes[image_hash] = image_path

    return hashes


print("\n==========================================")
print("       CLEAN DATASET DUPLICATE CHECK")
print("==========================================\n")


all_hashes = {}

for split in SPLITS:

    hashes = collect_hashes(split)

    all_hashes[split] = hashes

    print(
        f"{split.upper():5} : "
        f"{len(hashes)} unique images"
    )


train = set(all_hashes["train"].keys())
valid = set(all_hashes["valid"].keys())
test = set(all_hashes["test"].keys())


train_valid = train & valid
train_test = train & test
valid_test = valid & test


print("\n==========================================")
print("       CROSS-SPLIT DUPLICATES")
print("==========================================\n")

print(
    f"Train ∩ Valid : {len(train_valid)}"
)

print(
    f"Train ∩ Test  : {len(train_test)}"
)

print(
    f"Valid ∩ Test  : {len(valid_test)}"
)


print("\n==========================================")

if (
    len(train_valid) == 0
    and len(train_test) == 0
    and len(valid_test) == 0
):

    print("RESULT: DATASET IS CLEAN")
    print("No duplicate images exist between splits.")

else:

    print("WARNING: DUPLICATES FOUND")
    print("Do NOT train the model yet.")

print("==========================================\n")