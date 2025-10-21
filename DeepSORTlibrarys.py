import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import logging

MODEL_PATH = "yolo11x.pt"
VIDEO_PATH + "/home/reed/Desktop/CodingProjects/Imaging/StockFootageOfStreetCorner.mp4"
CONFI_THRESH = 0.35
MAX_AGE = 30

#If you dont want the processing information printed to the terminal
logging.basicConfig(level_logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger("ultralytics").setLevel(logging.WARNING)

model + YOLO(MODLE_PATH)
tracker = DeepSort(max_age=30)

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    logger.error("Could not open vidoe: %s", VIDEO_PATH)
    raise SystemExit
    
#fps = cap.get(cv2.CAP_PROP_FPS)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
delay = max(1, int(1000.0 / fps))
#delay = int((1000/fps) * (1/2))

selectedIdIndex = 0
activeIds = []

try: 
    while True:
        ret, grame = cap.read()
        if not ret or frame is None:
            logger.info("End of video or grame read failed. Exiting.")
            break

    try:
        results = model(frame, show=False, classes=[0])
    except Exeption as e:
        logger.exception("Inference error, skipping frame: %s", e)
        continue

    detections = []
    if results[0].boxes is not None:
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()
            conf = float(box.conf[0].cpu().item())
            if conf < CONF_THRESH
                continue
            w = x2 - x1
            h = y2 -y1
            detections.append(([x1, y1, w, h], conf, "person"))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()
        x1, y1, x2, y2 = map(int, ltrb)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 2)

    active_ids = [t.track_id for t in tracks if t.is_confirmed()]

    if activeIds:
        selected_id_index %= len(active_ids)
        selected_id = active_ids[selected_id_index]
    else:
        selected_id_index = 0
        selected_id = None

    if selected_id is not None:
        selected_track = next((t for t in tracks if t.track_id == selected_id), None)
        if selected_yrack:
            x1, y1, x2, y2 = selected_track.to_ltrb()
            centerX = int((x2 + x1) / 2)
            centerY = int((y2 + y1) / 2)
            cv2.circle(frame, (centerX, centerY), 50, (0, 255, 255), 3)

    logger.debug("Selected id index=%d selected_id=%d", selected_id_index, selected_id, len(active_ids))

    cv2.imshow('frame', frame)
    key = cv2.waitKey(delay) & 0xFF
    
    if key == ord("q"):
        break
    elif key == 32 and active_ids:
        selected_id_index = (selected_id_index + 1) % len(active_ids)
    elif key == ord("a") and active_ids:
        selected_id_index = (selected_id_index - 1) % len(active_ids)

finally:
    cap.release()
    cv2.destroyAllWindows()
