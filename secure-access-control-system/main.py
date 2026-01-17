import tkinter as tk
from tkinter import simpledialog, messagebox

# App logic imports
import logic
from models.user import User, init_db
from logic.card import VirtualCard
from logic.otp import generate_otp_cloud
from logic.pin_train import build_pin_train, extract_pin_from_train

# Servers
from servers.server_base import Server
from servers.server3 import server3  # Server 3 wrapper (manages Zone 3 by default)

# Create base servers
server1 = Server(name="Server 1", managed_zones=[1])
server2 = Server(name="Server 2", managed_zones=[2])
# server3 is imported above

# ---------------------------
# Globals & helpers
# ---------------------------
log_messages = []
card_instance = None

def log(message, tag="normal"):
    log_box.insert(tk.END, message + "\n", tag)
    log_box.see(tk.END)

def update_card_display():
    if not card_instance:
        return
    state = card_instance.get_state()
    content = (
        f"USER ID: {card_instance.user_id}\n"
        f"SCAN COUNT: {state['scan_count']}\n"
        f"CURRENT X: {state['x']}\n"
        f"AUTHORIZED ZONE: {state['zone_level']}\n"
        f"LOCKED: {state['locked']}"
    )
    card_display.config(state="normal")
    card_display.delete("1.0", tk.END)
    card_display.insert(tk.END, content)
    card_display.config(state="disabled")

def update_server_display(server_name, data):
    if server_name == "Server 1":
        display = server1_display
    elif server_name == "Server 2":
        display = server2_display
    else:
        display = server3_display  # Server 3

    display.config(state="normal")
    display.delete("1.0", tk.END)

    content = (
        f"SERVER: {data['name']}\n"
        f"ZONE: {data['managed_zones']}\n"
        f"USER ID: {data.get('user_id', 'N/A')}\n"
        f"SCAN COUNT: {data.get('scan_count', 'N/A')}\n"
        f"X USED: {data.get('x_used', 'N/A')}\n"
        f"NEXT X: {data.get('next_x', 'N/A')}\n"
        f"PIN VALID: {data.get('pin_valid', 'N/A')}\n"
        f"OTP VALID: {data.get('otp_valid', 'N/A')}\n"
        f"STATUS: {data.get('status', 'N/A')}"
    )

    display.insert(tk.END, content)
    display.config(state="disabled")

def get_server_for_zone(zone_number: int):
    """Return the active server currently managing the zone (auto-failover compatible)."""
    for srv in (server1, server2, server3):
        if getattr(srv, "is_active", True) and zone_number in getattr(srv, "managed_zones", []):
            return srv
    return None

# ---------------------------
# Dialogs
# ---------------------------
def show_pin_input():
    """Custom PIN input window."""
    pin_window = tk.Toplevel(root)
    pin_window.title("PIN")
    pin_window.geometry("300x150")
    pin_window.transient(root)
    pin_window.grab_set()

    tk.Label(pin_window, text="Enter your 4-digit PIN:", font=("Helvetica", 12)).pack(pady=10)
    pin_entry = tk.Entry(pin_window, show="*", font=("Courier", 14), width=20)
    pin_entry.pack(pady=5)

    result = {"value": None}

    def on_submit():
        result["value"] = pin_entry.get()
        pin_window.destroy()

    tk.Button(pin_window, text="Submit", command=on_submit).pack(pady=10)
    root.wait_window(pin_window)
    return result["value"]

def show_otp_input(expected_otp):
    """Shows the expected OTP (for testing)."""
    otp_window = tk.Toplevel(root)
    otp_window.title("OTP")
    otp_window.geometry("300x150")
    otp_window.transient(root)
    otp_window.grab_set()

    tk.Label(otp_window, text=f"Enter the displayed OTP:", font=("Helvetica", 12)).pack(pady=10)
    tk.Label(otp_window, text=f"OTP: {expected_otp}", font=("Courier", 14, "bold"), fg="blue").pack(pady=5)

    otp_entry = tk.Entry(otp_window, font=("Courier", 14), width=20)
    otp_entry.pack(pady=5)

    result = {"value": None}

    def on_submit():
        result["value"] = otp_entry.get()
        otp_window.destroy()

    tk.Button(otp_window, text="Submit", command=on_submit).pack(pady=10)
    root.wait_window(otp_window)
    return result["value"]

