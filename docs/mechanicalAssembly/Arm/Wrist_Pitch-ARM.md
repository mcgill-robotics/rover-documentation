# **Wrist Roll Motor**
## Motor and Gearbox Specifications

Electrical requirements:

* Must be brushed  
* Must include an encoder  
* Must draw the least amount of current  
* Must be 24V

Technical Specifications

| Rated Torque (Nm) | 8.82 |
| :---- | :---- |
| Rated RPM | 13 |
| Rated Voltage (DC) | 12 |
| Rated Current (A) | 3 |
| Gearbox ratio | 1:625 |
| Weight | \- |
| Data sheet link | [Link](https://drive.google.com/file/d/13U5swvCJxRlo7_JIyFcc0mwr1mnc3qjD/view?usp=drive_link) |

Supplier info

| Supplier | Robot Shop |
| :---- | :---- |
| Brand | E-S Motor |
| Part Number (SKU)  | RM-ESMO-0CP |
| Manufacturer number | 42PG-775-625-EN 24V |
| Price ($) | 68.12 |
| Link | https://ca.robotshop.com/products/e-s-motor-42mm-high-torque-planetary-gear-motor-w-encoder-24v-13rpm?qd=27b67613532d703a35f7fc44657f9aa6 |

## Mechanical Simulation and Analysis

### Hand Calculations:

Since dynamic analysis is more appropriate here (than static analysis), we have to consider the moment of inertia. So, it was established that the wrist must be able to make half a rotation in one second:

![ \=30 rpm \=  rad/s](img-wristpitch/image1.png)  
 
![\=t=  rad/s1s= rads2](img-wristpitch/image2.png)

The moment equation about the center of the small gear is:  

![M=mgrCG \-Tmotor=I](img-wristpitch/image3.png)   
![I \= 0.00426 kg/m2](img-wristpitch/image4.png)  
![rCG=64.74mm](img-wristpitch/image5.png)  
![m=7kg](img-wristpitch/image6.png) (approximate weight of wrist, end-effector, and weight picked up by end-effector)  

![0.0647479.81 \-Tmotor=0.00426](img-wristpitch/image7.png)   
![Tmotor=4.40Nm](img-wristpitch/image8.png)  

**With a factor of safety of 2:**  
![Tmotor=24.40= 8.80Nm](img-wristpitch/image9.png)  


#### Original notes:
![](img-wristpitch/image10.png)
