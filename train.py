import os
import copy
import json
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader


DATASET_DIR = "dataset_clean"
MODEL_DIR = "models"
RESULTS_DIR = "results"

BATCH_SIZE = 16
NUM_EPOCHS = 15

LEARNING_RATE = 0.0001

IMAGE_SIZE = 224

NUM_WORKERS = 0

RANDOM_SEED = 42


torch.manual_seed(RANDOM_SEED)

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")


print("\n==========================================")
print("       TOMATO DISEASE CLASSIFIER")
print("==========================================")

print(f"\nDevice: {DEVICE}")


os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


train_transforms = transforms.Compose([
    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomVerticalFlip(
        p=0.2
    ),

    transforms.RandomRotation(
        degrees=20
    ),

    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
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


valid_test_transforms = transforms.Compose([
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


train_dir = os.path.join(
    DATASET_DIR,
    "train"
)

valid_dir = os.path.join(
    DATASET_DIR,
    "valid"
)

test_dir = os.path.join(
    DATASET_DIR,
    "test"
)


train_dataset = datasets.ImageFolder(
    train_dir,
    transform=train_transforms
)


valid_dataset = datasets.ImageFolder(
    valid_dir,
    transform=valid_test_transforms
)


test_dataset = datasets.ImageFolder(
    test_dir,
    transform=valid_test_transforms
)


class_names = train_dataset.classes

num_classes = len(
    class_names
)


print("\n==========================================")
print("DATASET INFORMATION")
print("==========================================")

print(
    f"\nTraining images   : "
    f"{len(train_dataset)}"
)

print(
    f"Validation images : "
    f"{len(valid_dataset)}"
)

print(
    f"Testing images    : "
    f"{len(test_dataset)}"
)

print(
    f"Number of classes : "
    f"{num_classes}"
)

print("\nClasses:")

for index, class_name in enumerate(
    class_names
):
    print(
        f"{index}: {class_name}"
    )


class_file = os.path.join(
    MODEL_DIR,
    "class_names.json"
)

with open(
    class_file,
    "w"
) as file:

    json.dump(
        class_names,
        file,
        indent=4
    )


train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS
)


valid_loader = DataLoader(
    valid_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS
)


test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS
)


print("\n==========================================")
print("LOADING RESNET18")
print("==========================================")

try:

    weights = models.ResNet18_Weights.DEFAULT

    model = models.resnet18(
        weights=weights
    )

    print(
        "Pretrained ResNet18 loaded."
    )

except Exception as e:

    print(
        f"Could not load pretrained weights: {e}"
    )

    print(
        "Using ResNet18 without pretrained weights."
    )

    model = models.resnet18(
        weights=None
    )


num_features = model.fc.in_features

model.fc = nn.Linear(
    num_features,
    num_classes
)


model = model.to(
    DEVICE
)


class_counts = [
    0
] * num_classes


for _, label in train_dataset.samples:

    class_counts[label] += 1


total_samples = sum(
    class_counts
)


class_weights = []

for count in class_counts:

    weight = (
        total_samples
        /
        (num_classes * count)
    )

    class_weights.append(
        weight
    )


class_weights = torch.tensor(
    class_weights,
    dtype=torch.float32
)


class_weights = class_weights.to(
    DEVICE
)


print("\nClass counts:")

for i in range(num_classes):

    print(
        f"{class_names[i]}: "
        f"{class_counts[i]}"
    )


criterion = nn.CrossEntropyLoss(
    weight=class_weights
)


optimizer = optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=0.0001
)


scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=2
)


def train_one_epoch():

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images = images.to(
            DEVICE
        )

        labels = labels.to(
            DEVICE
        )

        optimizer.zero_grad()

        outputs = model(
            images
        )

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item()
            *
            images.size(0)
        )

        _, predictions = torch.max(
            outputs,
            1
        )

        total += labels.size(0)

        correct += (
            predictions == labels
        ).sum().item()

    epoch_loss = (
        running_loss / total
    )

    epoch_accuracy = (
        correct / total
    ) * 100

    return (
        epoch_loss,
        epoch_accuracy
    )


def validate():

    model.eval()

    running_loss = 0.0

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in valid_loader:

            images = images.to(
                DEVICE
            )

            labels = labels.to(
                DEVICE
            )

            outputs = model(
                images
            )

            loss = criterion(
                outputs,
                labels
            )

            running_loss += (
                loss.item()
                *
                images.size(0)
            )

            _, predictions = torch.max(
                outputs,
                1
            )

            total += labels.size(0)

            correct += (
                predictions == labels
            ).sum().item()

    epoch_loss = (
        running_loss / total
    )

    epoch_accuracy = (
        correct / total
    ) * 100

    return (
        epoch_loss,
        epoch_accuracy
    )


