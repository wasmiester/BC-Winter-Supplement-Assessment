### **README.txt**

#### **Project: Winter Supplement Rules Engine**

This project is a rules engine for determining eligibility and calculating the Winter Supplement benefit for various client scenarios. It uses an event-driven architecture, integrates with an MQTT broker, and includes unit tests for verification.

---

### **Setup Instructions**

1. **Prerequisites**  
   Ensure the following are installed on your system:
   - Python 3.8 or later
   - `pip` (Python package manager)

2. **Clone the Repository**  
   Clone the project files to your local machine:
   ```bash
   git clone https://github.com/wasmiester/BC-Winter-Supplement-Assessment/tree/main
   cd BC-Winter-Supplement-Assessment
   ```

3. **Install Dependencies**  
   Install the required Python libraries by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**  
   Create a `.env` file in the root directory and include the following variables:
   ```plaintext
   MQTT_BROKER=test.mosquitto.org
   MQTT_PORT=1883
   ```
   Update these values if connecting to a different broker.

---

### **Execution Instructions**

1. **Run the Rules Engine**  
   Execute the main script to start the rules engine. Provide the MQTT topic ID as a command-line argument:
   ```bash
   python main.py <MQTT_TOPIC_ID>
   ```
   Replace `<MQTT_TOPIC_ID>` with the unique topic ID provided by the Winter Supplement Calculator web application.

2. **MQTT Communication**  
   The engine listens for input data on:
   ```plaintext
   BRE/calculateWinterSupplementInput/<MQTT_TOPIC_ID>
   ```
   It publishes output data to:
   ```plaintext
   BRE/calculateWinterSupplementOutput/<MQTT_TOPIC_ID>
   ```

3. **Input Data Format**  
   Ensure input JSON follows this schema:
   ```json
   {
       "id": "str", 
       "numberOfChildren": "int",
       "familyComposition": "str", 
       "familyUnitInPayForDecember": "bool"
   }
   ```

4. **Output Data Format**  
   The engine generates JSON in this format:
   ```json
   {
       "id": "str", 
       "isEligible": "bool", 
       "baseAmount": "float", 
       "childrenAmount": "float", 
       "supplementAmount": "float"
   }
   ```

---

### **Testing Instructions**

1. **Unit Tests**  
   Unit tests are provided for both the core calculation logic and MQTT integration.

2. **Run the Tests**  
   Execute the tests using the following command:
   ```bash
   python -m unittest test_main.py
   ```

3. **Expected Test Output**  
   Each test prints an "OK" message on success. For example:
  ![image](https://github.com/user-attachments/assets/84949fe0-1899-435e-b6b4-7bc485d9223c)


4. **Test Coverage**  
   - Verifies eligibility determination based on the `familyUnitInPayForDecember` field.
   - Validates supplement amount calculations for various scenarios.
   - Tests MQTT message handling and data publication.

---

### **Troubleshooting**

1. **Connection Issues**  
   If the engine fails to connect to the MQTT broker, verify:
   - The broker address and port in the `.env` file.
   - Internet connectivity.

2. **No Messages Received**  
   Ensure the Winter Supplement Calculator is publishing input data to the correct MQTT topic. I was unable to receive messages via the web app broker, but the calculations are functioning correctly when retrieving the ID using the wildcard '#'

3. **Test Failures**  
   Re-check your `calculate_winter_supplement` function logic or MQTT integration.
