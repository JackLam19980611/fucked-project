from ultralytics import YOLO
model=YOLO("newmodel100epoch.pt")
model.predict(source=0, show=True, conf=0.5)