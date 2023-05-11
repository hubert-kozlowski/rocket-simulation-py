
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


#### Sinusoidal Thrust Function
```py
def sinusoidal_thrust(time):
    amplitude = 5000.0
    frequency = 0.5  # Adjust the frequency to control the oscillation
    return amplitude * math.sin(2 * math.pi * frequency * time)
```
This thrust function generates a sinusoidal thrust variation over time. Users can adjust the amplitude and frequency parameters to create different oscillation patterns.

#### Exponential Thrust Function
```py
def exponential_thrust(time):
    initial_thrust = 5000.0
    decay_rate = 0.2  # Adjust the decay rate to control the exponential decay
    return initial_thrust * math.exp(-decay_rate * time)
```
This thrust function produces an exponential decay in thrust over time. Users can adjust the initial thrust and decay rate parameters to control the rate of decay.

#### Step Function Thrust
```py
def step_thrust(time):
    return 5000.0 if time < 5.0 else 10000.0
```
This thrust function applies a step change in thrust at a specific time. In this example, the thrust is 5000.0 until time reaches 5.0 seconds, after which it increases to 10000.0. Users can modify the time threshold and thrust values to create different step variations.

### Custom Drag Function
The custom drag function takes the __'velocity'__ as input and returns the corresponding drag force at that velocity. Here's an example of a custom drag function:
```py
def custom_drag(velocity):
    return 0.5 * velocity  # Assuming drag coefficient = 0.5
```

#### Quadratic Drag Function
```py
def quadratic_drag(velocity):
    drag_coefficient = 0.5
    return drag_coefficient * velocity**2
```
This drag function introduces a quadratic drag force that increases with the square of the velocity. Users can adjust the drag coefficient parameter to change the strength of the drag effect.

#### Inverse Velocity Drag Function
```py
def inverse_velocity_drag(velocity):
    drag_coefficient = 0.5
    return drag_coefficient / velocity
```
This drag function creates an inverse relationship between drag force and velocity. As the velocity increases, the drag force decreases. Users can adjust the drag coefficient parameter to control the strength of the effect.
