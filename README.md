# Pico display demos

1. Start the pico in while pressing the BOOTSEL button.
2. An USB drive will appear on your computer.
3. Copy the pimoroni-micropython.uf2 driver to this drive. See driver folder or pimoroni releases on [github](https://github.com/pimoroni/pimoroni-pico/releases).
4. Reboot the pico without pressing the BOOTSEL button.
5. Install [Thonny](https://thonny.org/) and configure it for the pico:
    - Go to Tools - Options - Interpreter
    - Choose MicroPython (Raspberry Pi Pico)
    - Select the comport your pico is connected to.
  
6. Select a file from the src folder in Thonny.
    - File  Save As…
    - Choose Raspberry Pi Pico
    - Save the file as main.py
