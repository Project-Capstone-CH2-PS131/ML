import json
import tensorflow as tf
import numpy as np
import functions_framework
from PIL import Image
from object_detection.utils import label_map_util
from google.cloud import storage

BUCKET_IMAGES_NAME = 'smart-fridge-dev-images'

@functions_framework.http
def process_image_detection(request):
    request_json = request.get_json(silent=True)
        
    storage_client = storage.Client()
    images_bucket = storage_client.get_bucket(BUCKET_IMAGES_NAME)
    images_bucket.get_blob(request_json['image']).download_to_filename('/tmp/image.jpg')

    PATH_TO_SAVED_MODEL = 'models/saved_model'
    PATH_TO_LABEL_MAP = 'models/Fruits-and-Vegetables_label_map.pbtxt'
    PATH_TO_LABEL_IMAGE = '/tmp/image.jpg'

    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABEL_MAP)

    # Resize the image using PIL
    resized_image = Image.open(PATH_TO_LABEL_IMAGE).resize((250, 250))
    image_np = np.array(resized_image)

    # Preprocess the image
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    # Create an empty list to store predicted classes
    predicted_classes = []

    # Iterate through the detected classes and append them to the list
    for detection_class, score in zip(detections['detection_classes'], detections['detection_scores']):
        # Check if the detection score is above a certain threshold (e.g., 0.5)
        if score > 0.45:
            # Get the class name from the category_index
            class_name = category_index[detection_class]['name']
            predicted_classes.append(class_name)

    data = {
        'error': False,
        'ingredients': predicted_classes,
    }

    response = (json.dumps(data), 200, {'Content-Type': 'application/json'})
    print(response)

    return response
