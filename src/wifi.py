import machine
import network
import socket
import json
import time
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY

# set up the display and drawing constants
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
display.set_backlight(0.5)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
display.set_font("bitmap8")

def show_text(msg):
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)
    display.text(msg, 10, 10, scale=4)
    display.update()

# temperature sensor setup
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

# WiFi setup
SSID = "<NETWORK>"
PASSWORD = "<PASSWORD>"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(0.2)

ip = wlan.ifconfig()[0]
print("Connected! Pico IP:", ip)
show_text(str(ip))


# HTTP server setup
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)

print("Web API running on http://%s" % ip)

# Main loop
while True:
    client, remote_addr = server.accept()
    request = client.recv(2048).decode()

    # Basic request parsing
    method = request.split(" ")[0]
    path = request.split(" ")[1]

    if method == "GET" and path == "/temperature":
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        show_text(f'T: {temperature:.2f} C')

        body = json.dumps({"status": "ok", "temperature": temperature})
        response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Content-Length: %d\r\n"
                "\r\n%s" % (len(body), body)
        )
        client.send(response)

    elif method == "GET" and path.startswith("/display/"):
        raw = path[len("/display/"):]     # everything after /display/
        text = raw.replace("%20", " ")

        print("Received text:", text)
        show_text(text)

        reply = json.dumps({"received": text})
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "\r\n" + reply
        )
        client.send(response)



    # 404 fallback
    else:
        client.send("HTTP/1.1 404 Not Found\r\n\r\n")

    client.close()
