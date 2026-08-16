**ROVER WIRING STANDARD**

Wire Identification & Annotation Guide

------------------------------------------------------------------------

This document defines the standard for identifying, labelling, and
tracking every wire in the rover. All team members must follow this
standard when adding wires to the wire register spreadsheet or
physically labelling harnesses.

------------------------------------------------------------------------

**1. Wire ID Format**

Every wire has a single unique ID that encodes its type, system, route,
and destination connector. The format is:

> \[NUM\]-\[TYPE\]-\[SYS\]-\[FROM\]-\[TO\]-\[CONN\]

Example:

> 201-P-DRV-PWB-SPL-RKL

Power wire #201 in the Drive system, from the Power Board to the
Splitter, plugging into the RKL connector.

  ------------- ------------ ------------------- -----------------------
   **Segment**   **Values**      **Meaning**           **Example**

     **NUM**      101--999      3-digit wire               201
                             number; grouped by  
                             system (see legend) 

    **TYPE**       P or D    P = Power wire \| D            P
                               = Data / signal   
                                    wire         

     **SYS**      3-letter     System the wire             DRV
                    code         belongs to      

    **FROM**    3--5 letters Abbreviated source            PWB
                             device (silkscreen  
                                 preferred)      

     **TO**     3--5 letters     Abbreviated               SPL
                             destination device  

    **CONN**     Silkscreen  Connector label on            RKL
                    text     the TO device being 
                                plugged into     
  ------------- ------------ ------------------- -----------------------

------------------------------------------------------------------------

**2. Wire Numbering**

The 3-digit number groups wires by system so any number immediately
identifies its domain. Numbers are assigned sequentially within each
range as wires are added to the register.

  ----------- ---------- -------------------- -------------------------
   **Range**   **Code**       **System**             **Devices**

    **100**    **PWR**          Power         BMS, Fuse, Kill Switches,
                                                  Power Board, Buck
                                                  Converters, Fans

    **200**    **DRV**          Drive            Splitter, Brushless
                                                 Controllers, Drive
                                                   Motors, Rocker,
                                                Headlights, Switches

    **300**    **COM**      Communications      Jetson, Raspberry Pi,
                                              Network Switch, USB Hub,
                                               CANable, POE, Antenna,
                                              GPS, UART Board, Pantilt

    **400**    **ARM**           Arm            Arm PD, Arm Box, Arm
                                               Brushed, ESCs, Motors,
                                              Encoders, Limit Switches,
                                                     ToF, Laser

    **500**    **SCI**         Science            Science-Arm board

    **600**    **---**        (reserved)      

    **700**    **---**        (reserved)      

    **800**    **---**        (reserved)      

    **900**    **---**        (reserved)      
  ----------- ---------- -------------------- -------------------------

Ranges 600--900 are reserved for future systems. Do not use them without
updating this document first.

------------------------------------------------------------------------

**3. Wire Type Flag (P / D)**

The single letter after the wire number identifies what the wire
carries:

- P --- Power wire: carries voltage to supply a device (24V, 12V, 5V
  rails, motor power).

- D --- Data wire: carries a signal (CAN, USB, Ethernet, UART, PWM,
  encoder, sensor).

If a cable physically bundles both power and data (e.g. a servo cable
with signal + supply), treat it as P and note the signal type in the
Notes column of the register.

------------------------------------------------------------------------

**4. Device Abbreviation Dictionary**

Use these 3-letter codes for the FROM, TO, and CONN segments. Silkscreen
names are preferred over J-numbers because they are self-describing.
Where the silkscreen is longer than 5 characters, the abbreviated form
below is used in the Wire ID; the full silkscreen text is stored in the
End Connector column of the wire register.

  ---------- ---------------- -------------------- --------------------
   **Code**   **Silkscreen**   **Board / Device**       **System**

   **PWB**     Power Board        Power Board              PWR

   **BMS**         BMS         Battery Management          PWR
                                      Sys.         

   **FUS**         Fuse               Fuse                 PWR

   **MKS**   Kill Switch MKS   Kill Switch (MKS)           PWR

   **SKS**   Kill Switch SKS   Kill Switch (SKS)           PWR

   **BK1**     Buck 24→12V       Buck Converter            PWR
                                     24→12V        

   **BK2**      Buck 24→5V    Buck Converter 24→5V         PWR

   **FAN**         Fans               Fans                 PWR

   **SPL**       Splitter     Drive Splitter Board         DRV

   **BRL**     Brushless L       Brushless Ctrl            DRV
                                     (Left)        

   **BRR**     Brushless R       Brushless Ctrl            DRV
                                    (Right)        

   **BRF**     Brushless F       Brushless Ctrl            DRV
                                    (Front)        

   **MOL**    Drive Motor L    Drive Motor (Left)          DRV

   **MOR**    Drive Motor R   Drive Motor (Right)          DRV

   **MOF**    Drive Motor F   Drive Motor (Front)          DRV

   **RKL**     J17 Rocker L   Rocker Switch (Left)         DRV

   **RKR**     J18 Rocker R      Rocker Switch             DRV
                                    (Right)        

   **HD1**     Headlight 1        Headlight #1             DRV

   **HD2**     Headlight 2        Headlight #2             DRV

   **HD3**     Headlight 3        Headlight #3             DRV

   **SWT**       Switches      Switches (J23 RKS)          DRV

   **JET**      Jetson J6            Jetson                COM

   **RPI**     RBPi ARM J7        Raspberry Pi             COM

   **HAT**        Pi Hat        Raspberry Pi Hat           COM

   **NSW**    Network Switch     Network Switch            COM
                    J8                             

   **HUB**       USB Hub            USB Hub                COM

   **CAN**       CAN J27            CANable                COM

   **POE**         POE            POE Injector             COM

   **ANT**     Antenna J10          Antenna                COM

   **GPS**     GPS1 / GPS2          GPS Unit               COM

   **URT**         UART        UART Board (Sonia)          COM

   **PAN**       Pantilt        Pantilt Assembly           COM

   **PIT**     Pitch Servo        Pitch Servo              COM

   **YAW**      Yaw Servo          Yaw Servo               COM

   **TOC**      ToF sensor    ToF Sensor (Pantilt)         COM
                (Pantilt)                          

   **APD**     Arm PD Board       Arm PD Board             ARM

   **ABX**    Arm Box Board      Arm Box Board             ARM

   **ABR**     Arm Brushed     Arm Brushed Board           ARM
                  Board                            

   **ESE**      Elbow ESC          Elbow ESC               ARM

   **ESS**     Shoulder ESC       Shoulder ESC             ARM

   **ESW**      Waist ESC          Waist ESC               ARM

   **GRM**    Gripper Motor      Gripper Motor             ARM

   **WPM**     Wrist Pitch     Wrist Pitch Motor           ARM
                  Motor                            

   **WRM**   Wrist Roll Motor   Wrist Roll Motor           ARM

   **GRE**   Gripper Encoder    Gripper Encoder            ARM

   **WPE**     Wrist Pitch    Wrist Pitch Encoder          ARM
                 Encoder                           

   **WRE**      Wrist Roll     Wrist Roll Encoder          ARM
                 Encoder                           

   **LS1**    Limit Switch 1     Limit Switch 1            ARM

   **LS2**    Limit Switch 2     Limit Switch 2            ARM

   **LSG**     Limit Switch       Limit Switch             ARM
                 Gripper           (Gripper)       

   **TOA**   ToF sensor (Arm)   ToF Sensor (Arm)           ARM

   **LAS**        Laser              Laser                 ARM

   **SCA**     Arm/Sci J22     Science-Arm Board           SCI
  ---------- ---------------- -------------------- --------------------

