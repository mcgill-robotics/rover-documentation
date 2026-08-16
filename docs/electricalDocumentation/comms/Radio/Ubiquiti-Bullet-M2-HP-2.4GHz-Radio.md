

# **Rover 2025-2026**

# **Bullet M2 HP 2.4GHz Radio**

# **Documentation**

# **Overview**

The Ubiquiti Bullet M2 HP is a 2.4GHz radio. The rover has two of these. You interface with them through ethernet, which also powers them through PoE. 

The radios on the rover run in bridge mode, allowing them to function as simple pass-through devices. This means the two radios can communicate as if they were physically wired together, and you can treat the wireless communication as a blackbox. 

# **Setup**

**RADIO IP:** 			192.168.1.20  
**IPv4 Mask/Subnet Mask:** 	255.255.255.0  
**USERNAME:** 			mcgillrobotics  
**PASSWORD:** 			mcgillrobotics

The radio connects and receives power via PoE. If you plan to connect it to your personal machine, use the PoE adapter in the Antenna box. The one that says **Broken** is actually broken. Don’t use it. Connect the male end to your machine, female end through another cable to the radio, and the power into the wall. 

To connect to it on your machine, you’ll have to be on the same ip subnet, i.e. 192.168.1.x. To set this, you can go into your machine’s ethernet settings and assign a static IP.   
For the subnet mask you can put 255.255.255.0.   
For Default and Preferred gateway, put the radio’s ip address, i.e. 192.168.1.20.

# **Accessing airOS**

Once you’ve completed setup, and the radio is connected to your machine, you can access airOS through your web browser. Search the radio’s ip address in the URL bar, and you’ll be presented with the login. 

# **Recovering from a reset**

If the radios ever reset (**Known to happen during comp)**, you must reupload the config file. This is done in the **System** tab of airOS. There is an upload configuration button where you can attach the [bullet\_config.cfg](https://drive.google.com/file/d/1HJwPbppJpnZPwnQAKg1hCx2gWH6Ecn9J/view?usp=drive_link) file from the radio documentation folder of the drive.  
