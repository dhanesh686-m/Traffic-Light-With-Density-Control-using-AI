import cv2
import socket
import time
from ultralytics import YOLO

# --- Network Configuration ---
HOST = 'YOUR_ESP32_IP_ADDRESS'
PORT = 80
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connected to ESP32 on Wi-Fi.")
except socket.error as e:
    print(f"Socket connection error: {e}")
    print("Please ensure the ESP32 is powered on and connected to Wi-Fi.")
    exit()

def send_command(command, duration):
    try:
        s.sendall((command + ':' + str(duration) + '\n').encode())
        print(f"Sent command: {command} with duration {duration} ms")
    except socket.error as e:
        print(f"Error sending command: {e}")

# --- Video Capture and YOLO Model ---
cap_north = cv2.VideoCapture(0)
cap_south = cv2.VideoCapture(1)
cap_east = cv2.VideoCapture(2)
cap_west = cv2.VideoCapture(3)

# Load a pre-trained YOLOv8 model
model = YOLO('yolov8n.pt') 

# YOLOv8's COCO dataset classes: 'car', 'motorcycle', 'bus', 'truck'
VEHICLE_CLASSES = [2, 3, 5, 7] 

# --- Traffic Control Logic ---
traffic_lanes = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
FIXED_GREEN_TIME = 5000  # Base green time in ms
TIME_PER_CAR = 1000  # Additional time per car in ms

print("Starting traffic light controller with YOLO...")

while True:
    ret_n, frame_n = cap_north.read()
    ret_s, frame_s = cap_south.read()
    ret_e, frame_e = cap_east.read()
    ret_w, frame_w = cap_west.read()

    if not ret_n or not ret_s or not ret_e or not ret_w:
        print("Error reading from a camera.")
        break

    frames = {'N': frame_n, 'S': frame_s, 'E': frame_e, 'W': frame_w}
    
    # --- Traffic Light Sequence with Timer ---
    
    # NORTH lane
    green_duration_n = FIXED_GREEN_TIME + (traffic_lanes['N'] * TIME_PER_CAR)
    print("Green for NORTH...")
    send_command('N', green_duration_n)
    start_time = time.time()
    while time.time() - start_time < green_duration_n / 1000.0:
        remaining_time = int(green_duration_n / 1000.0 - (time.time() - start_time))
        # Update display for all cameras with the timer
        for direction, frame in frames.items():
            annotated_frame = frame.copy()
            cv2.putText(annotated_frame, f"Timer: {remaining_time}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow(f'Camera: {direction}', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
    
    # SOUTH lane
    green_duration_s = FIXED_GREEN_TIME + (traffic_lanes['S'] * TIME_PER_CAR)
    print("Green for SOUTH...")
    send_command('S', green_duration_s)
    start_time = time.time()
    while time.time() - start_time < green_duration_s / 1000.0:
        remaining_time = int(green_duration_s / 1000.0 - (time.time() - start_time))
        for direction, frame in frames.items():
            annotated_frame = frame.copy()
            cv2.putText(annotated_frame, f"Timer: {remaining_time}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow(f'Camera: {direction}', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

    # EAST lane
    green_duration_e = FIXED_GREEN_TIME + (traffic_lanes['E'] * TIME_PER_CAR)
    print("Green for EAST...")
    send_command('E', green_duration_e)
    start_time = time.time()
    while time.time() - start_time < green_duration_e / 1000.0:
        remaining_time = int(green_duration_e / 1000.0 - (time.time() - start_time))
        for direction, frame in frames.items():
            annotated_frame = frame.copy()
            cv2.putText(annotated_frame, f"Timer: {remaining_time}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow(f'Camera: {direction}', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
            
    # WEST lane
    green_duration_w = FIXED_GREEN_TIME + (traffic_lanes['W'] * TIME_PER_CAR)
    print("Green for WEST...")
    send_command('W', green_duration_w)
    start_time = time.time()
    while time.time() - start_time < green_duration_w / 1000.0:
        remaining_time = int(green_duration_w / 1000.0 - (time.time() - start_time))
        for direction, frame in frames.items():
            annotated_frame = frame.copy()
            cv2.putText(annotated_frame, f"Timer: {remaining_time}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow(f'Camera: {direction}', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

# --- Cleanup ---
cap_north.release()
cap_south.release()
cap_east.release()
cap_west.release()
cv2.destroyAllWindows()
s.close()