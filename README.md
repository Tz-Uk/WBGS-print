# WBGS print
# Lets you print files to the library printer in full colour, for free!
<!-- NERD STUFF:
The way this works is the printer accepts anonymous printer connections over wifi, thats all it is lol

-->

> **Note:** You must be connected to the **WGSB Wi-Fi** for the app to reach the printer.

---

## Setup

### 1. Install Python (one-time)

- Download it from [python.org/downloads](https://www.python.org/downloads/).
- **Windows:** tick **"Add python.exe to PATH"** at the bottom of the installer before clicking Install.
- **Mac/Linux:** Python 3 is usually already installed. Check with `python3 --version` in Terminal. On some Linux systems you may also need to install Tk (`sudo apt install python3-tk`).

The app also needs **curl**, which is built into Windows 10 (version 1803 or later), Windows 11 and macOS.

### 2. Download the code

1. Open `LibPrint.py` in this repository.
2. Click the **Download raw file** icon (next to the *Raw* button, top-right of the file view).
3. Move `LibPrint.py` somewhere easy, like your Desktop.


### 3. Run it

- **Windows:** double-click `LibPrint.py` (or `LibPrint.pyw`).
- **Mac/Linux:** open Terminal, type `python3 ` (with a space after it), drag `LibPrint.py` into the window, and press Enter.

---

## Using the app

1. **File:** click **Browse…** and choose what you want to print. You can also paste a file path into the box.
2. **Transfer format:** leave it on **Binary** for PDFs, images and most files. Choose **ASCII** only for plain `.txt` files.
3. **Copies:** set how many you want (default is 1).
4. Click **Send to Printer**.

The status line under the button shows progress and turns green when it's done (for example, *"✓ Sent 2 copies of essay.pdf"*). If something goes wrong, it turns red and a short error message appears.

---

## What you can print

**PDF files work best.** Word, PowerPoint and similar files aren't guaranteed to print this way. If you have one of those, export or save it as a PDF first.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| **"File not found"** | Check the path for typos, or use **Browse…** to pick the file instead. |
| **Double-clicking opens Notepad or a text editor, or nothing happens** | Python isn't installed, or the file was saved as `LibPrint.py.txt`. Install Python, check the file extension, then right-click the file and choose **Open with → Python**. |
| **`python` / `python3` is not recognised (Terminal)** | Python isn't installed or wasn't added to PATH. Re-run the installer and tick **"Add python.exe to PATH"**. |
| **"curl is not installed"** | Install curl, or update Windows to 10 (1803) or later. |
| **Connection timed out / failed to connect** | Make sure you're on the WGSB Wi-Fi. The library printer might also be switched off or offline. |
| **Sent successfully but nothing prints, or garbled output** | The printer can't read that file type. Convert it to PDF and try again. |
| **The app window won't open on Linux** | Install Tk: `sudo apt install python3-tk`. |

---

## Licence

Released under the MIT Licence, so you're free to use and change it. It is provided **as is, without warranty of any kind. Use at your own risk.** See the `LICENSE` file for details.

