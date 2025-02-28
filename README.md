LANE TRACKİNG SYSTEM

Description

This project implements a Lane Tracking System using OpenCV. The system detects and tracks lane markings on the road, guiding the vehicle to stay within the correct lane. It works by analyzing the road's edges, detecting lane lines, and determining whether the vehicle needs to turn left or right, or go straight.

Features:
- Lane detection using Hough Transform
- Dynamic lane following logic based on the vehicle's position within the lane
- Ability to handle sharp turns and maintain lane stability
- Real-time video processing for vehicle guidance

How to Use:
1. Clone or download the repository to your local machine.
2. Ensure you have the required dependencies installed (see below).
3. Run the Lane_Tracking_System.py script to begin lane tracking.
4. The system will process the video and display the detected lane and the vehicle's current direction (e.g., "Turn left", "Go straight", or "Turn right").

Dependencies:
- OpenCV (for image processing and video manipulation)
- Numpy (for numerical operations)

You can install the required libraries using pip:
- pip install opencv-python numpy

Example Video:
- You can watch the result video of the lane tracking system here: https://drive.google.com/file/d/1e_MF0u9tM_CmEbJQJ3imbosI0Lmuh-b8/view?usp=sharing
- Additionally, if you'd like to experiment with the same video used in the project, you can download it here: https://drive.google.com/file/d/1tD4gUrlxqKey6m29MjTTZt9fQ11-sq8O/view?usp=sharing

Notes:
- The project uses a sample video for lane tracking, but you can replace it with any road video to test the system's effectiveness.
- You might want to adjust parameters depending on the specific video or road conditions.
  

Improvements: 

There might be some inaccuracies in the calculations, but this project is open for further development and improvements. If you would like to contribute, feel free to submit issues or pull requests.


License:

This project is licensed under the MIT License.
