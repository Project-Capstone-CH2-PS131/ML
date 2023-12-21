# Machine Learning Function

This is a function to run machine learning model.

## Class List for Object Detection Model
- Bitter Melon
- Brinjal
- Cabbage
- Calabash
- Capsicum
- Cauliflower
- Garlic
- Ginger
- Green Chili
- Lady Finger
- Onion
- Potato
- Sponge Gourd
- Tomato
- Apple
- Banana
- Cucumber
- Dragon Fruit
- Guava
- Orange
- Oren
- Pear
- Pineapple
- Sugar Apple

## How to Deploy

Set project id and region.

``` bash
export PROJECT_ID='PROJECT_ID'
export REGION='REGION'
```

Deploy to 'Cloud Function'

```bash
gcloud functions deploy object-detection-dev \
    --project $PROJECT_ID \
    --region $REGION \
    --entry-point process_image_detection \
    --allow-unauthenticated \
    --runtime python39 \
    --max-instances 2 \
    --memory 2048MB \
    --trigger-http \
    --service-account 'service account'
```