When adding a new device, choose a 3-letter code not already in this
table, add it here, and update the wire register legend sheet before
assigning it to any Wire ID.

------------------------------------------------------------------------

**5. Wire Register Spreadsheet**

**5.1 Column Definitions**

The wire register is the single source of truth for all wiring. Each row
is one wire. The columns are:

  ---------------- ----------------------- ---------------- ----------------
     **Column**          **Example**          **Column**      **Example**

      Wire ID       201-P-DRV-PWB-SPL-RKL  End 2 --- Device     Splitter

    Description    Power board to splitter    End 2 ---           RKL
                                              Connector     

       System                DRV                Length            TBD

  End 1 --- Device       Power Board         Gauge (AWG)          TBD

     End 1 ---               J17              Harness ID        H-DRV-01
     Connector                                              

    Wire Colour              Red                Status           DRAFT

                                                Notes       
  ---------------- ----------------------- ---------------- ----------------

**5.2 Status Values**

Every wire must have a status. Never leave it blank.

  -------------- -----------------------------------------------------
    **Status**                        **Meaning**

    **DRAFT**    Wire identified in diagram; length and gauge not yet
                                       confirmed

   **MEASURED**        Physical length measured; gauge selected

     **MADE**               Wire cut, crimped, and labelled

    **ROUTED**            Wire physically installed in rover

   **COMPLETE**           Wire tested and verified end-to-end
  -------------- -----------------------------------------------------

**5.3 Harness IDs**

Wires that are physically bundled together in the same sleeve or conduit
share a Harness ID. Format: H-\[SYS\]-\[NN\], e.g. H-ARM-01. A single
wire with no bundle leaves the Harness ID blank. The harness grouping
does not affect the individual Wire ID.

------------------------------------------------------------------------

**6. Rules & Edge Cases**

- Wire IDs are permanent. Once assigned and entered in the register,
  never change a Wire ID even if the wire is re-routed. Update the
  description and device columns instead.

- No blanks in Wire ID, Type, System, or Status. Use TBD for Length and
  Gauge when not yet known.

- Cross-system wires use the source system code. A power wire going from
  PWB to a drive splitter is P-PWR, not P-DRV.

- Connector names with spaces: remove the space and run the words
  together or use only the most distinctive word (e.g. \'CAN J27\'
  becomes CAN, \'GPS + PanTilt\' becomes GPS).

- Two wires between the same devices on different connectors: they will
  naturally differ in the CONN segment (e.g. 201-P-DRV-PWB-SPL-J1 vs
  202-P-DRV-PWB-SPL-J2). No suffix needed.

- Physical wire labels: print or write the Wire ID on both ends of every
  wire, as close to the connector as possible.

------------------------------------------------------------------------

**7. Quick Reference**

> \[NUM\]-\[TYPE\]-\[SYS\]-\[FROM\]-\[TO\]-\[CONN\]

Real examples from this rover:

> 101-P-PWR-BMS-FUS-IN BMS output to fuse
>
> 201-P-DRV-PWB-SPL-RKL Power board J17 to splitter
>
> 301-D-COM-PWB-CAN-J27 Power board CAN to CANable
>
> 401-P-ARM-PWB-APD-PWR Power board to Arm PD board
>
> 402-D-ARM-ABR-GRM-IN Arm brushed board to gripper motor
>
> 501-D-SCI-PWB-SCA-J22 Power board Arm/Sci to science board
