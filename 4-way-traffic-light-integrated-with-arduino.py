import cv2
import time
from ultralytics import YOLO
import math
import socket
import sys


HOST = '0.0.0.0' 
PORT = 8080       
CAMERA_INDEX = 0  

client_socket = None 

def setup_server():
    
    global client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"TCP Server running on {HOST}:{PORT}. Waiting for ESP32 client...")
        client_socket, addr = server_socket.accept()
        print(f"Client connected from: {addr}")
        return True
    except socket.error as e:
        print(f"FATAL ERROR: Could not start TCP server on port {PORT}. Error: {e}")
        return False

FIXED_BASE_TIME = 8     
MAX_GREEN_TIME = 60      
YELLOW_TIME = 3          


TIME_HEAVY = 15          
TIME_MEDIUM = 10         
TIME_LIGHT = 5           


try:
    
    model_custom = YOLO(r"E:\TRAFFIC LIGHT PROJECT\best.pt") 
    print("Custom model 'best.pt' loaded successfully.")
    
    
    model_coco = YOLO('yolov8n.pt') 
    print("Pre-trained model 'yolov8n.pt' loaded successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not load one or both models. Error: {e}")
    sys.exit(1)


CUSTOM_RICKSHAW_ID = 0  


HEAVY_CLASSES_COCO = [5, 7]  
MEDIUM_CLASSES_COCO = [2]     
LIGHT_CLASSES_COCO = [1, 3]   

ZERO_COUNTS = {'heavy': 0, 'medium': 0, 'light': 0} 
vehicle_counts = {
    'N': dict(ZERO_COUNTS), 
    'S': dict(ZERO_COUNTS), 
    'E': dict(ZERO_COUNTS), 
    'W': dict(ZERO_COUNTS)
}
DIRECTIONS = ['N', 'S', 'E', 'W'] 



def detect_vehicles(frame):
    """Performs DUAL-MODEL YOLO detection and returns merged counts."""
    if frame is None: return dict(ZERO_COUNTS)
    
    counts = dict(ZERO_COUNTS)
    
    results_custom = model_custom(frame, verbose=False, conf=0.3)
    
    
    for r in results_custom:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            
            
            if cls_id == CUSTOM_RICKSHAW_ID:
                counts['light'] += 1
                color = (0, 0, 255) 
                
               
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"Auto-Rikshaw: {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    
    results_coco = model_coco(frame, verbose=False, conf=0.4) 

    
    for r in results_coco:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label_name = "Other"
            color = (255, 255, 255)
            
            if cls_id in HEAVY_CLASSES_COCO:
                counts['heavy'] += 1
                color = (0, 255, 255) # Cyan
                label_name = "Bus/Truck (H)"
            elif cls_id in MEDIUM_CLASSES_COCO:
                counts['medium'] += 1
                color = (0, 165, 255) # Orange
                label_name = "Car (M)"
            elif cls_id in LIGHT_CLASSES_COCO:
                counts['light'] += 1 
                color = (0, 0, 255) # Red
                label_name = "2W/Bicycle (L)"
            else:
                continue 
            
            if label_name != "Other":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"{label_name}: {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
    return counts


def calculate_time(counts):
    """Calculates weighted green time based ONLY on tiered VEHICLE counts."""
    
    weighted_time = (counts['heavy'] * TIME_HEAVY) + \
                    (counts['medium'] * TIME_MEDIUM) + \
                    (counts['light'] * TIME_LIGHT)
    
    weighted_time = min(weighted_time, MAX_GREEN_TIME) 
    
    total_time = FIXED_BASE_TIME + weighted_time
    return int(total_time)

def send_phase_data(direction, green_time, counts):
    """Sends phase data (DIRECTION,GREEN_TIME,VEHICLE_COUNT) via TCP Socket."""
    global client_socket
    if client_socket is None: raise ConnectionError("Client socket is not connected.")

   
    vehicle_count = sum(counts.values()) 
    
    message = f"{direction},{green_time},{vehicle_count}\n"
    
    try:
        client_socket.sendall(message.encode('utf-8'))
        print(f"-> Sent via TCP: Dir {direction} Duration: {green_time}s (Total Vehicles: {vehicle_count})")
    except socket.error:
        raise ConnectionError("TCP connection to ESP32 lost.")



def main():
    if not setup_server():
        return
        
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened(): 
        print("FATAL ERROR: Could not open video source.")
        if client_socket: client_socket.close()
        return

    print("Starting Smart Traffic Controller (TCP/IP Mode - DUAL MODEL: Vehicles Only)...")

    
    WINDOW_NAME = "Smart Traffic Monitor (Active Detection - Vehicles Only)"
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL) 
    
    try:
        
        ret, frame = cap.read()
        if ret:
            vehicle_counts['N'] = detect_vehicles(frame)

        while True:
            for i in range(len(DIRECTIONS)):
                current_dir = DIRECTIONS[i]
                next_dir = DIRECTIONS[(i + 1) % len(DIRECTIONS)]

                
                current_counts = vehicle_counts[current_dir]
                green_time = calculate_time(current_counts)
                
                send_phase_data(current_dir, green_time, current_counts) 
                
                
                total_wait_duration = green_time + YELLOW_TIME
                wait_start_time = time.time()
                current_next_counts = dict(ZERO_COUNTS) 
                
                while time.time() - wait_start_time < total_wait_duration:
                    
                    ret, frame = cap.read()
                    if not ret: 
                        time.sleep(0.05)
                        continue
                    
                    
                    current_next_counts = detect_vehicles(frame)
                    
                    current_next_count_total = sum(current_next_counts.values()) 

                    
                    elapsed_time = time.time() - wait_start_time
                    GREEN_END = green_time
                    YELLOW_END = GREEN_END + YELLOW_TIME
                    
                    if elapsed_time < GREEN_END:
                        current_light = "GREEN"
                        timer_color = (0, 255, 0)
                        remaining_s = GREEN_END - elapsed_time
                    elif elapsed_time < YELLOW_END:
                        current_light = "YELLOW"
                        timer_color = (0, 255, 255)
                        remaining_s = YELLOW_END - elapsed_time
                    else:
                        current_light = "RED"
                        timer_color = (0, 0, 255)
                        remaining_s = 0

                    remaining_s = max(0, remaining_s)
                    
                    display_frame = frame 
                    
                    
                    timer_text = f"ACTIVE ({current_dir}): {current_light} {math.ceil(remaining_s)}s (Calc Time: {green_time}s)"
                    scan_text_total = f"Scanning {next_dir} | Total Vehicles: {current_next_count_total}"
                    
                    
                    scan_text_breakdown = (
                        f"H(Bus/Truck):{current_next_counts['heavy']} "
                        f"M(Car):{current_next_counts['medium']} "
                        f"L(2W/Rikshaw/Bicycle):{current_next_counts['light']}"
                    )
                    
                    
                    cv2.putText(display_frame, timer_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, timer_color, 2)
                    cv2.putText(display_frame, scan_text_total, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.putText(display_frame, scan_text_breakdown, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2) # Cyan color for vehicles
                    
                    cv2.imshow(WINDOW_NAME, display_frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        raise StopIteration
                    
                    time.sleep(0.005)

                
                vehicle_counts[next_dir] = current_next_counts
                print(f"Completed cycle for {current_dir}. Next lane ({next_dir}) Green time set by weighted vehicle count.")
            
    except StopIteration:
        pass
    except ConnectionError:
        print("\nDisconnected from ESP32. Check Wi-Fi and ESP32 code. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if client_socket:
            client_socket.close()
        if cap and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        print("Program closed.")

if __name__ == "__main__":
    main()
