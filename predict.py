import os
import json
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_PATH = "models/best_model.pth"
IMAGE_FOLDER = "new_images"

IMAGE_SIZE = 224


# =========================================================
# DEVICE
# =========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# =========================================================
# LOAD MODEL CHECKPOINT
# =========================================================

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)

class_names = checkpoint["class_names"]
num_classes = checkpoint["num_classes"]


# =========================================================
# CREATE RESNET18
# =========================================================

model = models.resnet18(
    weights=None
)

num_features = model.fc.in_features

model.fc = nn.Linear(
    num_features,
    num_classes
)


model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(DEVICE)

model.eval()


# =========================================================
# IMAGE TRANSFORMATION
# =========================================================

transform = transforms.Compose([

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


# =========================================================
# PREDICT ONE IMAGE
# =========================================================

def predict_image(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    image_tensor = transform(
        image
    )

    image_tensor = image_tensor.unsqueeze(
        0
    )

    image_tensor = image_tensor.to(
        DEVICE
    )

    with torch.no_grad():

        outputs = model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            1
        )

    predicted_class = class_names[
        prediction.item()
    ]

    confidence_percentage = (
        confidence.item() * 100
    )

    return (
        predicted_class,
        confidence_percentage
    )


# =========================================================
# MAIN
# =========================================================

print("\n==========================================")
print("       TOMATO DISEASE PREDICTION")
print("==========================================")

print(
    f"\nDevice: {DEVICE}"
)

print(
    f"Images folder: {IMAGE_FOLDER}"
)

print("\n==========================================")
print("PREDICTIONS")
print("==========================================")


# Supported image formats

valid_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


image_files = [

    file_name

    for file_name in os.listdir(
        IMAGE_FOLDER
    )

    if file_name.lower().endswith(
        valid_extensions
    )
]


image_files.sort()


if len(image_files) == 0:

    print(
        "\nNo images found."
    )

    print(
        "Put your tomato leaf images inside:"
    )

    print(
        IMAGE_FOLDER
    )

    exit()


print(
    f"\nTotal images found: "
    f"{len(image_files)}"
)


# =========================================================
# PREDICT ALL IMAGES
# =========================================================

for index, file_name in enumerate(
    image_files,
    start=1
):

    image_path = os.path.join(
        IMAGE_FOLDER,
        file_name
    )

    try:

        predicted_class, confidence = (
            predict_image(
                image_path
            )
        )

        print(
            f"\n{index}. {file_name}"
        )

        print(
            f"   Disease: "
            f"{predicted_class}"
        )

        print(
            f"   Confidence: "
            f"{confidence:.2f}%"
        )

    except Exception as e:

        print(
            f"\n{index}. {file_name}"
        )

        print(
            f"   ERROR: {e}"
        )


# =========================================================
# COMPLETE
# =========================================================

print("\n==========================================")
print("PREDICTION COMPLETE")
print("==========================================")