def show_biometric_input():
    """Simple dialog to simulate biometric code (4 digits for demo)."""
    bio_window = tk.Toplevel(root)
    bio_window.title("Biometric")
    bio_window.geometry("300x150")
    bio_window.transient(root)
    bio_window.grab_set()

    tk.Label(bio_window, text="Enter your 4-digit biometric code:", font=("Helvetica", 12)).pack(pady=10)
    bio_entry = tk.Entry(bio_window, show="*", font=("Courier", 14), width=20)
    bio_entry.pack(pady=5)

    result = {"value": None}

    def on_submit():
        result["value"] = bio_entry.get()
        bio_window.destroy()

    tk.Button(bio_window, text="Submit", command=on_submit).pack(pady=10)
    root.wait_window(bio_window)
    return result["value"]

# ---------------------------
# Actions
# ---------------------------
def create_user():
    """Create a new user."""
    def submit():
        try:
            uid = int(entry_id.get())
            name = entry_name.get()
            level = int(entry_level.get())
            pin = entry_pin.get()
            user = User(uid, name, level, pin)
            user.save_to_db()
            messagebox.showinfo("Success", f"User {name} created.")
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    form = tk.Toplevel(root)
    tk.Label(form, text="User ID").grid(row=0, column=0)
    entry_id = tk.Entry(form)
    entry_id.grid(row=0, column=1)

    tk.Label(form, text="Name").grid(row=1, column=0)
    entry_name = tk.Entry(form)
    entry_name.grid(row=1, column=1)

    tk.Label(form, text="Zone Level (1/2/3)").grid(row=2, column=0)
    entry_level = tk.Entry(form)
    entry_level.grid(row=2, column=1)

    tk.Label(form, text="PIN (4 digits)").grid(row=3, column=0)
    entry_pin = tk.Entry(form, show="*")
    entry_pin.grid(row=3, column=1)

    tk.Button(form, text="Submit", command=submit).grid(row=4, columnspan=2)

def load_card():
    """Load card by user ID from DB."""
    global card_instance
    try:
        uid = int(entry_test_user.get())
        user = User.load_from_db(uid)
        if not user:
            log(f"[ERROR] User {uid} not found.", "error")
            return
        card_instance = VirtualCard(uid, user.scan_count, user.last_x, zone_level=user.zone_level)
        update_card_display()
        log(f"[CARD] Card loaded for User {uid}.", "success")
    except Exception as e:
        log(f"[ERROR] {str(e)}", "error")

def scan_zone1():
    """Zone 1: scan_count only (routed to current zone owner)."""
    global card_instance
    if not card_instance:
        log("[ERROR] No card loaded.", "error")
        return

    srv = get_server_for_zone(1)
    if not srv:
        log("[ERROR] No active server is managing Zone 1 right now.", "error")
        return

    result = card_instance.scan()
    if not result:
        log("[CARD] Card is locked or invalid scan.", "error")
        update_card_display()
        return

    received_count = result["count"]
    old_x = result["x_used"]
    new_x = result["new_x"]

    ok, user = srv.validate_scan_count(card_instance.user_id, received_count)
    if not ok:
        card_instance.lock()
        log(f"[{srv.name}]  Invalid scan count. Card locked.", "error")
        update_card_display()
        return

    success = srv.process_access(user, zone_requested=1, x_used=old_x)
    update_card_display()

    if success:
        if hasattr(card_instance, "unauthorized_zone_attempts"):
            card_instance.unauthorized_zone_attempts = 0
        log(f"[{srv.name}]  Access granted. Zone 1 New x = {new_x}", "success")
    else:
        log(f"[{srv.name}]  Access denied. Zone 1 Expected count: {user.scan_count}", "error")

    display_name = "Server 1" if srv is server1 else ("Server 2" if srv is server2 else "Server 3")
    server_data = {
        "name": srv.name,
        "managed_zones": srv.managed_zones,
        "user_id": user.user_id,
        "scan_count": user.scan_count,
        "x_used": old_x,
        "next_x": new_x,
        "pin_valid": "N/A",
        "otp_valid": "N/A",
        "status": " Access granted to Zone 1" if success else " Access denied to Zone 1"

    }
    update_server_display(display_name, server_data)

