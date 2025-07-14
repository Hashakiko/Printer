import usb.core
import usb.util
import usb.backend.libusb1 as libusb1
from escpos.printer import Usb

# --- CONFIGURATION ---
VID = 0x28E9    # Verify with Zadig/USBDeview
PID = 0x0289    # Verify with Zadig/USBDeview
IN_EP = 0x81    # Usually 0x81 for bulk IN
OUT_EP = 0x01   # Usually 0x01 for bulk OUT
TIMEOUT = 1000  # Timeout in ms

def connect_printer():
    backend = libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll")
    if backend is None:
        print("ERROR: libusb-1.0.dll not found. Place it in:")
        print("  - Script folder")
        print("  - Or C:\Windows\System32")
        return None

    try:
        printer = Usb(VID, PID, in_ep=IN_EP, out_ep=OUT_EP, timeout=TIMEOUT, backend=backend)
        if hasattr(printer, 'profile'):
            printer.profile.raise_exception = False
        print("Printer connected successfully!")
        return printer
    except usb.core.USBError as e:
        print(f"USB ERROR: {e}")
        print("Try: Replug printer, run as Admin, or check Zadig")
    except Exception as e:
        print(f"GENERAL ERROR: {e}")
    return None

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    printer = connect_printer()
    if printer:
        try:
            # Print ONLY the device specs (left-aligned)
            printer.set(align='left', width=1, height=1)  # Set alignment once
            printer.text("Device: Asus Laptop\n")
            printer.text("GPU: RTX 3060\n")
            printer.text("Price: $200\n")
            printer.text("\n\n\n")  # Feed paper
            printer.cut()
            print("Label printed successfully!")
        except Exception as e:
            print(f"PRINT ERROR: {e}")
        finally:
            usb.util.dispose_resources(printer.device)
    else:
        print("Printer not connected. See errors above.")