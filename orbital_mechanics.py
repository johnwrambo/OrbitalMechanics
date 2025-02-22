import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib

matplotlib.use('TkAgg')  # Use TkAgg instead of InterAgg
from datetime import datetime
import time


def log_time(func):
    """Decorator that logs the execution time and run time of the function."""

    def wrapper():
        current_date_and_time = datetime.now()
        start = time.time()
        steps = func()
        end = time.time()
        total_time = end - start
        with open("log.txt", "a") as file:  # "w" mode creates or overwrites the file
            file.write(
                f"Ran code at {current_date_and_time}, with {steps} steps, and a total run time: {total_time}...\n")
        print(f"Total run time: {total_time}...")

    return wrapper


@log_time
def main():
    steps = 50000
    inspace = True

    earth_radius = 6371E3
    if inspace:
        altitude = 370000
        orbital_alt = earth_radius
        x = orbital_alt + altitude
        y = 0
        z = 0
        satellite_pos = np.array([x, y, z])
        satellite_velocity = 7778.496  # m/s
        satellite_velocity_vec = np.array([0, satellite_velocity, 0])
        # This part is not yet working
    else:
        print("Launch")
        angle = np.radians(15)
        altitude = 370000
        # orbital_alt = altitude + earth_radius
        x = earth_radius
        y = 0
        z = 0
        satellite_pos = np.array([x, y, z])
        satellite_velocity = 0  # m/s
        satellite_velocity_vec = np.array([satellite_velocity * np.cos(angle), satellite_velocity * np.sin(angle), 0])

    dt = .1  #time step
    earth_mass = float(5.972E24)
    G = float(6.67E-11)
    gravity_unit_vec = np.array([-1, 0, 0])
    x_pos_list = []
    y_pos_list = []

    for _ in range(steps):
        a = ((G * earth_mass) / np.linalg.norm(satellite_pos) ** 2) * gravity_unit_vec

        satellite_velocity_vec = satellite_velocity_vec + a * dt

        satellite_pos += satellite_velocity_vec * dt

        gravity_unit_vec = (np.array([0, 0, 0]) - satellite_pos) / (np.linalg.norm(satellite_pos - np.array([0, 0, 0])))

        x_pos_list.append(satellite_pos[0])
        y_pos_list.append(satellite_pos[1])

    # Create figure and axis
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    pos1 = [x_pos_list[-1], y_pos_list[-1]]
    pos2 = pos1 / np.linalg.norm(pos1)
    pos3 = pos2 * earth_radius

    # Plot orbit path
    ax.plot(x_pos_list, y_pos_list, label="Path")
    ax.plot(x_pos_list[-1], y_pos_list[-1], label="Space Craft", marker="o", markersize=2, color="red")

    # Place earth image at origin
    earth_img = mpimg.imread("earth.png")
    earth_radius += 850000  # Needed to adjust image size for visually accuracy
    ax.imshow(earth_img, extent=[-earth_radius, earth_radius, -earth_radius, earth_radius])

    # Formatting plots
    scale = 1e7
    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.set_aspect('equal')  # Ensure 1:1 aspect ratio
    plt.grid(False)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.title('Orbit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    return steps


if __name__ == '__main__':
    main()
