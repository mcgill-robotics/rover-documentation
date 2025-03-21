# Steering Mechanism

### System: Drive

## **Mechanical Design:**

### Goal and purpose

The steering mechanism’s purpose is to indirectly drive the steering assembly. Instead of the steering motor shaft taking the stresses and loads while the rover is driving, the goal is to have this mechanism’s steel shaft take the reaction forces. Another purpose for this mechanism is to connect the steering bracket to the end of the suspension.

### Functionality

The steering mechanism is used to transmit the torque from the steering motor to an output shaft that will drive the steering bracket and wheel assembly. Gears are used to transmit the power.

### CAD

GitHub Path: Rover\_v05\\DRIVE\\STEERING MECHANISM

![](img\steering\image9.png)![](img\steering\image1.png) 
![](img\steering\image20.png)![](img\steering\image9.png)


## **Specifications:**

### Bounding box dimensions

110x190.29x49.53 \[mm\] (with motor)  
110x90.86x49.53 \[mm\] (without motor)

### Material(s)

- Aluminum 6061-T6: Machined/laser cut brackets  
- AerMet 310: Output shaft  
- Carbon Steel 1045: Gears, collar, bearings  
- PETG: Spacers, covers, limit switch arm, 

### Weight

654g (without motor and fastener)

### Included electrical components

- 1 x Limit switch ZMA00A150L04PC  
- Placed at the top of the assembly.  
- Switched by the cam shape at the top of the output shaft  
- To indicate when steering is in position for forward driving (zero-ing/straight position)

![](img\steering\image19.png)

### Motor and Gearbox Specification

