from torchvision.datasets import ImageFolder
from pathlib import Path


DATASET_DIR = Path("dataset_processed")

splits = ["train", "valid", "test"]


print("\n==========================================")
print("       TOMATO DATASET CHECK")
print("==========================================\n")


for split in splits:

    folder = DATASET_DIR / split

    if not folder.exists():
        print(f"{split}: FOLDER NOT FOUND")
        continue

    dataset = ImageFolder(folder)

    print(f"{split.upper()}")
    print("------------------------------------------")
    print(f"Images  : {len(dataset)}")
    print(f"Classes : {len(dataset.classes)}")
    print(f"Names   : {dataset.classes}")
    print()