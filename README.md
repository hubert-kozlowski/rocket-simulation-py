# Rocket Simulation

This program simulates the flight of a rocket based on the provided parameters, such as mass, thrust function, and drag function. It calculates the rocket's altitude, velocity, acceleration, and temperature over time and plots the telemetry data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/rocket-simulation.git
   ```
   
2. Change into the project directory:

   ```bash
   cd rocket-simulation
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the program:

   ```bash
   python rocket_simulation.py
   ```
   
2. Enter the rocket's mass when prompted:

   ```bash
   Enter the rocket's mass (in kg): 100.0
   ``` 
   
3. Choose whether to use custom thrust function:

   ```bash
   Custom thrust? (yes/no): yes
   ```    
 If you choose "yes," enter the custom thrust function when prompted. Otherwise, a default thrust function will be used.

Example of a custom thrust function:
```py
Enter the custom thrust function:
def custom_thrust(time):
    if time < 5.0:
        return 5000.0 * time
    elif time < 10.0:
        return 25000.0
    else:
        return 0.0
```

4. Choose whether to use custom drag function:

   ```bash
   Custom drag? (yes/no): no
   ```      
If you choose "yes," enter the custom drag function when prompted. Otherwise, a default drag function will be used.

5. The program will simulate the rocket's flight and display the telemetry data in a plot.

6. Adjust the simulation parameters and the custom thrust and drag functions in the code as needed.


## Custom Thrust and Drag Functions

When prompted for custom thrust and drag functions, you have the option to define your own functions. Ensure that the functions you provide are valid Python functions that take the necessary input and return the corresponding output.

### Custom Thrust Function
The custom thrust function takes the __'time'__ as input and returns the corresponding thrust at that time. Here's an example of a custom thrust function:
```py
def custom_thrust(time):
    if time < 5.0:
        return 5000.0 * time
    elif time < 10.0:
        return 25000.0
    else:
        return 0.0
```

### Custom Drag Function
The custom drag function takes the __'velocity'__ as input and returns the corresponding drag force at that velocity. Here's an example of a custom drag function:
```py
def custom_drag(velocity):
    return 0.5 * velocity  # Assuming drag coefficient = 0.5
```
