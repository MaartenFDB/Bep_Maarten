import matplotlib.pyplot as plt
import numpy as np

# Initialize the variables
filtered_theta_dot = 0
filtered_zdot = 0
offset_z = 0
offset_theta = 0
theta_dot = 0
zdot = 0
theta = 0
z = 0

def init_real_time_plot():
    # Create empty lists for the plots
    plott = []
    plotVy = []
    plotVz = []
    plotSnelheid_magnitude = []
    plotpps = []

    # Interactive plot
    plt.ion()
    fig, ax = plt.subplots(3, 1)  # Create 3 subplots

    # Plot for V_y and V_z
    line_Vy, = ax[0].plot(plott, plotVy, label='V_y', color='blue')
    line_Vz, = ax[0].plot(plott, plotVz, label='V_z', color='red')

    # Plot for Snelheid_magnitude
    line_Snelheid_magnitude, = ax[1].plot(plott, plotSnelheid_magnitude, label='Snelheid_magnitude', color='green')

    # Plot for pps
    line_pps, = ax[2].plot(plott, plotpps, label='PPS', color='purple')

    # Set labels and titles
    ax[0].set_xlabel('Tijd')
    ax[0].set_ylabel('V_y, V_z')
    ax[0].set_title('Real-Time Measured V_y and V_z')
    ax[0].legend()

    ax[1].set_xlabel('Tijd')
    ax[1].set_ylabel('Snelheid_magnitude')
    ax[1].set_title('Real-Time Measured Snelheid_magnitude')
    ax[1].legend()

    ax[2].set_xlabel('Tijd')
    ax[2].set_ylabel('PPS')
    ax[2].set_title('Real-Time Measured PPS')
    ax[2].legend()

    return fig, ax, line_Vy, line_Vz, line_Snelheid_magnitude, line_pps, plott, plotVy, plotVz, plotSnelheid_magnitude, plotpps

def update_real_time_plot(fig, ax, line_Vy, line_Vz, line_Snelheid_magnitude, line_pps, plott, plotVy, plotVz, plotSnelheid_magnitude, plotpps):
    line_Vy.set_data(plott, plotVy)
    line_Vz.set_data(plott, plotVz)
    line_Snelheid_magnitude.set_data(plott, plotSnelheid_magnitude)
    line_pps.set_data(plott, plotpps)

    ax[0].relim()
    ax[0].autoscale_view()
    ax[1].relim()
    ax[1].autoscale_view()
    ax[2].relim()
    ax[2].autoscale_view()

    fig.canvas.draw()
    fig.canvas.flush_events()