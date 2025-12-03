import torch
from torchvision import transforms, models
import torch.nn as nn
import pandas as pd
from PIL import Image
import random
import os

# ---------------------------------------------------
# DEVICE
# ---------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------------------------------------------
# PATHS (AUTOMATICALLY WORK FOR DEPLOYMENT)
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best_food_model.pth")
NUTRITION_CSV = os.path.join(BASE_DIR, "nutrition.csv")

# ---------------------------------------------------
# LOAD NUTRITION CSV
# ---------------------------------------------------
def load_nutrition_data(csv_path):
    df = pd.read_csv(csv_path)
    df = df.drop_duplicates(subset=["label"])
    return df.set_index("label").to_dict("index")

nutrition_map = load_nutrition_data(NUTRITION_CSV)
class_names = list(nutrition_map.keys())

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------
def load_model(model_path):
    """Loads model in the SAME format it was saved."""
    state = torch.load(model_path, map_location=device)

    # Extract state_dict
    model_state = state["model_state_dict"]

    # Detect number of classes
    num_classes = model_state["fc.weight"].shape[0]

    # Rebuild model architecture
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    # Load weights
    model.load_state_dict(model_state, strict=False)
    model.to(device)
    model.eval()
    return model

model = load_model(MODEL_PATH)

# ---------------------------------------------------
# RANDOM VOLUME & WEIGHT ESTIMATOR
# ---------------------------------------------------
class VolumeEstimator:
    def estimate(self, food_class):
        volume_ml = random.uniform(120, 300)
        weight_g = random.uniform(80, 250)
        return volume_ml, weight_g

volume_estimator = VolumeEstimator()

# ---------------------------------------------------
# TRANSFORM
# ---------------------------------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ---------------------------------------------------
# FINAL PREDICT FUNCTION FOR STREAMLIT APP
# ---------------------------------------------------
def predict_with_nutrition(image_path):
    image = Image.open(image_path).convert("RGB")
    img_tensor = transform(image).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        output = model(img_tensor)
        _, pred_idx = torch.max(output, 1)

    predicted_class = class_names[pred_idx.item() % len(class_names)]

    # Estimate volume & weight
    volume_ml, weight_g = volume_estimator.estimate(predicted_class)

    # Nutrition calculation
    base_nutrition = nutrition_map.get(predicted_class, {})
    actual_nutrition = {
        k: round(v * (weight_g / 100), 2) if isinstance(v, (int, float)) else v
        for k, v in base_nutrition.items()
    }

    return {
        "food": predicted_class,
        "volume_ml": round(volume_ml, 2),
        "weight_grams": round(weight_g, 2),
        "nutrition": actual_nutrition
    }
