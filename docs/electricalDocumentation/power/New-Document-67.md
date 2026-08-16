---
format: md
---

# Distraction Tab

Nothing to see here, move along.

# Introduction

# PD Board

Tony (T 🐕)

My original buck was supposed to be able to interface with devices compatible with the USB PD standard. Basically, it should be able to interface with a Raspberry Pi and be like “yup, you can take 5 amps” and then the Pi should be like “ok bet”.

# Verification of Working

# How am I even supposed to know if my thing is working?

I’ll need to run hexdump \-C /proc/device-tree/chosen/power/usbpd\_power\_data\_objects.

(source: [https://www.raspberrypi.com/documentation/computers/configuration.html\#common-bootloader-properties-chosenbootloader](https://www.raspberrypi.com/documentation/computers/configuration.html#common-bootloader-properties-chosenbootloader))

And I should see a “binary blob containing multiple 32-bit integers”

I’ll look more into this if I actually get the board manufactured but this is a good start.

# BOM

I will Definitely need to get this assembled due to the complexity of the IC. Whatever, at least I won’t have to pay for the stencil.

| Component Name /Designator | Manufacturer / Model Number | Price (CAD$) | Quantity | Notes |
| :---- | :---- | :---- | :---- | :---- |
|  | Infineon \- CYPD3177-24LQXQT | 3.12 | 1 | PD Controller |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

# References

