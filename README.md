# Feed My Pet

A project created for the Internet of Things course in the Computer Engineering curriculum at the University of Salerno.
This project utilizes a Zerynth ESP32 microcontroller, which connects to a servo motor, a proximity sensor, and an OLED display.

## Key Features:
- Automatic Feeding Mechanism: The feeder releases a portion of food when the proximity sensor detects the presence of a pet nearby. This ensures that pets are fed only when they are close to the feeder, preventing overfeeding and waste.
- User-Controlled Settings: Pet owners can set the maximum daily food portion via a dedicated application developed for PC. This feature allows for personalized feeding schedules tailored to each pet's dietary needs.
- Manual Dispensing Option: In addition to automatic feeding, users can manually dispense food at any time through the app, providing flexibility for varying pet needs.
- Real-Time Monitoring: The OLED display provides essential information, including the number of food portions remaining and the timestamp of the last feeding. This allows owners to keep track of their pet's feeding habits easily.

## Technical Components:
- Zerynth ESP32: Acts as the central controller, managing communication between sensors and the user interface.
- Servo Motor: Responsible for dispensing food accurately when activated by the proximity sensor or user command.
- Proximity Sensor: Detects when a pet is near the feeder, triggering the food dispensing mechanism.
OLED Display: Displays real-time information about food portions and feeding times.
