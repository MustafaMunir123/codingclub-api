import os
import uuid
import json

import pyrebase

# import ast
from dotenv import load_dotenv
from typing import Dict

# Loading .env file
load_dotenv("config/.env")

# getting config str-dict and convert it into dict type using ast.literal_eval
RTDB = os.getenv("REALTIME_DB_CONFIG")
# config = ast.literal_eval(os.getenv("REALTIME_DB_CONFIG"))
config = json.loads(RTDB)
email = os.getenv("FB_EMAIL")
password = os.getenv("FB_PASSWORD")


def store_image_get_url(image_file, path: str):
    try:
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email=email, password=password)
        storage = firebase.storage()
        image_file.name = f"{uuid.uuid4()} _ {image_file.name}"
        storage.child("coding_club-api/media/" + path + image_file.name).put(
            image_file, token=user["idToken"]
        )
        image_url = storage.child(
            "coding_club-api/media/" + path + image_file.name
        ).get_url(token=None)
        print(image_url)
        return image_url
    except Exception as ex:
        raise ValueError(f"Error: {ex}")


def delete_image_from_url(url_path):
    try:
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email=email, password=password)
        storage = firebase.storage()  # url=storage.child(url_path).get_url(None)
        storage.delete(url_path, token=user["idToken"])
    except Exception as ex:
        raise ValueError(f"Error: {ex}")


def convert_to_id(dictionary_list: Dict, ManyToManyModel):
    objects_id = []
    for key, value in dictionary_list.items():
        objects_id = []
        print(key, value)
        dictionary_list = value.split(",")  # ast.literal_eval(value)
        print(dictionary_list)
        for obj in dictionary_list:
            kwargs = {key: obj}
            print(kwargs)
            obj = ManyToManyModel.objects.get(**kwargs)
            objects_id.append(obj.id)
    return objects_id


def format_image_url(url):
    path = url.split(".com/o/", 1)[1].replace("%2F", "/").replace("%20", " ")
    path = path.split("?alt")[0]
    print(path)
    return path