- Weight: 360g  
- Voltage: 24V  
- Torque at rated voltage: 7.15Nm (73kg.cm)  
- No load speed (RPM): 15RPM  
- Safety Factor: 1.43  
- Gearbox ratio: 516:1  
- Shaft diameter: 8mm  
- Link to supplier website: [https://microdcmotors.com/product/31mm-reversible-planetary-gear-motor-model-nfp-ga32y-31zy-en](https://microdcmotors.com/product/31mm-reversible-planetary-gear-motor-model-nfp-ga32y-31zy-en)

![](img\steering\image7.png) 
L \= 45mm

### Power Transmission Specification

- Gear ratio: 1:1  
- Gears in assembly:   
  - Gear for steering motor D-shaft:  
    Specs: 1.5M, 24 teeth, 8mm bore, no key hole, 1045 carbon steel  
    Link to supplier website:  
    [https://www.aliexpress.com/item/1005004961200856.html?spm=a2g0o.order\_list.order\_list\_main.5.21ef1802dYw6pZ](https://www.aliexpress.com/item/1005004961200856.html?spm=a2g0o.order_list.order_list_main.5.21ef1802dYw6pZ)   
  - Gear for steel output shaft:  
    Specs: 1.5M, 24 teeth, 8mm bore, 3mm key hole, 1045 carbon steel  
    [https://us.misumi-ec.com/vona2/detail/110300428520/?HissuCode=GEAKBB1.5-24-15-B-8N\&PNSearch=GEAKBB1.5-24-15-B-8N\&searchFlow=results2type\&KWSearch=GEAKBB1.5-24-15-B-8N](https://us.misumi-ec.com/vona2/detail/110300428520/?HissuCode=GEAKBB1.5-24-15-B-8N&PNSearch=GEAKBB1.5-24-15-B-8N&searchFlow=results2type&KWSearch=GEAKBB1.5-24-15-B-8N) 

### Functionality of assembly 

#### Output Shaft Stack Up and Functionality

| ![](img\steering\image3.png) |  Stack up: |
| :---: | ----- |
|  | Shaft Collar: Prevent shaft from falling down |
|  | Ball Bearing: Reduce friction and align shaft |
|  | Thrust Bearing: Reduce friction and absorb axial force |
|  |  Spur Gear: Power transmission (secures to the shaft by key and set screw) |
|  | Bracket Flange: Keep bearing in place |
|  | Ball Bearing: Reduce friction and align shaft |
|  | Thrust Bearing: Reduce friction and absorb axial force |
|  | Shaft Flange: Keep stack up from falling out |
|  | Steering bracket connection plate |

#### Motor Shaft Stack Up and Functionality

| ![](img\steering\image5.png) |  Stack up: |
| :---- | ----- |
|  | Motor Shaft (secures to gear by set screw) |
|  | 3D Printed Spacer: Keep gear aligned with the other |
|  |  Spur Gear: Power transmission |
|  | Alignment Shaft: Help with axial alignment |
|  | Ball Bearing: Reduce friction and align shaft |

## 

## **Mechanical Simulation and Analysis:**

### Static Simulation

#### Output shaft

- Case study: Rover drops from 0.5m  
- Set-up:  
  - Material: AerMet 310, custom material, properties taken from:  
    [AerMet 310 properties.pdf](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.carpentertechnology.com/hubfs/Data%2520Sheets/AerMet%2520310.pdf&ved=2ahUKEwjx853R5NKLAxV1w_ACHZhZFKoQFnoECCQQAQ&usg=AOvVaw1EpePfHl8iR63Y_FPDO5ly)   
  - Applied Loads:   
    - 600N upwards at the bottom face of the flange  
    - No safety factor is applied to loads, forces are  already exaggerated   
  - Fixtures:  
    - Radially fixed at the bearing location  
    - Axial fixed on the contact area of the thrust bearing and flange  
    - Fixed support at the top of the shaft

    

- Screenshot

| Stress distribution | Displacement |
| :---: | :---: |
| ![](img\steering\image14.png) | ![](img\steering\image11.png) |


- Case study: Rover drives into a wall, according to suspension Matlab simulation  
- Set-up:  
  - Material: AerMet 310, custom material, properties taken from:  
    [AerMet 310 properties.pdf](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.carpentertechnology.com/hubfs/Data%2520Sheets/AerMet%2520310.pdf&ved=2ahUKEwjx853R5NKLAxV1w_ACHZhZFKoQFnoECCQQAQ&usg=AOvVaw1EpePfHl8iR63Y_FPDO5ly)   
  - Applied Loads:  
    - 520N to the left at the bottom face of the flange  
    - 125N upwards at the bottom face of the flange  
    - 93.6Nm on the axis perpendicular to the shaft axis, on the bottom face of the flange  
    - No safety factor is applied to loads, forces are already exaggerated   
  - Fixtures:   
    - Radially fixed at the bearing location  
    - Axial fixed on the contact area of the thrust bearing and flange  
    - Fixed support at the top of the shaft

- Screenshots:

| Stress distribution | Displacement |
| :---: | :---: |
| ![](img\steering\image6.png) | ![](img\steering\image16.png) |

#### Brackets connecting suspension to steering

- Case study: Rover drives into a wall, according to suspension Matlab simulation  
- Set-up:  
  - Material: Aluminum 6061-T6, Ansys library material   
  - Applied Loads:  
    - Same 520N and 125N loads but divided by 2 as there are two brackets per steering mechanism  
    - Remote 62.5N load upwards (+Y-axis) at the top hole closest to weight relief  
    - Remote 255N load to the right (+X-axis) at the same hole  
    - No safety factor is applied to loads, and forces are already exaggerated, hence want close to SF of 1  
      - Results: SF=1.05  
  - Fixtures:  
    - Axially and tangentially fixed at two bottom holes (M3)  
    - Free radially at two bottom holes (M3)

- Screenshots:

| Stress distribution | Displacement |
| :---: | ----- |
| ![](img\steering\image15.png) | ![](img\steering\image10.png) |

### Motor & Power Transmission Calculations

Motors are rated for 7.15Nm torque and 15 RPM corresponding to 0.015062 hp. The gears need to be able to take and transmit this load in addition to a safety factor.  
The following website was used to find the correct gears for this application.  
[https://evolventdesign.com/pages/gear-strength-calculator](https://evolventdesign.com/pages/gear-strength-calculator)

Inputs  
Pinion RPM: 15  
Module: 1.5  
Number of teeth (pinion): 24  
Number of teeth (gear): 24  
Pressure angle: 20  
Material: Steel, BHM \>180  
Manufacturing methods: Hobbed or shaved  
Face width \[mm\]: 15  
Support conditions: Less rigid mounting, contact across the full face  
Power source: Uniform  
Character of load: Uniform  
Pinion and gear material: Steel  
Total life cycles required: 100,000  
Application requirements: Fewer than 1 in 100  
Safety factor: 1.2

Output  
Horsepower: 0.01397 hp

Since the motor’s corresponding hp is calculated from the toque with a safety factor and an at-no load speed RPM, the difference in hp is acceptable.

Additional documentation for motor selection:  
[Steering Motor Selection Process](https://docs.google.com/document/d/1G8tH65Sch3DyAUgKkcOe7X5swMmq2XpTk6KxpRKquhc/edit?usp=sharing)

## **Assembly and Machining:**

Parts made from aluminum are standard sheet metal thicknesses (excluding the bottom plate placed under the gears). The parts were ordered and laser cut through Sendcutsend. Post machining processes include tapping the M3 holes in the connection plate, drilling, tapping, and milling the top plate to fit bearing tolerances and add counterbore holes. 

Parts machined at school include the bottom plate, aluminum alignment shaft, and steel shaft.  
Drawings for these parts are in the Appendix.

Specific tolerances: [Bearing Fits.pdf](https://drive.google.com/file/d/1rbsR6Vu4XsITub9o-CqVe4-AJuiKqWc8/view?usp=drive_link)  
Shaft:   
\+0.001  
\+0.01

Bearing: (608ZZ)  
\+0.0105  
\-0.0105

3D parts printed include the cover, limit switch arm, and all spacers.

### Assembly to Rover

Assembly to steering bracket uses the connecting bracket and 4 x M4-10mm countersink screws  
Assembly to suspension square-channel uses 2 x M5-55mm screws and M5 nuts.

### Physical part/assembly

For initial testing, while waiting for parts to get machined, a 3D-printed version of the assembly was made.

![](img\steering\image13.jpg) ![](img\steering\image8.jpg)

Final Assembly:

*Insert assembled picture*

## 

## **Appendix**

### BOM

![](img\steering\image18.png)

### Mechanical Drawings

Output shaft  
![](img\steering\image4.png)

Alignment shaft![](img\steering\image12.png)

Bottom plate![](img\steering\image17.png)