import math
import matplotlib.pyplot as plt
import numpy as np

class RocketSimulation:
    def __init__(self, mass, thrust_func, drag_func):
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

        # Variables for plotting
        self.time_data = []
        self.altitude_data = []
        self.velocity_data = []
        self.acceleration_data = []
        self.temperature_data = []

    def update(self, time_step):
        gravity_force = self.calculate_gravity_force()
        thrust_force = self.thrust_func(self.time)
        drag_force = self.drag_func(self.velocity)

        net_force = thrust_force - drag_force - gravity_force
        self.acceleration = net_force / self.mass
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

        # Update latitude and longitude based on curved path
        angular_velocity = self.velocity / self.earth_radius
        delta_longitude = math.degrees(angular_velocity * time_step)
        self.longitude.append(self.longitude[-1] + delta_longitude)
        self.latitude.append(0.0)  # Dummy value for latitude

        # Append telemetry data for plotting
        self.time_data.append(self.time)
        self.altitude_data.append(self.altitude)
        self.velocity_data.append(self.velocity)
        self.acceleration_data.append(self.acceleration)
        self.temperature_data.append(temperature)

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def calculate_gravity_force(self):
        gravitational_constant = 6.67430e-11  # Gravitational constant in m^3 / (kg * s^2)
        earth_mass = 5.9722e24  # Mass of the Earth in kg
        return gravitational_constant * self.mass * earth_mass / (self.earth_radius + self.altitude)**2

    def calculate_temperature(self, velocity):
        speed_of_sound = 343.0  # Speed of sound in m/s at sea level
        mach_number = velocity / speed_of_sound
        gamma = 1.4  # Specific heat ratio for air
        temperature = 288.0  # Temperature at sea level in Kelvin
        return temperature * (1 + (gamma - 1) * mach_number ** 2 / 2)

# Example thrust and drag functions
def varying_thrust(time):
    if time < 5.0:
        return 5000.0 * time
    elif time < 10.0:
        return 25000.0
    else:
        return 0.0

def linear_drag(velocity):
    return 0.5 * velocity  # Assuming drag coefficient = 0.5

# Prompt user for rocket parameters
mass = float(input("Enter the rocket's mass (in kg): "))

# Prompt user for custom thrust function
custom_thrust_input = input("Custom thrust? (yes/no): ")
if custom_thrust_input.lower() == 'yes':
    thrust_func = eval(input("Enter the custom thrust function: "))
else:
    thrust_func = varying_thrust  # Default thrust function

# Prompt user for custom drag function
custom_drag_input = input("Custom drag? (yes/no): ")
if custom_drag_input.lower() == 'yes':
    drag_func_input = input("Enter the custom drag function (in terms of 'velocity'): ")
    drag_func = eval(f"lambda velocity: {drag_func_input}")
else:
    drag_func = linear_drag  # Default drag function

# Example usage
simulation = RocketSimulation(mass, thrust_func, drag_func)


time_step = 0.1
total_time = 15.0

while simulation.time < total_time:
    simulation.update(time_step)

# Plotting the telemetry data
fig, axs = plt.subplots(3, 2, figsize=(12, 12))
fig.suptitle('Rocket Simulation Telemetry')

# Altitude
axs[0, 0].plot(simulation.time_data, simulation.altitude_data, color='red')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Altitude (m)')
axs[0, 0].set_title('Altitude vs. Time')

# Velocity
axs[0, 1].plot(simulation.time_data, simulation.velocity_data, color='green')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Velocity (m/s)')
axs[0, 1].set_title('Velocity vs. Time')

# Acceleration
axs[1, 0].plot(simulation.time_data, simulation.acceleration_data, color='blue')
axs[1, 0].set_xlabel('Time (s)')
axs[1, 0].set_ylabel('Acceleration (m/s^2)')
axs[1, 0].set_title('Acceleration vs. Time')

# Temperature
axs[1, 1].plot(simulation.time_data, simulation.temperature_data, color='orange')
axs[1, 1].set_xlabel('Time (s)')
axs[1, 1].set_ylabel('Temperature (K)')
axs[1, 1].set_title('Temperature vs. Time')

# Rocket Path (Longitude vs. Latitude)
axs[2, 0].plot(simulation.longitude, simulation.latitude, color='purple')
axs[2, 0].set_xlabel('Longitude (degrees)')
axs[2, 0].set_ylabel('Latitude (degrees)')
axs[2, 0].set_title('Rocket Path')

# Additional Telemetry: Altitude vs. Temperature (Dotted line comparison)
axs[2, 1].plot(simulation.altitude_data, simulation.temperature_data, 'r:', label='Altitude vs. Temperature')
axs[2, 1].set_xlabel('Altitude (m)')
axs[2, 1].set_ylabel('Temperature (K)')
axs[2, 1].set_title('Altitude vs. Temperature')
axs[2, 1].legend()

# Text statistics
peak_apogee = f"Peak Apogee: {simulation.max_altitude:.2f} meters"
max_temperature = f"Max Temperature: {simulation.max_temperature:.2f} K"
axs[2, 1].text(0.5, 0.9, peak_apogee, fontsize=12, ha='center')
axs[2, 1].text(0.5, 0.8, max_temperature, fontsize=12, ha='center')

# Adjusting subplot spacing
fig.subplots_adjust(hspace=0.5, wspace=0.3, top=0.9, bottom=0.1, left=0.1, right=0.9)

# Show the plot
plt.show()
