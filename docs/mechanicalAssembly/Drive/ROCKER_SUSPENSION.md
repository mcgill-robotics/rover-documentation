# Rocker Suspension

**System:** Drive

## **Mechanical Design:**

### Goal and Purpose

The suspension mechanism is used to absorb shocks and periodic vibrations which can damage crucial components on the rover. The suspensions need to be able to absorb the shocks of a 0.5m drop while also being able to clear obstacles as high as 30cm.  
 

### Functionality

It is based on a hybrid rocker suspension, where there are two rocking links on either side of the rover that oscillate in opposite direction averaging out any bump or crevice. It is also equipped with 4 shocks allow it to absorb frontal and vertical impacts

### CAD

> GitHub Path: Rover\_v05\\DRIVE\\SUSPENSION

![](img\rocker\image13.png)

![](img\rocker\image10.png)

![](img\rocker\image4.png)

## **Specifications:**

### Bounding Box Dimensions

193x857x778 \[mm\]

### Materials

- Aluminum 6061-T6: Machined/Laser cut bracket  
- Brass: Bushings  
- Carbon Steel: Shoulder Bolts, Shocks, Nuts, Pivot Shaft  
- PETG: Spacers, Covers

### Weight

4580g

### Included electrical components

N/A

### Shocks Specification

- Weight: 350g each  
- Length: 165mm  
- Spring Constant: 650 lbs/in  
- Damping Coefficient: N/A  
- Hole Diameter: 8mm  
- Link to supplier website:  
  [https://a.co/d/6U3LlC1](https://a.co/d/6U3LlC1)


### Functionality of Assembly:

#### Rocking Mechanism

| ![](img\rocker\image8.png) | Bearings are press-fit into aluminum bearing housing, then  rocking shaft is inserted into bearing bores and tightened using M14 nut. The nut is to prevent the shaft from sliding out even though it is press fit. |
| :---- | :---- |

#### Linkages and Springs

| ![](img\rocker\image18.png) | All components are attached to one another using 8mm shoulder bolts while being separated by brass / plastic bushings. Only the V shaped gussets are held on using rivets |
| :---- | :---- |

#### Differential Bar

| ![](img\rocker\image5.png) | The differential bar is attached to the main assembly using ball joints  |
| :---- | :---- |

## **Mechanical Simulation and Analysis:**

### Static Simulations:

#### Gusset Plates:

- Case study:   
  - Rover drops from 0.5m  
  - Frontal Impact  
- Set-up:  
  - Material: All gusset plates are out of 6061-T6 Aluminum  
  - Applied Loads:   
    - 600N vertical load was applied at link tip and we let the simulation run  
  - Fixtures:  
    - Axially and tangentially fixed at the shoulder bolts location

![](img\rocker\image3.png)		![](img\rocker\image1.png)

![](img\rocker\image17.png)

![](img\rocker\image15.png)	      ![](img\rocker\image11.png)

#### Pivot Assembly:

- Case study:   
  - Rover drops from 0.5m  
  - Frontal Impact  
- Set-up:  
  - Material: The bearing housing is made of  6061-T6 Aluminum and the shaft is made out of carbon steel  
  - The bearings were assumed to be infinitely fixed for the sim.  
  - Applied Loads:   
    - 1200N vertical load was applied at the shaft tip, aluminum housing was fixed at bolt holes and the shaft was assumed to be bonded to the bearings.

![](img\rocker\image16.png)

## **Assembly and Machining:**

The rocking assembly is assembled first, the bearings are press-fit into the housing and then, the shaft is press-fit into both bearings. Check list of tolerances bellow:

Bearing Hole: 1.8504” \+- 0.0003”  
Shaft Diameter: 0.6693” \+0.0005”

Then the V shaped gusset plates get riveted on the square tubes and the bushings get inserted into the link holes. Then, with the shoulder bolts and spacers attach the springs to the center gusset. Finally attach the center gusset to the pivot shaft using 4 M5x10mm bolts.

### Final Assembly:

![](img\rocker\image2.png)

## **Appendix:**

![](img\rocker\image14.png)

![](img\rocker\image6.png)

![](img\rocker\image9.png)

![](img\rocker\image12.png)

![](img\rocker\image7.png)