def scan_zone2():
    """Zone 2: PIN + OTP (routed to current zone owner)."""
    global card_instance
    if not card_instance:
        log("[ERROR] No card loaded.", "error")
        return

    srv = get_server_for_zone(2)
    if not srv:
        log("[ERROR] No active server is managing Zone 2 right now.", "error")
        return

    result = card_instance.scan()
    if not result:
        log("[CARD] Card is locked or invalid scan.", "error")
        update_card_display()
        return

    received_count = result["count"]
    x_used = result["x_used"]
    new_x = result["new_x"]

    user = User.load_from_db(card_instance.user_id)
    if not user:
        log(f"[{srv.name}]  User not found in database.", "error")
        return

    if user.zone_level < 2:
        if not hasattr(card_instance, "unauthorized_zone_attempts"):
            card_instance.unauthorized_zone_attempts = 0
        card_instance.unauthorized_zone_attempts += 1
        log(f"[{srv.name}]  User not authorized for Zone 2. Attempt {card_instance.unauthorized_zone_attempts}/3", "error")
        user.scan_count = received_count + x_used
        user.save_to_db()
        if card_instance.unauthorized_zone_attempts >= 3:
            card_instance.lock()
            log(f"[{srv.name}]  Card locked after 3 unauthorized zone access attempts.", "error")
        update_card_display()
        return

    ok, user = srv.validate_scan_count(card_instance.user_id, received_count)
    if not ok:
        card_instance.lock()
        log(f"[{srv.name}]  Invalid scan count. Card locked.", "error")
        update_card_display()
        return

    # Ask PIN
    pin_attempts = 0
    while pin_attempts < 3:
        entered_pin = show_pin_input()
        if entered_pin and len(entered_pin) == 4 and entered_pin.isdigit():
            break
        pin_attempts += 1
        log(f"[PIN]  Invalid PIN format attempt {pin_attempts}/3", "error")
    if pin_attempts == 3:
        card_instance.lock()
        log("[PIN]  Too many invalid attempts. Card locked.", "error")
        update_card_display()
        return

    pin_train, positions = build_pin_train(entered_pin)
    pin_train_display.config(state="normal")
    pin_train_display.delete("1.0", tk.END)
    pin_train_display.insert(tk.END, "PIN TRAIN: " + " ".join(pin_train))
    pin_train_display.config(state="disabled")

    # OTP
    otp_cloud, expected_otp = generate_otp_cloud(received_count)
    log(f"[OTP]  OTP cloud: {otp_cloud}", "normal")
    otp_cloud_display.config(state="normal")
    otp_cloud_display.delete("1.0", tk.END)
    otp_cloud_display.insert(tk.END, "OTP CLOUD: " + " | ".join(otp_cloud))
    otp_cloud_display.config(state="disabled")

    otp_attempts = 0
    otp_valid = False
    entered_otp = None

    while otp_attempts < 2:
        entered_otp = show_otp_input(expected_otp)
        if not entered_otp:
            otp_attempts += 1
            log(f"[OTP]  No OTP entered. Attempt {otp_attempts}/2", "error")
            continue
        if entered_otp == expected_otp:
            otp_valid = True
            break
        else:
            otp_attempts += 1
            log(f"[OTP]  Incorrect OTP attempt {otp_attempts}/2", "error")

    if not otp_valid:
        card_instance.lock()
        log("[OTP]  Too many incorrect attempts. Card locked.", "error")
        update_card_display()
        return

    success = srv.process_access(
        user,
        zone_requested=2,
        x_used=x_used,
        pin_train=pin_train,
        positions=positions,
        entered_otp=entered_otp,
        expected_otp=expected_otp
    )

    update_card_display()

    display_name = "Server 1" if srv is server1 else ("Server 2" if srv is server2 else "Server 3")
    server2_data = {
        "name": srv.name,
        "managed_zones": srv.managed_zones,
        "user_id": user.user_id,
        "scan_count": user.scan_count,
        "x_used": x_used,
        "next_x": new_x,
        "pin_valid": "" if extract_pin_from_train(pin_train, positions) == user.pin_code else "",
        "otp_valid": "" if entered_otp == expected_otp else "",
        "status": " Access granted to Zone 2" if success else " Access denied to Zone 2"


    }
    update_server_display(display_name, server2_data)

    if success:
        log(f"[{srv.name}]  Access granted to Zone 2.", "success")
    else:
        log(f"[{srv.name}]  Access denied to Zone 2.", "error")

