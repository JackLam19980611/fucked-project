import cv2
import requests
server_url = "https://accident-alert.azurewebsites.net/streaming/upload"
def stream(frame):
    _ , img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = img_encoded.tobytes()
    try:
        img_file = {'file': ('image.jpg', img_bytes, 'image/jpeg')}
        # Send the image data to the server
        response = requests.post(server_url, files=img_file)
        print("Server response:", response.text)
    except Exception as e:
        print("Error sending frame to server:", e)