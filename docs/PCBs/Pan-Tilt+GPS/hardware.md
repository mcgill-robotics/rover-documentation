# Pan-Tilt & GPS - Comms

## Purpose of the PCB
The PCB is designed to:
- Read UART output from GPS.
- Control two Pan-Tilt servo motors.

## Functionality Description
- **Inputs**: 
  - Reads UART data from GPS.
  - Reads the rover’s angle position data using a gyroscope.
- **Outputs**: 
  - Sends instructions to the servos.
  - Communicates with the Jetson via USB.

## Components Communication
1. **Microcontroller**: A Teensy 4.0 is mounted on the PCB.
2. **Servo Motors**: 
   - Each servo’s PWM pin connects to a PWM pin on the Teensy for control.
3. **GPS**:
   - TX pin (GPS) → RX pin (Teensy).
   - RX pin (GPS) → TX pin (Teensy).
4. **Gyroscope**:
   - SDA pin (Gyro) → SDA pin (Teensy).
   - SCL pin (Gyro) → SCL pin (Teensy).

## Components Connections (Routing)
| Teensy Pin | Connected To         |
|------------|----------------------|
| 23         | Servo 1 PWM          |
| 22         | Servo 2 PWM          |
| 0          | GPS TX               |
| 1          | GPS RX               |
| 17         | Gyro SDA             |
| 16         | Gyro SCL             |
| 2          | LED1                 |

## Power & Grounding
- **Power Source**: All components are powered by an external 5V source, distributed to each component's VCC pin via internal PCB routing.
- **Grounding**: Includes a net tie to separate the Teensy ground from the components ground.

## Notes for Assembling
1. On the back of the Teensy, locate the copper trace connecting the USB port to the Vin pin.
2. Use an X-Acto knife to cut this copper trace. This ensures the Teensy is powered by the external 5V source instead of the USB connection.

## Additional Resources
- **How to Crimp Wires for Molex Connectors**: [YouTube Link](https://www.youtube.com/watch?v=WFvEeWHDt1E)
- **Schematic**: [YouTube Link](https://www.youtube.com/watch?v=WFvEeWHDt1E)
