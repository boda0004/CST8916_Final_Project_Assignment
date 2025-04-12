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
**IoT Sensor Simulation**
To simulate real-time ice monitoring, we created three Python scripts, each acting as a virtual IoT device for a specific location:

dow_lake_simulator.py

fifth_ave_simulator.py

nac_simulator.py

Each script generates random values for:

Ice Thickness (cm)

Surface Temperature (°C)

Snow Accumulation (cm)

External Temperature (°C)

Timestamp (ISO UTC format)

This data is formatted in JSON and sent to Azure IoT Hub using the Azure IoT Device SDK.

**Sample JSON Payload:**

    {
        "location": "Dow's Lake",
        "iceThickness": random.randint(20, 35),
        "surfaceTemperature": random.randint(-10, 1),
        "snowAccumulation": random.randint(0, 15),
        "externalTemperature": random.randint(-15, 4),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
Each script uses a device-specific connection string and pushes data every 10 seconds.

**Azure IoT Hub Configuration**
I created an Azure IoT Hub named RideauSkatewayHub.
Under the hub, I registered three devices:

DowLakeDevice

FifthAveDevice

NACDevice

Each device uses symmetric key authentication and its unique connection string.

Steps Followed:

Created IoT Hub in Canada Central region.

Added devices under IoT Devices tab.

Copied each connection string into its matching simulator script.

Used messages/events as the default endpoint.

**Azure Stream Analytics Job**
I created a Stream Analytics job called SkatewayAnalytics to process incoming sensor data in real-time.

Input Configuration:
Type: IoT Hub

Input Alias: RideauSkatewayHubInput

Serialization: JSON

Encoding: UTF-8

Output Configuration:
Type: Azure Blob Storage

Output Alias: processed-data-blobOutput

Container: processed-data

Format: JSON (line-separated)

Path pattern: skateway/{date}/{time}

Write mode: Append

**Query Logic:**

    SELECT
        location,
        System.Timestamp AS windowEnd,
        AVG(CAST(iceThickness AS float)) AS avgIceThickness,
        MAX(CAST(snowAccumulation AS float)) AS maxSnowAccumulation
    INTO
        [processed-data-blobOutput]
    FROM
        [RideauSkatewayHubInput] TIMESTAMP BY timestamp
    GROUP BY
        TumblingWindow(minute, 5), location

This query uses 5-minute tumbling window to group and analyze data by location.
This allows near real-time aggregation of safety metrics for each monitored location.

# Azure Blob Storage





