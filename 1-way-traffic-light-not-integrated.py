import cv2
import time
from ultralytics import YOLO

# --- Configuration ---
CAMERA_INDEX = 0

# --- AI Model Setup ---
model = YOLO('yolov8n.pt')
VEHICLE_CLASSES = [2, 3, 5, 7]

# --- Main Program ---
def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    print("Camera feed started. Press 'q' to quit.")

    try:
        while True:
            # --- PHASE 1: Traffic Detection and Time Calculation ---
            print("\nScanning traffic...")
            scan_start_time = time.time()
            vehicle_count = 0

            while time.time() - scan_start_time < 5:
                ret, frame = cap.read()
                if not ret:
                    break
                
                results = model(frame, verbose=False)
                current_frame_count = sum(1 for r in results for c in r.boxes.cls if int(c) in VEHICLE_CLASSES)
                if current_frame_count > vehicle_count:
                    vehicle_count = current_frame_count

                cv2.imshow("Traffic Monitor", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return

            # --- PHASE 2: Logic and Green Light Countdown ---
            if vehicle_count > 10:
                green_time = 30
            elif vehicle_count > 5:
                green_time = 15
            else:
                green_time = 5

            print(f"Detected {vehicle_count} vehicles. Green light time: {green_time}s")
            print(f"🚦 Green Light ON...")

            for i in range(green_time, 0, -1):
                print(f"Time remaining: {i} seconds", end='\r', flush=True)
                time.sleep(1)
            print("                                    ", end='\r', flush=True) # Clear line

            # --- PHASE 3: Yellow and Red Light Countdown ---
            print(f"🟡 Yellow Light ON...")
            yellow_time = 2
            for i in range(yellow_time, 0, -1):
                print(f"Time remaining: {i} seconds", end='\r', flush=True)
                time.sleep(1)
            print("                                    ", end='\r', flush=True)

            print(f"🔴 Red Light ON...")
            red_time = 5
            for i in range(red_time, 0, -1):
                print(f"Time remaining: {i} seconds", end='\r', flush=True)
                time.sleep(1)
            print("                                    ", end='\r', flush=True)

            print("Cycle finished. Starting a new scan.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Program closed.")

if __name__ == "__main__":
    main()