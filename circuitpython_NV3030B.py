import displayio
import board
import busio
import digitalio
import time

_INIT_SEQUENCE = (
    b"\x36\x01\x08"  # Memory Access Control: Sets the row/column exchange and RGB/BGR order.
    b"\xfd\x02\x06\x08"  # Command Unlock: Unlocks specific command sets.
    b"\x61\x02\x07\x04"  # Display Inversion Control: Sets the inversion parameters.
    b"\x62\x03\x00\x44\x45"  # RGB Interface Signal Control: Configures the RGB interface signals.
    b"\x63\x04\x41\x07\x12\x12"  # Display Function Control: Controls various display functions.
    b"\x64\x01\x37"  # Power Control 1: Sets the power control parameters for the display.
    b"\x65\x03\x09\x10\x21"  # Power Control 2: Additional power control settings.
    b"\x66\x03\x09\x10\x21"  # Power Control 3: Further power control settings.
    b"\x67\x02\x20\x40"  # VCOM Control: Controls the VCOM voltage.
    b"\x68\x04\x90\x4c\x7c\x66"  # Source Driver Timing Control: Sets the timing for the source drivers.
    b"\xb1\x03\x0f\x02\x01"  # Frame Rate Control (Normal Mode): Sets the frame rate for normal display mode.
    b"\xb4\x01\x01"  # Display Inversion Control: Sets the display inversion mode.
    b"\xb5\x04\x02\x02\x0a\x14"  # Blanking Porch Control: Controls the front and back porch settings.
    b"\xb6\x05\x04\x01\x9f\x00\x02"  # Display Function Control: Configures various display functions.
    b"\xdf\x01\x11"  # Power Control 4: Additional power control settings.
    b"\xe2\x06\x13\x00\x00\x30\x33\x3f"  # Gamma Set: Sets the gamma curve parameters.
    b"\xe5\x06\x3f\x33\x30\x00\x00\x13"  # Gamma Set (Reverse): Sets the reverse gamma curve parameters.
    b"\xe1\x02\x00\x57"  # Brightness Control: Sets the brightness level.
    b"\xe4\x02\x58\x00"  # CABC Control: Controls the Content Adaptive Brightness Control (CABC) settings.
    b"\xe0\x07\x01\x03\x0e\x0e\x0c\x15\x19"  # Positive Voltage Gamma Control: Sets the positive voltage gamma curve.
    b"\xe3\x08\x1a\x16\x0c\x0f\x0e\x0d\x02\x01"  # Negative Voltage Gamma Control: Sets the negative voltage gamma curve.
    b"\xe6\x02\x00\xff"  # Panel Control: Controls panel-related settings.
    b"\xe7\x06\x01\x04\x03\x03\x00\x12"  # Panel Timing Control: Sets the timing parameters for the panel.
    b"\xe8\x03\x00\x70\x00"  # Display Off: Turns the display off with specific parameters.
    b"\xec\x01\x52"  # Set Panel Timing: Configures specific panel timing parameters.
    b"\xf1\x03\x01\x01\x02"  # Power Control 5: Additional power control settings.
    b"\xf6\x04\x09\x10\x00\x00"  # Interface Control: Interface-related control settings.
    b"\xfd\x02\xfa\xfc"  # Command Unlock: Unlocks specific command sets.
    b"\x3a\x01\x05"  # Pixel Format Set: Sets the pixel format.
    b"\x35\x01\x00"  # Tearing Effect Line ON: Enables the tearing effect line.
    b"\x21\x00"  # Display Inversion ON: Enables display inversion.
    b"\x11\x80\xc8"  # Sleep Out: Exits sleep mode with a delay of 200ms (0xc8).
    b"\x29\x80\x0a"  # Display ON: Turns the display on with a delay of 10ms (0x0a).
)

class NV3030B(displayio.Display):
    """NV3030B driver"""

    def __init__(
            self, 
            clk: board.PIN,
            mosi: board.PIN,
            cs: board.PIN,
            dc: board.PIN,
            rst: board.PIN,
            **kwargs
        ) -> None:
        # reset the display before initializing according to the datasheet
        reset = digitalio.DigitalInOut(rst)
        reset.direction = digitalio.Direction.OUTPUT
        reset.value = True
        time.sleep(0.01)
        reset.value = False
        time.sleep(0.01)
        reset.value = True
        time.sleep(0.05)

        spi = busio.SPI(
            clock= clk, 
            MOSI= mosi
        )
        display_bus = displayio.FourWire(
            spi,
            command=dc,
            chip_select=cs,
            reset=rst
        )
        super().__init__(
            display_bus,
            _INIT_SEQUENCE,
            **kwargs,
            set_column_command=0x2A,
            set_row_command=0x2B,
            write_ram_command=0x2C,
        )