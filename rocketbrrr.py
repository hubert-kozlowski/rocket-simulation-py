import logging
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from rich import print

logging.basicConfig(filename='rocket_simulation.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class RocketSimulation:
    def __init__(self, mass, thrust_func, drag_func):
        """Creates a new RocketSimulation object with the given
        mass, thrust function, and drag function."""
        self.mass = mass
        self.thrust_func = thrust_func
        self.drag_func = drag_func
        self.time = 0.0
        self.latitude = [0.0]  # Start with initial latitude
        self.longitude = [0.0]  # Start with initial longitude
        self.altitude = 0.0
        self.velocity = 0.0
        self.acceleration = 0.0
        self.max_altitude = 0.0
        self.max_temperature = 0.0
        self.earth_radius = 6371000  # Radius of the Earth in meters
        self.angular_velocity = 2 * math.pi / (24 * 60 * 60)  # Angular velocity of the Earth's rotation

        # Variables for plotting
        self.time_data = []
        self.altitude_data = []
        self.velocity_data = []
        self.acceleration_data = []
        self.temperature_data = []

    def update(self, time_step):
        try:
            gravity_force = self.calculate_gravity_force()
            thrust_force = self.thrust_func(self.time)
            drag_force = self.drag_func(self.velocity)

            net_force = thrust_force - drag_force - self.calculate_gravity_force()
            if self.altitude > 100000:  # Check if altitude is above 100 km
                if net_force <= 0:  # Rocket is not achieving sufficient thrust to overcome gravity
                    self.acceleration = -gravity_force / self.mass  # Apply gravitational acceleration
                else:
                    self.acceleration = 0.0  # Rocket is in weightless orbit, set acceleration to zero
            else:
                self.acceleration = net_force / self.mass  # Rocket is below 100 km, consider all forces
            self.velocity += self.acceleration * time_step
            self.altitude += self.velocity * time_step
            self.time += time_step

            if self.altitude < 0:
                self.altitude = 0
                self.velocity = 0

            if self.altitude > self.max_altitude:
                self.max_altitude = self.altitude

            temperature = self.calculate_temperature(self.velocity)
            if temperature > self.max_temperature:
                self.max_temperature = temperature

            # Update latitude and longitude based on curved path and Earth's rotation
            angular_velocity = self.velocity / (self.earth_radius + self.altitude)
            delta_longitude = math.degrees(angular_velocity * time_step)
            delta_latitude = math.degrees(self.angular_velocity * time_step)
            self.longitude.append(self.longitude[-1] + delta_longitude)
            self.latitude.append(self.latitude[-1] + delta_latitude)

            # Append telemetry data for plotting
            self.time_data.append(self.time)
            self.altitude_data.append(self.altitude)
            self.velocity_data.append(self.velocity)
            self.acceleration_data.append(self.acceleration)
            self.temperature_data.append(temperature)

        except Exception as e:
            logging.error(f"[bold red]Error: An error occurred in the RocketSimulation.update method: {str(e)}[/]")

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def calculate_gravity_force(self):
        gravitational_constant = 6.67430e-11  # Gravitational constant in m^3 / (kg * s^2)
        earth_mass = 5.9722e24  # Mass of the Earth in kg
        if self.altitude >= 100000 and self.velocity >= 11186:  # Check if altitude is above 100 km
            return 0.0  # Rocket is in weightless orbit, no gravity
        else:
            return gravitational_constant * self.mass * earth_mass / (self.earth_radius + self.altitude)**2
        

    def calculate_temperature(self, velocity):
        speed_of_sound = 343.0  # Speed of sound in m/s at sea level
        mach_number = velocity / speed_of_sound
        gamma = 1.4  # Specific heat ratio for air
        temperature = 288.0  # Temperature at sea level in Kelvin
        return temperature * (1 + (gamma - 1) * mach_number ** 2 / 2)

# Example thrust and drag functions
def default_thrust(time):
    if time < 5.0:
        return 5000.0 * time
    elif time < 10.0:
        return 25000.0
    else:
        return 0
   
def linear_drag(velocity):
    return 0.5 * velocity  # Assuming drag coefficient = 0.5

# Prompt user for rocket parameters
while True:
    try:
        mass = float(input("Enter the rocket's mass (in kg): "))
        if mass <= 0:
            raise ValueError("[bold red]Mass must be greater than 0.[/]")
        break
    except ValueError as err:
        print(err)

# Prompt user for maximum simulation time
while True:
    try:
        total_time = float(input("Enter the maximum simulation time (in seconds): "))
        if total_time <= 0:
            raise ValueError("[bold red]Maximum time must be greater than 0.[/]")
        break
    except ValueError as err:
        print(err)

# Prompt user for custom thrust function
custom_thrust_input = input("Custom thrust? (yes/no): ")
if custom_thrust_input.lower() == 'yes':
    while True:
        try:
            thrust_func = eval(input("Enter the custom thrust function: "))
            break
        except:
            print("[bold red]Invalid thrust function. Please try again.[/]")
else:
    thrust_func = default_thrust  # Default thrust function (v = 5000t for t < 5s, v = 25000 for t >= 5s)

    # Inform the user about the default thrust function
    print("[bold green]Using default thrust function: v = 5000t for t < 5s, v = 25000 for t >= 5s[/]")

# Prompt user for custom drag function
custom_drag_input = input("Custom drag? (yes/no): ")
if custom_drag_input.lower() == 'yes':
    while True:
        drag_func_input = input("Enter the custom drag function (in terms of 'velocity'): ")
        try:
            drag_func = eval(f"lambda velocity: {drag_func_input}")
            break
        except:
            print("[bold red]Invalid input. Please try again.[/]")
else:
    print("[bold green]Using default drag function: F = 0.5 * v[/]")
    drag_func = linear_drag  # Default drag function

try:
    simulation = RocketSimulation(mass, thrust_func, drag_func)

    time_step = 0.1
    reached_zero_altitude = False
    zero_altitude_time = None
    custom_time_limit = None  # Initialize custom time limit

    while simulation.time < total_time:
        simulation.update(time_step)

        # Check if the altitude has reached zero
        if simulation.altitude <= 0:
            if not reached_zero_altitude:
                reached_zero_altitude = True
                zero_altitude_time = simulation.time
                # Prompt user for a custom time limit after reaching zero altitude (only if not already set)
                if custom_time_limit is None:
                    custom_time_limit = float(input("Enter the custom time limit (in seconds) after reaching zero altitude: "))
            else:
                # Check if the custom time limit (if provided) has passed since hitting zero altitude
                if custom_time_limit is not None and simulation.time - zero_altitude_time >= custom_time_limit:
                    break
                # Check if 5 seconds have passed since hitting zero altitude (default time limit)
                elif custom_time_limit is None and simulation.time - zero_altitude_time >= 5.0:
                    break
        else:
            reached_zero_altitude = False

except Exception as e:
    logging.error(f"[bold red]An error occurred in the main part of the script: {str(e)}[/]")

# Create subplots for Altitude, Velocity, Acceleration, and Temperature
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Altitude vs. Time 
# Dotted line at 0 on y-axis
axes[0, 0].plot(simulation.time_data, simulation.altitude_data, color='blue')
axes[0, 0].set_xlabel('Time (s)')
axes[0, 0].set_ylabel('Altitude (m)')
axes[0, 0].set_title('Altitude vs. Time')
axes[0, 0].grid(True)

# Velocity vs. Time
axes[0, 1].plot(simulation.time_data, simulation.velocity_data, color='orange')
axes[0, 1].set_xlabel('Time (s)')
axes[0, 1].set_ylabel('Velocity (m/s)')
axes[0, 1].set_title('Velocity vs. Time')
axes[0, 1].grid(True)

# Acceleration vs. Time
axes[1, 0].plot(simulation.time_data, simulation.acceleration_data, color='green')
axes[1, 0].set_xlabel('Time (s)')
axes[1, 0].set_ylabel('Acceleration (m/s^2)')
axes[1, 0].set_title('Acceleration vs. Time')
axes[1, 0].grid(True)

# Temperature vs. Time
axes[1, 1].plot(simulation.time_data, simulation.temperature_data, color='red')
axes[1, 1].set_xlabel('Time (s)')
axes[1, 1].set_ylabel('Temperature (K)')
axes[1, 1].set_title('Temperature vs. Time')
axes[1, 1].grid(True)

# Adjust spacing between subplots
plt.tight_layout()

# Rocket Path (3D)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(simulation.longitude[:-1], simulation.latitude[:-1], simulation.altitude_data, color='purple')
ax.set_xlabel('Longitude (degrees)')
ax.set_ylabel('Latitude (degrees)')
ax.set_zlabel('Altitude (m)')
ax.set_title('Rocket Path')
ax.grid(True)

# Show maximum altitude and temperature
print("Maximum Altitude: {:.2f} meters".format(simulation.max_altitude))
print("Maximum Temperature: {:.2f} K".format(simulation.max_temperature))

# Show all the plots
plt.show()