# Pico display demos

1. Start the pico in while pressing the BOOTSEL button.
2. An USB drive will appear on your computer.
3. Copy the correct uf2 file to this drive. See driver folder or pimoroni releases on [github](https://github.com/pimoroni/pimoroni-pico/releases):
    - pico-v1.25.0-pimoroni-micropython.uf2 for pico 1
    - rpi_pico2_w-v1.26.1-micropython.uf2 for pico 2W
4. Reboot the pico without pressing the BOOTSEL button.
5. Install [Thonny](https://thonny.org/) and configure it for the pico:
    - Go to Tools - Options - Interpreter
    - Choose MicroPython (Raspberry Pi Pico)
    - Select the comport your pico is connected to.
  
6. Select a file from the src folder in Thonny.
    - File  Save As…
    - Choose Raspberry Pi Pico
    - Save the file as main.py
