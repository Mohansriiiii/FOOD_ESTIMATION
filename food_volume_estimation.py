# food_volume_estimation.py
# Simple mockup for demonstration

class VolumeEstimator:
    def __init__(self, depth_model_path=None, seg_model_path=None):
        print("⚠️ Using mock VolumeEstimator (no real depth/segmentation models loaded).")

    def estimate(self, image_path, food_class):
        """
        Dummy volume estimator. Replace with your real logic later.
        Returns (volume_ml, weight_g)
        """
        # Example rough estimates for testing
        import random
        volume_ml = random.uniform(100, 300)   # pretend volume between 100–300 ml
        weight_g = volume_ml * 1.0             # assume 1 ml ≈ 1 g (for water-like density)
        return volume_ml, weight_g
