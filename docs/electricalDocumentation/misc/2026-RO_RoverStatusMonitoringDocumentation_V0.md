# **Cleaned Up Documentation**

**Rover 2025-2026**  
**Rover Status Monitoring Interface**  
**Documentation**

Sonia Ly

# **Project Overview**

A Rover Status Monitoring Interface is a real-time display system that provides operators with key information about a rover’s electrical and operational state. The project originated as a simple voltage and current sensing task but has evolved to include additional critical data, such as battery status and kill switch state, enabling safe operation, quick troubleshooting, and effective performance monitoring.  
	  
While it may initially seem like a convenience or quality-of-life upgrade, the interface is useful for safe and efficient operation. By allowing operators to quickly identify abnormal conditions, prevent potential failures, and conveniently access vital information, it aims to substantially minimize the risk of damage to the rover.

# 

# **Telemetry Architecture (need a better, less vague, title .\_.)**

The 2025 Rover Powerboard PCB features a Teensy 4.0 microcontroller that handles telemetry for the various peripherals connected to the powerboard. This includes monitoring voltage and current for each system (arm, antenna, etc.), as well as tracking the status of the headlights and kill switch.

The Teensy also enables software control of the headlights and secondary kill switch when connected, allowing these functions to be toggled directly through the firmware.

For reference, the Rover 2025 Powerboard schematic (found in *MCU+Controls.SchDoc*) illustrates how the Teensy 4.0 interfaces with each peripheral—useful when modifying firmware or identifying which pins correspond to specific subsystems.

A single INA230 Current, Voltage, and Power Monitoring IC is used to measure seven peripherals (see Table 1). It communicated with the Teensy via the I2C communication protocol.

# 

# **Firmware**

The firmware for this project can be found in the rover-embedded-2025[^1] GitHub repo, under the status\_display branch.

## **SETUP**

1) IDE: VSCode \-\> PlatformIO  
     
2) Extensions:

   latformIO

* C/C++  
* C/C++ Extension Pack

3) Compiler: MinGW-w64[^2] (If on Windows, if not then figure it out)

Note: Once you’ve installed the compiler, make sure to close and re-open VSCode 

## **VOLTAGE AND CURRENT SENSING**

The firmware was written based on the guide in section *7.5 Programming* of the INA230 datasheet. 

The “target” address for each INA230 chip was determined by referencing Table 7-2 *INA230 Address Pins and Target Addresses* (on p.18) of the datasheet. Essentially, the target address of an INA230 IC is determined by what its A0 and A1 pin is connected to. Identifying its target address can easily be done by looking at the power board schematic, but for the sake of convenience, here are the target addresses associated to each INA230 IC on the board:

| ID in Schematic | System | A1 | A0 | Target Address | Target Address (HEX) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| U1 | Jetson | GND | GND | 1000000 | 0x40 |
| U2 | Raspberry Pi | GRD | 5V | 1000001 | 0x41 |
| U3 | Antenna | GND | SDA | 1000010 | 0x42 |
| U4 | Rocker 1 (L) | GND | SCL | 1000011 | 0x43 |
| U5 | Rocker 2 (R) | 5V | GND | 1000100 | 0x44 |
| U6 | Arm | 5V | 5V | 1000101 | 0x45 |

***Table 1:** Target Addresses for each IC on the Power Board*

The registers you can write to and their addresses can be found in Table 7-3 *Summary of Register Set* (p.21-22) in the datasheet.

The R\_SHUNT value is 0.0002 Ohms (check schematic) and the MAX\_EXPECTED\_CURRENT is 25 Amps (value provided by James Di Sciullo lol)

## **HEADLIGHT & KILL SWITCH TOGGLE**

Firmware for Headlight and Kill Switch toggle exists in the project too.

## **PYTHON SCRIPTS**

Python scripts have been written for each of these functionalities to facilitate testing. If more features are added, it would be ideal to write python scripts for those too. Look into how to use the pyserial library if you are working on this.

**Future Improvements**  
Although the essential firmware for this project is (probably) complete, it, unfortunately, wasn't a high enough priority task to be completed in the 2024-2025 school year. There are many upgrades that can be done and here is a list: 

* Actually display the telemetry information onto a screen  
  * Find a compatible screen that uses a compatible communication protocol  
  * Write UI to display the information in a neat way  
* ~~Find a way of sending the telemetry information to the Jetson so that the data can be accessed by the base station computer during competition tasks. This would allow the driver(s) to identify where the source of the problem may be. Would probably need to chat with Software division for this.~~  
* Display the status of the Kill Switches.  
* Currently, only the Left Rocker INA230 is soldered on. The rest must be too. 

# **WIP**

# **Test Jig: Current and Voltage Sensing** 

A test jig was made to test the current and voltage sensing capabilities of the INA230. The following is a guide for how to set it up. The setup for this jig can be figured out by looking at the layout example on page 30 of the datasheet of the INA230, but since it may 

## **MATERIAL**

* An INA230 IC  
* A power supply   
* Shunt resistor   
* Jumper cables  
* 

Figure 1: 

**Figure 2:** Picture of the physical test jig for current and voltage sensing 

blablabla

## **FIRMWARE FOR TEST JIG**

[^1]:  [rover-embedded-2025](https://github.com/mcgill-robotics/rover-embedded-2025) repo link

[^2]:  [How to download \+ setup](https://code.visualstudio.com/docs/languages/cpp) the compiler