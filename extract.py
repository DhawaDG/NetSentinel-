import sqlite3
import subprocess
import time
from datetime import datetime

DB_PATH = 'database.db'

# Devices to monitor
devices = [
    {"name": "Main_Router", "ip": "192.168.1.1", "type": "Router"},
    {"name": "Reception_SIP_Phone", "ip": "192.168.1.50", "type": "SIP Phone"},
    {"name": "Biometric_Server", "ip": "192.168.1.100", "type": "Security"}
]

def run_check():
    # Generate a unique session for each "hour" of the demo
    session_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS device_logs 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, 
                       device_name TEXT, status TEXT, timestamp DATETIME)''')

    for device in devices:
        # Ping check
        res = subprocess.run(['ping', '-n', '1', device['ip']], capture_output=True, text=True)
        status = "Online" if res.returncode == 0 else "Offline"
        
        cursor.execute("INSERT INTO device_logs (session_id, device_name, status, timestamp) VALUES (?, ?, ?, ?)",
                       (session_id, device['name'], status, datetime.now()))
    
    conn.commit()
    conn.close()
    print(f"Log captured at {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    # --- DEMO MODE SETTINGS ---
    # lets simulate an 2-hour shift in 2 seconds:
    cycles = 8  
    delay = 1   # 1 second between checks for instant results
    
    # --- PRODUCTION MODE SETTINGS (Commented out for reference) ---
    # cycles = 16  # 16 cycles (30 mins each = 8 hours)
    # delay = 1800 # 1800 seconds = 30 minutes
    
    print(f"Starting INSTANT DEMO: Running {cycles} cycles...")
    
    for i in range(cycles):
        print(f"Simulating Hour {i+1}...")
        run_check()
        if i < cycles - 1:
            time.sleep(delay) 
            
    print("--- Demo Data Generation Complete ---")

