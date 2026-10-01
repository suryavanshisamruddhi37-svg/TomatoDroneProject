import os
import json
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

DATASET_DIR = "dataset_processed"
MODEL_PATH = "models/best_model.pth"
RESULTS_DIR = "results"
IMAGE_SIZE = 224
BATCH_SIZE = 16
NUM_WORKERS = 0

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

print("\n==========================================")
print("       TOMATO DISEASE MODEL EVALUATION")
print("==========================================")
print(f"\nDevice: {DEVICE}")

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)

test_transform = transforms.Compose([
    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],
        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])

test_dir = os.path.join(
    DATASET_DIR,
    "test"
)

test_dataset = datasets.ImageFolder(
    test_dir,
    transform=test_transform
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS
)

class_names = test_dataset.classes
num_classes = len(class_names)

print("\n==========================================")
print("TEST DATASET")
print("==========================================")

print(
    f"\nTest images : {len(test_dataset)}"
)

print(
    f"Classes     : {num_classes}"
)

for i, name in enumerate(class_names):
    print(
        f"{i}: {name}"
    )

model = models.resnet18(
    weights=None
)

num_features = model.fc.in_features

model.fc = nn.Linear(
    num_features,
    num_classes
)

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)

if "model_state_dict" in checkpoint:
    model.load_state_dict(
        checkpoint["model_state_dict"]
    )
else:
    model.load_state_dict(
        checkpoint
    )

model = model.to(
    DEVICE
)

model.eval()

all_predictions = []
all_labels = []

print("\n==========================================")
print("RUNNING TEST PREDICTIONS")
print("==========================================")

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(
            DEVICE
        )

        outputs = model(
            images
        )

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        all_predictions.extend(
            predictions.cpu().numpy()
        )

        all_labels.extend(
            labels.numpy()
        )

accuracy = accuracy_score(
    all_labels,
    all_predictions
)

precision = precision_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)

print("\n==========================================")
print("FINAL TEST RESULTS")
print("==========================================")

print(
    f"\nAccuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1 Score  : {f1 * 100:.2f}%"
)

report = classification_report(
    all_labels,
    all_predictions,
    target_names=class_names,
    zero_division=0
)

print("\n==========================================")
print("CLASSIFICATION REPORT")
print("==========================================\n")

print(report)

report_path = os.path.join(
    RESULTS_DIR,
    "classification_report.txt"
)

with open(
    report_path,
    "w"
) as file:
    file.write(
        "Tomato Disease Classification Report\n"
    )

    file.write(
        "=====================================\n\n"
    )

    file.write(
        f"Accuracy: {accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Precision: {precision * 100:.2f}%\n"
    )

    file.write(
        f"Recall: {recall * 100:.2f}%\n"
    )

    file.write(
        f"F1 Score: {f1 * 100:.2f}%\n\n"
    )

    file.write(
        report
    )

cm = confusion_matrix(
    all_labels,
    all_predictions
)

print("\n==========================================")
print("CONFUSION MATRIX")
print("==========================================\n")

print(cm)

cm_path = os.path.join(
    RESULTS_DIR,
    "confusion_matrix.txt"
)

with open(
    cm_path,
    "w"
) as file:
    file.write(
        "Confusion Matrix\n"
    )

    file.write(
        "================\n\n"
    )

    file.write(
        str(cm)
    )

print("\n==========================================")
print("EVALUATION COMPLETE")
print("==========================================")

print(
    "\nClassification report:"
)

print(
    report_path
)

print(
    "\nConfusion matrix:"
)

print(
    cm_path
)