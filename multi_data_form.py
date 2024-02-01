import requests
import os

url = "http://127.0.0.1:5000/test" ## server url
file_path = f"{os.getcwd()}/accident_recording.avi"

def make_request(detected_accidents, time):
    payload = {
        "accidents": detected_accidents,
        "time": time
    }
    with open(file_path, "rb") as file:
        multipart_form_data = {
            "file" : ('file.avi', file, 'video/x-msvideo')
        }
        response = requests.post(url, files=multipart_form_data, data=payload)



