import hashlib
from pathlib import Path


DATASET_DIR = Path("dataset_processed")

SPLITS = ["train", "valid", "test"]

EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


def get_image_hash(file_path):
    """
    Generate a unique hash for an image file.
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(8192)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def collect_hashes(split):
    """
    Collect image hashes for a dataset split.
    """

    hashes = {}

    split_path = DATASET_DIR / split

    for file_path in split_path.rglob("*"):

        if file_path.suffix.lower() not in EXTENSIONS:
            continue

        image_hash = get_image_hash(file_path)

        hashes.setdefault(image_hash, []).append(
            str(file_path)
        )

    return hashes


print("\n==========================================")
print("       DATASET DUPLICATE CHECK")
print("==========================================\n")


all_hashes = {}

for split in SPLITS:

    print(f"Scanning {split}...")

    hashes = collect_hashes(split)

    all_hashes[split] = hashes

    print(f"Images found: {sum(len(v) for v in hashes.values())}")
    print(f"Unique images: {len(hashes)}")
    print()




print("==========================================")
print("       CROSS-SPLIT DUPLICATES")
print("==========================================\n")


train_hashes = set(all_hashes["train"].keys())
valid_hashes = set(all_hashes["valid"].keys())
test_hashes = set(all_hashes["test"].keys())


train_valid = train_hashes & valid_hashes
train_test = train_hashes & test_hashes
valid_test = valid_hashes & test_hashes


print(f"Train ∩ Valid : {len(train_valid)} duplicates")
print(f"Train ∩ Test  : {len(train_test)} duplicates")
print(f"Valid ∩ Test  : {len(valid_test)} duplicates")


print("\n==========================================")

if len(train_test) == 0 and len(train_valid) == 0 and len(valid_test) == 0:

    print("RESULT: No cross-split duplicates found.")
    print("Dataset split looks clean.")

else:

    print("WARNING: Duplicate images found between splits.")
    print("We should fix the dataset split before training.")

print("==========================================")