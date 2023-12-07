import network
import time


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Tima", "00000000")

    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break

        wait -= 1
        print("Waiting for connection..")
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError("Wifi connection failed")
    else:
        print("Connected!")
        print(f"IP: {wlan.ifconfig()[0]}")

