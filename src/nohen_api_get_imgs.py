import os

import requests


def get_nohen_imgs_by_requests(data_id: str):
    api_url = os.getenv("NOHEN_API_URL")
    json = {
        "token": os.getenv("NOHEN_API_TOKEN"),
        # 降水量："rain", 風向・風速："wind"
        "data_id": data_id,
        "data_type": "prab",
    }

    response = requests.post(api_url, json=json)
    response.raise_for_status()

    image_url = response.json().get("image_url")
    img_response = requests.get(image_url)
    img_response.raise_for_status()

    img_path = f"/tmp/data/nohen_{data_id}.png"
    with open(img_path, "wb") as f:
        f.write(img_response.content)

    return img_path
