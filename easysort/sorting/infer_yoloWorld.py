# Need:
# !pip install -q inference-gpu[yolo-world]==0.9.12rc1
# !pip install -q supervision==0.19.0rc3
# From: https://colab.research.google.com/github/roboflow/supervision/blob/develop/docs/notebooks/zero-shot-object-detection-with-yolo-world.ipynb#scrollTo=37CMTxw0jSyH

import cv2
import supervision as sv

from easysort.common.logger import EasySortLogger
from inference.models.yolo_world.yolo_world import YOLOWorld
import time
import torch

LOGGER = EasySortLogger()
RANDOM_IMAGE_TENSOR = torch.rand((980, 1280, 3))

class ClassifierYoloWorld:
    def __init__(self, classes: list[str]):
        self.model = YOLOWorld(model_id="yolo_world/l")
        self.classes = classes
        self.model.set_classes(self.classes)

    def __call__(self, image):
        results = self.model.infer(image)
        detections = sv.Detections.from_inference(results)
        world_view_detections = self.cam_view_to_world_view(detections)
        LOGGER.info("Inference done")
        return world_view_detections

    def test_speed(self) -> None:
        time0 = time.time()
        self(RANDOM_IMAGE_TENSOR)
        LOGGER.info(f"Time taken: {round(time.time() - time0, 2)} seconds")

    def visualize(self, image_path: str) -> None:
        image = cv2.imread(image_path)
        detections = self(image)
        sv.plot_image(sv.BoundingBoxAnnotator(thickness=2).annotate(image, detections), (10, 10))

    def cam_view_to_world_view(self, detections):
        # Do computations...
        return detections

if __name__ == "__main__":
    SOURCE_IMAGE_PATH = "_old/test.jpg"
    image = cv2.imread(SOURCE_IMAGE_PATH)
    classifier = ClassifierYoloWorld(classes=["bottle", "cardboard", "metal", "class", "paper", "plastic"])
    detections = classifier(image)
    annotated_image = image.copy()

    BOUNDING_BOX_ANNOTATOR = sv.BoundingBoxAnnotator(thickness=2)
    LABEL_ANNOTATOR = sv.LabelAnnotator(text_thickness=2, text_scale=1, text_color=sv.Color.BLACK)
    annotated_image = BOUNDING_BOX_ANNOTATOR.annotate(annotated_image, detections)
    annotated_image = LABEL_ANNOTATOR.annotate(annotated_image, detections)
    sv.plot_image(annotated_image, (10, 10))

