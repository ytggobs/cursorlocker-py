import tkinter as tk
from threading import Thread
import time
import ctypes
import sys
import os

class CursorLockerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cursor Locker")

        # Global variable to track the cursor lock state
        self.cursor_locked = False

        # Store the original cursor position
        self.original_cursor_pos = (0, 0)

        # Create GUI elements
        self.open_window_label = tk.Label(master, text="Press F7 to toggle visibility.")
        self.open_window_label.pack(pady=(0, 5))

        self.instruction_label = tk.Label(master, text="Press F6 to toggle on and off.")
        self.instruction_label.pack(pady=(0, 5))

        self.button = tk.Button(master, text="Toggle Cursor Lock", command=self.toggle_cursor_lock)
        self.button.pack(pady=10)

        # Label to display "Made with ChatGPT" in grey
        self.made_with_label = tk.Label(master, text="Made with ChatGPT", fg="grey")
        self.made_with_label.pack()

        # Function to check if the F6 key is pressed
        def is_f6_pressed():
            time.sleep(0.1)
            return ctypes.windll.user32.GetKeyState(0x75) & 0x8000 != 0

        # Function to check if the F7 key is pressed
        def is_f7_pressed():
            time.sleep(0.1)
            return ctypes.windll.user32.GetKeyState(0x76) & 0x8000 != 0

        # Function to continuously move the cursor to the center
        def move_cursor_to_center():
            while True:
                if self.cursor_locked:
                    screen_width, screen_height = master.winfo_screenwidth(), master.winfo_screenheight()
                    center_x, center_y = screen_width // 2, screen_height // 2
                    ctypes.windll.user32.SetCursorPos(center_x, center_y)

        # Create a thread for continuous cursor movement
        self.cursor_thread = Thread(target=move_cursor_to_center)
        self.cursor_thread.start()

        # Bind the close event to the close_app method
        master.protocol("WM_DELETE_WINDOW", self.close_app)

        # Start the main loop
        master.after(0, self.check_f6_and_f7_keys)
        master.mainloop()

    def toggle_cursor_lock(self):
        if self.cursor_locked:
            # Unlock the cursor and restore its original position
            self.cursor_locked = False
            ctypes.windll.user32.SetCursorPos(*self.original_cursor_pos)
        else:
            # Lock the cursor and move it to the center of the screen
            self.cursor_locked = True
            screen_width, screen_height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
            center_x, center_y = screen_width // 2, screen_height // 2
            ctypes.windll.user32.SetCursorPos(center_x, center_y)

        print(f"Cursor {'locked' if self.cursor_locked else 'unlocked'}")

    def check_f6_and_f7_keys(self):
        if self.is_f6_pressed():
            self.toggle_cursor_lock()

        if self.is_f7_pressed():
            self.toggle_visibility()

        # Check the F6 and F7 keys every 100 milliseconds
        self.master.after(100, self.check_f6_and_f7_keys)

    def toggle_visibility(self):
        # Toggle window visibility
        if self.master.attributes('-alpha') == 1.0:
            self.master.attributes('-alpha', 0.0)
        else:
            self.master.attributes('-alpha', 1.0)

    def is_f6_pressed(self):
        return ctypes.windll.user32.GetKeyState(0x75) & 0x8000 != 0

    def is_f7_pressed(self):
        return ctypes.windll.user32.GetKeyState(0x76) & 0x8000 != 0

    def close_app(self):
        self.master.destroy()

        # On Windows, close the console using taskkill
        if sys.platform.startswith('win'):
            console_pid = os.getpid()
            os.system(f'taskkill /F /PID {console_pid}')

if __name__ == "__main__":
    master = tk.Tk()
    # Make the window always stay on top
    master.attributes('-topmost', True)
    app = CursorLockerApp(master)
