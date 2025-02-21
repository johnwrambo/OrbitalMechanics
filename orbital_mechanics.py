import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg instead of InterAgg
from datetime import datetime
import time


def log_time(func):
    def wrapper():
        current_date_and_time = datetime.now()
        start = time.time()
        steps = func()
        end = time.time()
        total_time = end - start
        with open("log.txt", "a") as file:  # "w" mode creates or overwrites the file
            file.write(f"Ran code at {current_date_and_time}, with {steps} steps, and a total run time: {total_time}...\n")
        print(f"Total run time: {total_time}...")

    return wrapper


@log_time
def main():
    steps = 50000
    dt = .1
    # sun_mass = float(1.989E30)
    earth_radius = 6371E3
    altitude = 370000
    orbital_alt = altitude + earth_radius
    earth_mass = float(5.972E24)
    r = float(42164)
    x = orbital_alt
    y = 0
    z = 0
    G = float(6.67E-11)
    satellite_pos = np.array([x, y, z])
    satellite_velocity = 7778.496  # m/s
    print(type(G))
    gravity_unit_vec = np.array([-1, y / r, z / r])
    satellite_velocity_vec = np.array([0, satellite_velocity, 0])
    a = ((G * earth_mass) / orbital_alt ** 2) * gravity_unit_vec

    # t = np.arange(0,100000,5)
    x_pos_list = []
    y_pos_list = []
    # print(f"POS: {satellite_pos}")
    for _ in range(steps):
        # print(f"Gravity Vec: {gravity_unit_vec}")
        # print(f"Acceleration: {a}")
        a = ((G * earth_mass) / np.linalg.norm(satellite_pos) ** 2) * gravity_unit_vec
        # check = input("enter")
        # if check == "s":
        #     break
        satellite_velocity_vec = satellite_velocity_vec + a * dt
        # print(f"Velocity: {v}")
        satellite_pos += satellite_velocity_vec * dt
        # print(f"POS: {satellite_pos}")
        gravity_unit_vec = (np.array([0, 0, 0]) - satellite_pos) / (np.linalg.norm(satellite_pos - np.array([0, 0, 0])))
        # print(f"new gravity Vec: {gravity_unit_vec}")
        # print(f"Gravity mag: {np.linalg.norm(gravity_unit_vec)}")
        x_pos_list.append(satellite_pos[0])
        y_pos_list.append(satellite_pos[1])

    # Create figure and axis
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')


    # Plot orbit path
    ax.plot(x_pos_list, y_pos_list, label="Path")
    ax.plot(x_pos_list[-1], y_pos_list[-1], label="Space Craft", marker="o", markersize=2, color="red")
    # Plot gravity vector
    gravity_unit_vec = gravity_unit_vec * 1000000
    # ax.plot([x_pos_list[-1], (x_pos_list[-1] + gravity_unit_vec[0])],
    #         [y_pos_list[-1], (y_pos_list[-1] + gravity_unit_vec[1])], label="Gravity",
    #         marker='.')  # Scale for visibility

    # Plot origin (Earth center)
    earth_img = mpimg.imread("earth.png")
    ax.imshow(earth_img, extent=[-earth_radius, earth_radius, -earth_radius, earth_radius])
    # ax.plot(0, 0, label="Origin", marker="o", markersize=6, color="blue")

    # Add a circle for Earth
    # earth_circle = plt.Circle((0, 0), earth_radius, color='b', fill=True)
    # ax.add_patch(earth_circle)  # Add circle to the axes

    # Formatting
    scale = 1e7
    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.set_aspect('equal')  # Ensure 1:1 aspect ratio
    plt.grid(False)
    plt.legend()
    plt.title('Orbit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    return steps

if __name__ == '__main__':
    main()