print("\n==========================================")
print("STARTING TRAINING")
print("==========================================")

print(
    f"\nEpochs: {NUM_EPOCHS}"
)

print(
    f"Batch size: {BATCH_SIZE}"
)

print(
    f"Learning rate: {LEARNING_RATE}"
)

print(
    f"Device: {DEVICE}"
)


best_accuracy = 0.0

best_model_weights = copy.deepcopy(
    model.state_dict()
)


train_losses = []
train_accuracies = []

valid_losses = []
valid_accuracies = []


for epoch in range(
    NUM_EPOCHS
):

    print(
        f"\nEpoch "
        f"{epoch + 1}/{NUM_EPOCHS}"
    )

    train_loss, train_accuracy = (
        train_one_epoch()
    )

    valid_loss, valid_accuracy = (
        validate()
    )

    scheduler.step(
        valid_accuracy
    )


    train_losses.append(
        train_loss
    )

    train_accuracies.append(
        train_accuracy
    )

    valid_losses.append(
        valid_loss
    )

    valid_accuracies.append(
        valid_accuracy
    )


    print(
        f"Train Loss: "
        f"{train_loss:.4f}"
    )

    print(
        f"Train Accuracy: "
        f"{train_accuracy:.2f}%"
    )

    print(
        f"Validation Loss: "
        f"{valid_loss:.4f}"
    )

    print(
        f"Validation Accuracy: "
        f"{valid_accuracy:.2f}%"
    )


    if valid_accuracy > best_accuracy:

        best_accuracy = (
            valid_accuracy
        )

        best_model_weights = (
            copy.deepcopy(
                model.state_dict()
            )
        )

        best_model_path = os.path.join(
            MODEL_DIR,
            "best_model.pth"
        )

        torch.save(
            {
                "model_state_dict":
                    best_model_weights,

                "class_names":
                    class_names,

                "num_classes":
                    num_classes,

                "best_validation_accuracy":
                    best_accuracy
            },
            best_model_path
        )

        print(
            "Best model saved!"
        )

        print(
            f"Best validation accuracy: "
            f"{best_accuracy:.2f}%"
        )


model.load_state_dict(
    best_model_weights
)


print("\n==========================================")
print("TRAINING COMPLETE")


print(
    f"\nBest validation accuracy: "
    f"{best_accuracy:.2f}%"
)

print(
    "\nModel saved at:"
)

print(
    os.path.join(
        MODEL_DIR,
        "best_model.pth"
    )
)


print(
    "\nClass names saved at:"
)

print(
    class_file
)

print(
    "\n=========================================="
)


history = {
    "train_loss": train_losses,
    "train_accuracy": train_accuracies,
    "valid_loss": valid_losses,
    "valid_accuracy": valid_accuracies
}


history_path = os.path.join(
    RESULTS_DIR,
    "training_history.json"
)

with open(
    history_path,
    "w"
) as file:

    json.dump(
        history,
        file,
        indent=4
    )


epochs = range(
    1,
    NUM_EPOCHS + 1
)


plt.figure(
    figsize=(8, 5)
)

plt.plot(
    epochs,
    train_accuracies,
    marker="o",
    label="Training Accuracy"
)

plt.plot(
    epochs,
    valid_accuracies,
    marker="o",
    label="Validation Accuracy"
)

plt.xlabel(
    "Epoch"
)

plt.ylabel(
    "Accuracy (%)"
)

plt.title(
    "Training and Validation Accuracy"
)

plt.legend()

plt.grid(
    True
)

plt.tight_layout()


accuracy_graph = os.path.join(
    RESULTS_DIR,
    "training_validation_accuracy.png"
)

plt.savefig(
    accuracy_graph,
    dpi=300
)

plt.close()


plt.figure(
    figsize=(8, 5)
)

plt.plot(
    epochs,
    train_losses,
    marker="o",
    label="Training Loss"
)

plt.plot(
    epochs,
    valid_losses,
    marker="o",
    label="Validation Loss"
)

plt.xlabel(
    "Epoch"
)

plt.ylabel(
    "Loss"
)

plt.title(
    "Training and Validation Loss"
)

plt.legend()

plt.grid(
    True
)

plt.tight_layout()


loss_graph = os.path.join(
    RESULTS_DIR,
    "training_validation_loss.png"
)

plt.savefig(
    loss_graph,
    dpi=300
)

plt.close()


print(
    "\nTraining graphs saved:"
)

print(
    accuracy_graph
)

print(
    loss_graph
)

print(
    history_path
)