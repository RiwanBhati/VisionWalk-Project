# VisionWalk - Smart Glasses for Visually Impaired Navigation

**VisionWalk is a university project aimed at developing smart glasses to assist visually impaired individuals with barrier-free navigation. This system uses a Raspberry Pi Zero W and an ultrasonic sensor to detect obstacles and provide real-time auditory feedback.**

---


 ![VisionWalk Prototype](https://github.com/RiwanBhati/VisionWalk-Project/blob/84fbc4ac6de1cd358c02a8b25d8a15cc777efcfe/VisionWalk%20Prototype.jpg) -->

---

## 🌟 Project Overview

Navigating independently can be a significant challenge for visually impaired individuals, often leading to accidents. VisionWalk aims to mitigate these risks by providing a wearable, cost-effective solution for obstacle detection. The smart glasses alert the user to nearby obstructions through auditory cues, enhancing their spatial awareness and safety.

This project was developed as part of the second-semester curriculum at BML Munjal University and was presented at the TechSparX event.

##  Demo

Watch VisionWalk in action:
▶️ [VisionWalk Demonstration Video](https://youtu.be/lfVLQecjdlI?si=va1neLF8wA3mukE1)

## 🛠️ Features

*   **Real-time Obstacle Detection:** Uses an HC-SR04 ultrasonic sensor to detect obstacles.
*   **Auditory Feedback:** Provides immediate alerts via a buzzer.
*   **Wearable Design:** Built onto a glasses frame.
*   **Raspberry Pi Powered:** Utilizes a Raspberry Pi Zero W.
*   **Cost-Effective:** Designed with affordable components.

## ⚙️ Hardware Components

*   Raspberry Pi Zero W
*   HC-SR04 Ultrasonic Sensor
*   Piezo Buzzer
*   Resistors
*   Jumper Wires
*   MicroSD Card
*   Portable Power Source (e.g., USB Power Bank)
*   Glasses Frame

## 💻 Software & Prerequisites

*   **Operating System:** Raspberry Pi OS
*   **Programming Language:** Python 3
*   **Key Python Libraries:** `RPi.GPIO`, `time`

## 🏗️ Setup & Installation

1.  **Hardware Assembly:**
    *   Assemble the circuit (see circuit diagram).
    *   Mount components on the glasses frame.

2.  **Software Setup on Raspberry Pi:**
    *   Flash Raspberry Pi OS onto MicroSD card.
    *   Ensure Python 3 and `RPi.GPIO` library are installed.
        ```bash
        # To install RPi.GPIO if needed:
        # sudo apt-get update
        # sudo apt-get install python3-rpi.gpio
        ```
    *   Download or clone the Python script (`visionwalk.py`) to your Raspberry Pi.

## 🚀 Usage

1.  Connect hardware and power on the Raspberry Pi.
2.  Navigate to the script's directory.
3.  Run:
    ```bash
    python3 visionwalk.py
    ```
    *(Replace `visionwalk.py` with your script's name if different)*
    The buzzer will sound when obstacles are detected.

## 📊 Diagrams

*   **Block Diagram:**
   ![Block Diagram](https://github.com/RiwanBhati/VisionWalk-Project/blob/13782343075eac043d2674f0d0ffcf255087fd40/VisionWalk%20Block%20diagram.jpg)

*   **Circuit Diagram:**
   ![Circuit Diagram](https://github.com/RiwanBhati/VisionWalk-Project/blob/e72d2dda05afc9429569cb557166ae07c12a66e0/Visionwalk%20Circuit%20diagram.pdf)

## 📄 Project Documentation

For more details (full report, presentation, etc.):
🔗 [VisionWalk Full Project Documentation (Google Drive)](https://drive.google.com/drive/folders/1yjPgEbyaSdTwBvtd94TVTjnZGKU2oxyp?usp=sharing)

## 💡 Future Scope

*   Directional feedback and varied alert patterns.
*   Improved ergonomics and compact design.
*   Advanced sensors (e.g., LiDAR, camera for basic object recognition).
*   Mobile app integration.

## 🤝 Contributing 

This was a personal university project. If you have suggestions or find issues, feel free to open an issue on GitHub.

## 🙏 Acknowledgements

*   BML Munjal University
*   Project Supervisors: Dr. Soharab Hossain, Dr. Shrikant K

## 📞 Contact

Riwan Bhati - www.linkedin.com/in/riwan-bhati-049a44323
