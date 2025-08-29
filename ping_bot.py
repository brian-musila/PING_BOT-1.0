import requests
import time
import winsound
import tkinter as tk
import threading
import datetime
import webbrowser

# ----------------------------
# CONFIGURATION
# ----------------------------
URL = "https://example.com"   # Replace with the site you want to monitor
LOG_FILE = "site_status_log.txt"
CHECK_INTERVAL = 3600  # seconds (default = 1 hour)


# ----------------------------
# Logging function
# ----------------------------
def log_status(status: str):
    """Append a status update with timestamp into the log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {status}\n")


# ----------------------------
# Alert popup function
# ----------------------------
def alert_window():
    """Show alert window with flashing green background and sound."""
    root = tk.Tk()
    root.title("🚨 Site is UP! 🚨")
    root.geometry("400x200+50+50")  # Position: top-left corner
    root.resizable(False, False)
    root.attributes("-topmost", True)  # Keep on top

    label = tk.Label(
        root,
        text="✅ The site is finally UP!",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="green"
    )
    label.pack(expand=True, fill="both")

    # Clickable link
    def open_link(event=None):
        webbrowser.open(URL)

    link = tk.Label(
        root,
        text="🔗 Open Website",
        font=("Arial", 14, "underline"),
        fg="cyan",
        bg="black",
        cursor="hand2"
    )
    link.pack(pady=10)
    link.bind("<Button-1>", open_link)

    # Animate link click
    def on_enter(event):
        link.config(fg="yellow")
    def on_leave(event):
        link.config(fg="cyan")

    link.bind("<Enter>", on_enter)
    link.bind("<Leave>", on_leave)

    # Flashing background
    def flash_bg(count=0):
        colors = ["green", "black"]
        label.config(bg=colors[count % 2])
        if count < 60:  # ~30 seconds
            root.after(500, flash_bg, count + 1)
        else:
            root.destroy()

    flash_bg()

    # Play sound in background
    def play_sound():
        for _ in range(30):  # ~30 seconds
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            time.sleep(1)

    threading.Thread(target=play_sound, daemon=True).start()

    root.mainloop()


# ----------------------------
# Main monitor function
# ----------------------------
def check_site_forever():
    """Continuously check the site until it is UP."""
    while True:
        try:
            response = requests.get(URL, timeout=10)
            if response.status_code == 200:
                log_status("✅ Site is UP!")
                alert_window()
                break  # stop after site is up
            else:
                log_status(f"❌ Site returned {response.status_code}")
        except Exception as e:
            log_status(f"⚠️ Error: {e}")

        time.sleep(CHECK_INTERVAL)


# ----------------------------
# Run script
# ----------------------------
if __name__ == "__main__":
    log_status("🔍 Monitoring started...")
    check_site_forever()
