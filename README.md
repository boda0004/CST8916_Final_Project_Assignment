# CST8916_Final_Project_Assignment

# Scenario Description:

In winter people like to go skate on Rideau Cana; Skateway. But It need to assessed the thickness, surface temperature, and amount of snow accumulation periodically so that skater are safe while skating.

Most of this test are done manually .This process take too much time and there is possibility of human error or over look some unexpected changes which could lead to unexpected accidents. That's why I build a system that will provides us with the real-time data and all of this is done automatically so it remove the possibility of human error.

**How it work:-**

I have design 3 sensors for 3 different location (Dow's Lake, Fifth Avenue, and NAC).
The Azure IoT Hub will receives real-time data of weather and ice data from these sensors.
All the data will be examined by Azure Stream Analytics every 5 min.
All the findings is gonna store in azure blob storage so we can determine whether the condition is safe for the skater or not.
This system facilitates quicker and more precious findings which will help National Capital Commission in making a safer decision for the skaters

# System Architecture:
![Rideau Canal drawio1](https://github.com/user-attachments/assets/0a95f3e8-77fe-45ee-a4fe-9c9e436c3994)

# Implementation Details:
** IoT Sensor Simulation **



