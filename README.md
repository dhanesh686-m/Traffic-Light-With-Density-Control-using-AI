# Traffic Light with Density Control using AI

This project implements an intelligent traffic management system that uses computer vision and an AI model to dynamically control a 4-way traffic light system. By analyzing real-time traffic density, the system adjusts the green light duration for each lane, aiming to reduce congestion and improve overall traffic flow.

## Project Components

This project consists of two main parts: the software for vehicle detection and the hardware for traffic light control.

### Software (Python)

The Python script (`4-way-traffic-light-integrated-with-arduino.py` and `1-way-traffic-light-not-integrated.py`) handles the video analysis and traffic density calculation.

* Vehicle Detection: The script uses the `ultralytics` library with a pre-trained **YOLOv8** model (`yolov8n.pt`) to detect vehicles from live video feeds. It is configured to identify cars, motorcycles, buses, and trucks based on the COCO dataset classes.
* Video Feeds: The system is designed to handle four separate camera feeds, one for each lane (North, South, East, and West).
* Dynamic Timing: The script calculates the green light duration for each lane based on a fixed base time and an additional time per detected vehicle.
* Hardware Communication**: The script establishes a network connection to a microcontroller (e.g., ESP32) to send commands for controlling the traffic lights.

### Hardware (Microcontroller)

The microcontroller, likely an **ESP32**, runs the `ESP32_Traffic_Control.ino` code.

* Network Server: The ESP32 acts as a server, listening for commands from the Python script over Wi-Fi.
* Traffic Light Control: It receives commands containing the lane direction and the desired green light duration, then controls the physical traffic lights accordingly. The circuit diagram for the traffic light system is provided in `traffic light signal ckt.pdf`.

## How It Works

1.  Start-up: The Python script initializes and connects to the ESP32 over a Wi-Fi network.
2.  Video Capture: The script captures real-time video feeds from the cameras at each intersection lane.
3.  Vehicle Counting: Using the YOLOv8 model, it detects and counts the number of vehicles in each lane.
4.  Time Calculation: An algorithm calculates the optimal green light duration for each lane based on the vehicle count.
5.  Signal Control: The script sends a command to the ESP32 with the lane direction and the calculated green light duration.
6.  Loop: This process is repeated in a continuous loop, allowing the system to adapt to changing traffic conditions in real-time.

## Project Structure

 `4-way-traffic-light-integrated-with-arduino.py`: The main Python script for the 4-way traffic light system.
 `1-way-traffic-light-not-integrated.py`: A Python script for a 1-way traffic light system.
 `ESP32_Traffic_Control.ino`: The Arduino IDE sketch for the ESP32 microcontroller that controls the traffic lights.
 `traffic light signal ckt.pdf`: A PDF document containing the circuit diagram for the traffic light system.
 `yolov8n.pt`: The pre-trained YOLOv8 model weights used for vehicle detection.

## Requirements

### Hardware
 An ESP32 microcontroller
 Traffic lights (LEDs) for a 4-way intersection
 Jumper wires and resistors
 Four cameras (e.g., webcams or dedicated traffic cameras)
 A computer to run the Python script

### Software
 Python 3.x
 `OpenCV`
 `ultralytics`
 `pyserial` (or other library for socket communication)
 Arduino IDE for flashing the ESP32
  
## Setup Instructions

1.  Hardware Setup: Assemble the traffic light circuit according to the provided `traffic light signal ckt.pdf`.
2.  ESP32: Flash the `ESP32_Traffic_Control.ino` sketch onto your ESP32 board using the Arduino IDE. Ensure the ESP32 is connected to the same Wi-Fi network as your computer.
3.  Python Script:
     Install the required Python libraries using pip.
     Update the `HOST` variable in `4-way-traffic-light-integrated-with-arduino.py` with the IP address of your ESP32.
     Place the `yolov8n.pt` model file in the same directory as the Python script.
4.  Run: Execute the Python script to start the traffic management system.
