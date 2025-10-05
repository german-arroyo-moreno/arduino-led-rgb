# 💡 Real-time Arduino RGB LED Controller

[](https://www.python.org/)
[](https://streamlit.io)
[](https://pyserial.readthedocs.io/en/latest/)

A web-based controller to manage the color of an RGB LED connected to an Arduino in real-time. This project uses Python with the **Streamlit** framework to create an interactive user interface and **pySerial** to communicate with the Arduino board.

The web app automatically detects available serial devices, allowing you to connect, select any color from a beautiful color picker, and see your physical LED change instantly.

-----

### \#\# 📸 App Preview

*(Here you can add a screenshot or GIF of the application in action)*
`![App Screenshot](./img/app-screenshot.png)`

-----

### \#\# ✨ Features

  * **Interactive Web Interface:** Modern UI built with Streamlit that can be accessed from your browser.
  * **Auto-Device Discovery:** Automatically scans and lists available serial ports (e.g., `/dev/ttyACM0` on Linux).
  * **Dual Color Selection:** Choose a color using an intuitive HSL color picker or fine-tune it with precise RGB sliders.
  * **Real-time Color Preview:** A visual box in the app displays the currently selected color and its hex code.
  * **Instantaneous Control:** Color data is sent to the Arduino as soon as you change it, for immediate physical feedback.
  * **Simple Connection Management:** Easy connect and disconnect buttons with clear status indicators.

-----

### \#\# 🛠️ Requirements

#### Hardware

  * An Arduino board (e.g., Arduino Uno, Nano)
  * A common-cathode RGB LED
  * 3 x 220Ω resistors
  * A breadboard and jumper wires
  * A USB cable to connect the Arduino to your computer

#### Software

  * [Python 3.8+](https://www.python.org/downloads/)
  * [Arduino IDE](https://www.arduino.cc/en/software)
  * The following Python libraries: `streamlit`, `pyserial`

-----

### \#\# 🚀 Setup and Installation

Follow these steps to get the project up and running.

#### **Step 1: Clone the Repository**

Open your terminal and clone this project.

```bash
git clone https://github.com/your-username/your-project-name.git
cd your-project-name
```

#### **Step 2: Hardware Setup**

Assemble the circuit as shown below. Connect the three anode (longer) pins of the LED to the resistors, which then connect to the Arduino's digital PWM pins. Connect the cathode (longest) pin to GND.

  * LED Red Pin → 220Ω Resistor → **Pin 9** on Arduino
  * LED Green Pin → 220Ω Resistor → **Pin 10** on Arduino
  * LED Blue Pin → 220Ω Resistor → **Pin 11** on Arduino
  * LED Ground (Cathode) Pin → **GND** on Arduino

#### **Step 3: Upload the Arduino Sketch**

1.  Open the `led_controller/led_controller.ino` file in the Arduino IDE.
2.  Connect your Arduino board to your computer via USB.
3.  In the IDE, select your board (e.g., *Tools \> Board \> Arduino Uno*) and the correct port (*Tools \> Port*).
4.  Click the "Upload" button.

#### **Step 4: Set Up the Python Environment**

It's highly recommended to use a Python virtual environment.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate

# Or activate it (Windows)
# .venv\Scripts\activate

# Install the required packages
pip install streamlit pyserial
```

##### **A Note for Linux Users - Serial Port Permissions**

On Linux, you need permission to access serial ports. Running the script will likely result in a "Permission Denied" error if you don't configure this. You have two options:

1.  **Recommended Method: Add Your User to the `dialout` Group**

    This is the best and most secure method. It grants your user account permanent access to serial ports.

    Open a terminal and run the following command:

    ```bash
    sudo usermod -aG dialout $USER
    ```

    **Important:** You must **log out and log back in** for this change to take effect.

2.  **Temporary Method: Run as Root**

    You can run the script using `sudo` to give it root privileges for a single session. This is a quick fix but is not generally recommended for security reasons.

    ```bash
    sudo streamlit run app.py
    ```

-----

#### **Step 5: Run the Streamlit App**

With your virtual environment activated, run the following command in your terminal:

```bash
streamlit run app.py
```

Your default web browser will automatically open with the controller interface.

-----

### \#\# 🕹️ How to Use

1.  **Select Your Device:** In the sidebar on the left, choose your Arduino from the dropdown menu.
2.  **Connect:** Click the "Connect" button. The status will change to "Connected" upon success.
3.  **Choose a Color:**
      * Use the **HSL Color Picker** for a quick and easy selection.
      * Use the **RGB Sliders** for precise, granular control.
4.  **Observe:** Your physical RGB LED will change color in real-time to match your selection.
5.  **Disconnect:** When you're finished, click the "Disconnect" button in the sidebar.

-----

### \#\# 🔧 Troubleshooting

  * **No devices found:** Ensure your Arduino is properly connected to your computer. If you're on Linux, your user might not have permission to access the serial port. Run `sudo usermod -a -G dialout $USER` and then log out and log back in.
  * **LED colors are inverted:** This usually means you have a **common-anode** RGB LED instead of a common-cathode one. To fix this, open the Arduino `.ino` sketch and modify the `setColor` function to invert the values:
    ```cpp
    void setColor(int r, int g, int b) {
      analogWrite(RED_PIN, 255 - r);
      analogWrite(GREEN_PIN, 255 - g);
      analogWrite(BLUE_PIN, 255 - b);
    }
    ```
    Then, re-upload the sketch to your Arduino.

-----

### \#\# 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