def scan_zone3():
    """Zone 3: PIN + Biometric (simulated; routed to current zone owner)."""
    global card_instance
    if not card_instance:
        log("[ERROR] No card loaded.", "error")
        return

    srv = get_server_for_zone(3)
    if not srv:
        log("[ERROR] No active server is managing Zone 3 right now.", "error")
        return

    result = card_instance.scan()
    if not result:
        log("[CARD] Card is locked or invalid scan.", "error")
        update_card_display()
        return

    received_count = result["count"]
    x_used = result["x_used"]
    new_x = result["new_x"]

    user = User.load_from_db(card_instance.user_id)
    if not user:
        log(f"[{srv.name}]  User not found in database.", "error")
        return

    if user.zone_level < 3:
        if not hasattr(card_instance, "unauthorized_zone_attempts"):
            card_instance.unauthorized_zone_attempts = 0
        card_instance.unauthorized_zone_attempts += 1
        log(f"[{srv.name}]  User not authorized for Zone 3. Attempt {card_instance.unauthorized_zone_attempts}/3", "error")
        user.scan_count = received_count + x_used
        user.save_to_db()
        if card_instance.unauthorized_zone_attempts >= 3:
            card_instance.lock()
            log(f"[{srv.name}]  Card locked after 3 unauthorized zone access attempts.", "error")
        update_card_display()
        return

    ok, user = srv.validate_scan_count(card_instance.user_id, received_count)
    if not ok:
        card_instance.lock()
        log(f"[{srv.name}]  Invalid scan count. Card locked.", "error")
        update_card_display()
        return

    # Step 1: PIN
    pin_attempts = 0
    while pin_attempts < 3:
        entered_pin = show_pin_input()
        if entered_pin and len(entered_pin) == 4 and entered_pin.isdigit():
            break
        pin_attempts += 1
        log(f"[PIN]  Invalid PIN format attempt {pin_attempts}/3", "error")
    if pin_attempts == 3:
        card_instance.lock()
        log("[PIN]  Too many invalid attempts. Card locked.", "error")
        update_card_display()
        return

    pin_train, positions = build_pin_train(entered_pin)
    pin_train_display.config(state="normal")
    pin_train_display.delete("1.0", tk.END)
    pin_train_display.insert(tk.END, "PIN TRAIN: " + " ".join(pin_train))
    pin_train_display.config(state="disabled")

    # Step 2: Biometric (simulated like PIN)
    biometric_attempts = 0
    while biometric_attempts < 2:
        entered_bio = show_biometric_input()
        if entered_bio and len(entered_bio) == 4 and entered_bio.isdigit():
            break
        biometric_attempts += 1
        log(f"[BIOMETRIC]  Invalid entry attempt {biometric_attempts}/2", "error")
    if biometric_attempts == 2:
        card_instance.lock()
        log("[BIOMETRIC]  Too many invalid attempts. Card locked.", "error")
        update_card_display()
        return

    biometric_train, biometric_positions = build_pin_train(entered_bio)

    # Process Zone 3 (PIN + Biometric)
    success = srv.process_access(
        user,
        zone_requested=3,
        x_used=x_used,
        pin_train=pin_train,
        positions=positions,
        biometric_train=biometric_train,
        biometric_positions=biometric_positions
    )

    update_card_display()

    display_name = "Server 1" if srv is server1 else ("Server 2" if srv is server2 else "Server 3")
    server3_data = {
        "name": srv.name,
        "managed_zones": srv.managed_zones,
        "user_id": user.user_id,
        "scan_count": user.scan_count,
        "x_used": x_used,
        "next_x": new_x,
        "pin_valid": "" if extract_pin_from_train(pin_train, positions) == user.pin_code else "",
        "otp_valid": "N/A",
        "status": " Access granted to Zone 3" if success else " Access denied to Zone 3"


    }
    update_server_display(display_name, server3_data)

    if success:
        log(f"[{srv.name}]  Access granted to Zone 3.", "success")
        if hasattr(card_instance, "unauthorized_zone_attempts"):
            card_instance.unauthorized_zone_attempts = 0
    else:
        log(f"[{srv.name}]  Access denied to Zone 3.", "error")

def fake_scanner_attack():
    global card_instance
    if not card_instance:
        log("[ERROR] No card loaded.", "error")
        return
    result = card_instance.scan()
    log(f"[SECURITY]  Fake scanner used — sent count: {result['count']}, new x: {result['new_x']}", "error")
    update_card_display()

# ---------------------------
# Simple outage simulation buttons
# ---------------------------



# ---------------------------
# UI
# ---------------------------
root = tk.Tk()
root.title("Secure Access Control System")
root.geometry("1080x900")

# --- Toggle button labels ---
s1_btn_text = tk.StringVar(value="Deactivate Server 1")  # starts active
s2_btn_text = tk.StringVar(value="Deactivate Server 2")
s3_btn_text = tk.StringVar(value="Deactivate Server 3")

# --- Toggle handlers ---
def toggle_server1():
    server1.set_active(not server1.is_active)
    s1_btn_text.set("Reactivate Server 1" if not server1.is_active else "Deactivate Server 1")
    log(f"[Server 1]  {'Reactivated (up)' if server1.is_active else 'Deactivated (down)'}",
        "success" if server1.is_active else "error")

def toggle_server2():
    server2.set_active(not server2.is_active)
    s2_btn_text.set("Reactivate Server 2" if not server2.is_active else "Deactivate Server 2")
    log(f"[Server 2]  {'Reactivated (up)' if server2.is_active else 'Deactivated (down)'}",
        "success" if server2.is_active else "error")

