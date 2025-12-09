import socket
import time
import threading
from pynput import keyboard as kb


HOST = '10.42.0.1'
PORT = 5001

key_map = {
    kb.Key.up: b'FORWARD',
    kb.Key.down: b'BACKWARD',
    kb.Key.left: b'LEFT',
    kb.Key.right: b'RIGHT',
    'w': b'UP',
    's': b'DOWN',
    'm': b'STOP',
}
priority = [kb.Key.up, kb.Key.down, kb.Key.left, kb.Key.right]

def main():
    pressed = set()
    lock = threading.Lock()
    stop_event = threading.Event()
    s = None 

    def connect():
        nonlocal s
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((HOST, PORT))
            sock.settimeout(None)
            s = sock
            print(f"Connected to server {HOST}:{PORT}")
        except OSError as e:
            s = None
            print(f"Could not connect to {HOST}:{PORT} -> {e}. Running offline (printing keys).")

    def on_press(key):
        k = key
        try:
            if hasattr(key, 'char') and key.char:
                k = key.char.lower()
        except:
            pass

        if k in key_map:
            with lock:
                pressed.add(k)
        elif k in ('q',) or key == kb.Key.esc:
            stop_event.set()
            return False


    def on_release(key):
        k = key
        try:
            if hasattr(key, 'char') and key.char:
                k = key.char.lower()
        except:
            pass

        if k in key_map:
            with lock:
                pressed.discard(k)


    connect()

    with kb.Listener(on_press=on_press, on_release=on_release) as listener:
        last_cmd = None
        try:
            while not stop_event.is_set():
                with lock:
                    active = next((k for k in priority if k in pressed), None)
                    
                    if not active:
                        if 'w' in pressed:
                            active = 'w'
                        elif 's' in pressed:
                            active = 's'
                        elif 'm' in pressed:
                            active = 'm'

                cmd = key_map[active] if active else None

                if cmd != last_cmd:
                    if cmd:
                        if s:
                            try:
                                s.sendall(cmd)
                            except OSError as e:
                                print(f"Socket error: {e}. Switching to offline mode.")
                                try:
                                    s.close()
                                except Exception:
                                    pass
                                s = None
                        else:
                            print(f"CMD: {cmd.decode()}")
                    else:
                        if not s:
                            print("IDLE")
                    last_cmd = cmd

                time.sleep(0.1)
        finally:
            stop_event.set()
            listener.stop()
            if s:
                try:
                    s.close()
                except Exception:
                    pass

if __name__ == "__main__":
    main()
