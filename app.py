import streamlit as st
import serial
import serial.tools.list_ports
import time

# --- Helper Functions ---

@st.cache_data
def find_serial_devices():
    """Scans for and returns a list of available serial devices."""
    # Use list_ports to get a list of all available serial ports
    ports = serial.tools.list_ports.comports()
    # Return the device path for each port
    return [port.device for port in ports if port.device.startswith("/dev/ttyACM")]

def send_color_to_arduino(connection, r, g, b):
    """Formats and sends the RGB color data to the Arduino."""
    if connection and connection.is_open:
        # Create a command string, e.g., "255,100,50\n"
        command = f"{r},{g},{b}\n"
        try:
            connection.write(command.encode('utf-8'))
            return True
        except serial.SerialException as e:
            st.error(f"Failed to send data: {e}")
            return False
    return False

def hex_to_rgb(hex_color):
    """Converts a hex color string (e.g., '#RRGGBB') to an (R, G, B) tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """Converts an (R, G, B) tuple to a hex color string."""
    return f'#{r:02x}{g:02x}{b:02x}'

# --- Streamlit App ---

st.set_page_config(page_title="RGB LED Controller", layout="wide")

st.title("💡 Real-time RGB LED Controller")

# Initialize session state variables
if 'serial_connection' not in st.session_state:
    st.session_state.serial_connection = None
if 'last_sent_color' not in st.session_state:
    st.session_state.last_sent_color = None

# --- Sidebar for Connection Management ---
with st.sidebar:
    st.header("⚙️ Connection")
    available_devices = find_serial_devices()

    if not available_devices:
        st.warning("No serial devices found. Connect a device and refresh.")
    else:
        selected_device = st.selectbox("Select Device", options=available_devices)

        if st.session_state.serial_connection:
            st.success(f"Connected to **{st.session_state.serial_connection.port}**")
            if st.button("Disconnect"):
                st.session_state.serial_connection.close()
                st.session_state.serial_connection = None
                st.rerun()
        else:
            if st.button("Connect"):
                try:
                    # Establish connection
                    ser = serial.Serial(selected_device, 9600, timeout=1)
                    time.sleep(2) # Wait for Arduino to reset after connection
                    st.session_state.serial_connection = ser
                    st.rerun()
                except serial.SerialException as e:
                    st.error(f"Failed to connect: {e}")

# --- Main Interface for Color Control ---
if st.session_state.serial_connection:
    st.header("🎨 Color Controls")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Color Preview")

        # This empty element will be our color box
        color_box = st.empty()

        st.subheader("HSL Color Picker")
        # The color picker is the primary source of color change
        hex_color = st.color_picker("Choose a color with the picker", '#000000')
        r, g, b = hex_to_rgb(hex_color)

    with col2:
        st.subheader("RGB Sliders")
        # The sliders are controlled by the color picker's state
        r_val = st.slider("Red", 0, 255, r)
        g_val = st.slider("Green", 0, 255, g)
        b_val = st.slider("Blue", 0, 255, b)

    # Update the color preview box
    final_hex = rgb_to_hex(r_val, g_val, b_val)
    color_box.markdown(
        f"""
        <div style="
            width: 100%;
            height: 200px;
            background-color: {final_hex};
            border: 2px solid #ccc;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
            color: {'black' if (r_val*0.299 + g_val*0.587 + b_val*0.114) > 186 else 'white'};
        ">
            {final_hex.upper()}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Logic to send data ---
    # Only send data if the color has actually changed
    current_color = (r_val, g_val, b_val)
    if current_color != st.session_state.last_sent_color:
        if send_color_to_arduino(st.session_state.serial_connection, r_val, g_val, b_val):
            st.session_state.last_sent_color = current_color
            # A subtle success message in the sidebar can be nice
            st.sidebar.markdown(f"Sent: `{current_color}`")
        else:
            # If sending fails, close the connection
            st.session_state.serial_connection.close()
            st.session_state.serial_connection = None
            st.rerun()

else:
    st.info("Please connect to a serial device from the sidebar to begin.")
