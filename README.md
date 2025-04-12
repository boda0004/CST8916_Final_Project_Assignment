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

- Type: IoT Hub

- Input Alias: RideauSkatewayHubInput

- Serialization: JSON

- Encoding: UTF-8

Output Configuration:

- Type: Azure Blob Storage

- Output Alias: processed-data-blobOutput

- Container: processed-data

- Format: JSON (line-separated)

- Path pattern: skateway/{date}/{time}

- Write mode: Append

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
Processed data is saved in an Azure Storage account (rideauskatewaystore) under a container called processed-data.

**Folder Structure**

    skateway/YYYY/MM/DD/HH/
    
**File Format:** JSON 

**Example Blob Path:**

    skateway/2025/04/09/17/
**Sample Output JSON:**

    {
      "location": "Dow's Lake",
      "windowEnd": "2025-04-09T17:40:00Z",
      "avgIceThickness": 27.2,
      "maxSnowAccumulation": 14
    }

# Usage Instructions:

**Running the IoT Sensor Simulation**
1.Install dependencies

    pip install azure-iot-device

Navigate to the sensor-simulation/ directory in your project folder.

Open three terminal windows or tabs, one for each script.

Run each script using:

    python dow_lake_simulator.py
    python fifth_ave_simulator.py
    python nac_simulator.py

The scripts will send live telemetry (every 10 seconds) to the Azure IoT Hub using each device’s unique connection string.


**Configuring Azure Services**

**IoT Hub Setup**

- Go to the Azure Portal

- Search and create a new IoT Hub (region: Canada Central)

- Under the IoT Hub:

  - Navigate to IoT Devices

  - Click + New to create:

   - DowLakeDevice

   - FifthAveDevice

   - NACDevice

Copy and paste each connection string into the appropriate Python script


**Stream Analytics Job Setup**

Create a Stream Analytics Job (name: SkatewayAnalytics)

Under Inputs:

- Add a new input of type IoT Hub

- Set alias to RideauSkatewayHubInput

- Select All Devices and JSON format

Under Outputs:

- Add an output of type Blob Storage

- Set alias: processed-data-blobOutput

- Use your existing storage account and container processed-data

- Format: JSON, line separated

- Path pattern: skateway/{date}/{time}

Under Query, paste the following:

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

- Click Save Query, then Start Job > Choose Now > Start

**Accessing Stored Data in Blob Storage**

- Go to your Storage Account in Azure

- Open the Containers section and select processed-data

- Navigate the folders based on the date and hour:

        skateway/2025/04/09/17/

- Open or download the output files (JSON or CSV)

  - Each file contains results grouped by location and time window

  - Use tools like Notepad, VS Code, or Excel to view the data

- Example file content:

        {
          "location": "Fifth Avenue",
          "windowEnd": "2025-04-09T17:45:00Z",
          "avgIceThickness": 28.4,
          "maxSnowAccumulation": 13
        }

# Results:

After we operated the counterfeit IoT sensors and transmitted the data via Azure Stream Analytics, the system functioned effectively and provided us with a summary of the outcomes every 5 minutes for each location: Dow’s Lake, Fifth Avenue, and NAC.

**Key Findings:**

- The system captured real-time ice safety data at 10-second intervals.

- Data was aggregated in 5-minute windows by location using Stream Analytics.

- Results include:

  - Average Ice Thickness

  - Maximum Snow Accumulation

**Sample Output (from Azure Blob Storage)**

Container Path:

    skateway/2025/04/09/17/

Sample JSON File:

    {
      "location": "Dow's Lake",
      "windowEnd": "2025-04-09T17:45:00Z",
      "avgIceThickness": 27.6,
      "maxSnowAccumulation": 12
    }


This output confirms that the system is:

- Grouping data correctly by location

- Capturing trends across time

- Ready for future use in dashboards, alerts, or decision-making tools


# Reflection

**Challenges Faced:**

Start Job Button Not Working (Azure Stream Analytics).

At one time, the “Start job” button in the Azure portal appeared to be disabled, even though all configurations were correct.
Fix: The problem was fixed by saving the query, refreshing the portal, and initiating the job from the Overview tab or by utilizing the Azure CLI.

Real-Time Data Testing.

Emulating three distinct IoT devices necessitated executing several scripts concurrently and observing their output separately.
Fix: Launched three terminal windows and executed each script with the correct device connection string.

Azure IoT Hub Configuration Confusion.

Determining which connection string to apply to each device was initially perplexing.
Fix: Diligently aligned each device’s connection string with the appropriate script and included comments in the code.

Blob Storage Output Structure.

The original folder path and output configuration needed verification to make sure that files were correctly saved and accessible.
Fix: Modified the path pattern and verified that data was saved in line-separated JSON format for straightforward parsing.


# 