def toggle_server3():
    server3.set_active(not server3.is_active)
    s3_btn_text.set("Reactivate Server 3" if not server3.is_active else "Deactivate Server 3")
    log(f"[Server 3]  {'Reactivated (up)' if server3.is_active else 'Deactivated (down)'}",
        "success" if server3.is_active else "error")


# Top controls
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Button(top_frame, text="Create User", command=create_user).grid(row=0, column=0, padx=5)
tk.Label(top_frame, text="User ID:").grid(row=0, column=1, padx=5)
entry_test_user = tk.Entry(top_frame, width=7)
entry_test_user.grid(row=0, column=2, padx=5)
tk.Button(top_frame, text="Load Card", command=load_card).grid(row=0, column=3, padx=5)

# Zone buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Zone 1 Scan", command=scan_zone1).grid(row=0, column=0, padx=6)
tk.Button(btn_frame, text="Zone 2 Scan", command=scan_zone2).grid(row=0, column=1, padx=6)
tk.Button(btn_frame, text="Zone 3 Scan", command=scan_zone3).grid(row=0, column=2, padx=6)
tk.Button(btn_frame, text="External Scanner", command=fake_scanner_attack).grid(row=0, column=3, padx=6)


# Outage simulation (toggle buttons)
switch_frame = tk.Frame(root)
switch_frame.pack(pady=6)

tk.Button(switch_frame, textvariable=s1_btn_text, command=toggle_server1).grid(row=0, column=0, padx=6)
tk.Button(switch_frame, textvariable=s2_btn_text, command=toggle_server2).grid(row=0, column=1, padx=6)
tk.Button(switch_frame, textvariable=s3_btn_text, command=toggle_server3).grid(row=0, column=2, padx=6)


# Log box
log_box = tk.Text(root, height=10, width=110, bg="white", fg="lime")
log_box.pack(pady=10)
log_box.tag_configure("success", foreground="green")
log_box.tag_configure("error", foreground="red")
log_box.tag_configure("normal", foreground="black")

# Card info display
card_frame = tk.Frame(root)
card_frame.pack(pady=10)
tk.Label(card_frame, text="Smart Card Display", font=("Helvetica", 12, "bold")).pack()
card_display = tk.Text(card_frame, height=5, width=30, bg="lightyellow", font=("Courier", 12))
card_display.pack()
card_display.config(state="disabled")

# Servers info display
server_frame = tk.Frame(root)
server_frame.pack(pady=10)

tk.Label(server_frame, text="Server 1 Info", font=("Helvetica", 12, "bold")).grid(row=1, column=0)
server1_display = tk.Text(server_frame, height=10, width=33, bg="lightblue", font=("Courier", 12))
server1_display.grid(row=0, column=0, padx=5)
server1_display.config(state="disabled")
server1_display.tag_configure("server", foreground="black", font=("Courier", 12, "bold"))

tk.Label(server_frame, text="Server 2 Info", font=("Helvetica", 12, "bold")).grid(row=1, column=1)
server2_display = tk.Text(server_frame, height=10, width=33, bg="lightgreen", font=("Courier", 12))
server2_display.grid(row=0, column=1, padx=5)
server2_display.config(state="disabled")
server2_display.tag_configure("server", foreground="black", font=("Courier", 12, "bold"))

tk.Label(server_frame, text="Server 3 Info", font=("Helvetica", 12, "bold")).grid(row=1, column=2)
server3_display = tk.Text(server_frame, height=10, width=33, bg="lightpink", font=("Courier", 12))
server3_display.grid(row=0, column=2, padx=5)
server3_display.config(state="disabled")
server3_display.tag_configure("server", foreground="black", font=("Courier", 12, "bold"))

# PIN train + OTP display
info_frame = tk.Frame(root)
info_frame.pack(pady=10)

tk.Label(info_frame, text="PIN Train (hidden PIN + noise)", font=("Helvetica", 12)).pack()
pin_train_display = tk.Text(info_frame, height=2, width=65, bg="lightgray", font=("Courier", 12))
pin_train_display.pack(pady=5)
pin_train_display.config(state="disabled")

tk.Label(info_frame, text="OTP Cloud (1 real + 4 fake)", font=("Helvetica", 12)).pack()
otp_cloud_display = tk.Text(info_frame, height=2, width=65, bg="lightgray", font=("Courier", 12))
otp_cloud_display.pack(pady=5)
otp_cloud_display.config(state="disabled")

# Init DB and run
init_db()
root.mainloop()
