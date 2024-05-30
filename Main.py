#main file waarbij alle losse functies worden opgeroepen en uitgevoerd
#nog niet getest
#import serial
#from Data import data
#from Controller import LQR_control
#from Motoren import motor_drive
#from Plot import real_time_plot
#import time


#duration = 100
#start_time = time.time()
#while time.time() - start_time < duration:
#    theta,z,theta_dot,zdot = data()
#    Fmotor1 = LQR_control(theta, theta_dot)
#    print("F =", Fmotor1, flush=True)
#    speed = motor_drive(Fmotor1, theta_dot)
#    print("Speed = ", speed, flush=True)
#    #real_time_plot()

#Motor = serial.Serial('COM7',9600) #connectie met Arduino
#Motor.write(b'speed')

#main file waarbij alle losse functies worden opgeroepen en uitgevoerd
#nog niet getest wel gecheckt door bert
import serial
from Data import data
from Controller import LQR_control
from Motoren import lengte_pendulum
from Motoren import straal_motor
from Motoren import motor_drive
from Motoren import motor_follow
import time
from Plot import init_real_time_plot, update_real_time_plot

import numpy as np

def check_port_availability(port):
    try:
        ser = serial.Serial(port)
        ser.close()
        return True
    except serial.SerialException as e:
        print(f"Port {port} is not available: {e}")
        return False

# Replace 'COM3' with the port you want to check
port_name = 'COM7'
available = check_port_availability(port_name)
print(f"Port {port_name} is available: {available}")

Leonardo = serial.Serial('COM7',230400) #connectie met Arduino
fig, ax, line_Vy, line_Vz, line_Snelheid_magnitude, line_pps, plott, plotVy, plotVz, plotSnelheid_magnitude, plotpps = init_real_time_plot()
duration = 500
start_time = time.time()
offset_theta = -0.88
offset_z = -1.31


while time.time() - start_time < duration:
    #print(Leonardo.readline().decode())
    #data uit arduino halen
    theta,z,theta_dot,zdot = data(Leonardo)
    
    #data filteren.
    if np.abs(theta_dot) < 6:
        filtered_theta_dot = 0
    else:
        filtered_theta_dot = theta_dot
    if np.abs(zdot) < 6:
        filtered_zdot = 0
    else:
        filtered_zdot = zdot
    #offset:
    filtered_z = z - offset_z
    filtered_theta = theta - offset_theta

    #Rad/s naar m/s
    V_y = filtered_theta_dot * lengte_pendulum
    V_z = filtered_zdot * lengte_pendulum

    #vectoren snelheid omrekenen absolute waarde:
    Snelheid_magnitude = np.sqrt((V_y)**2 + (V_z)**2)
    Richting_motor = np.arctan2(V_y, V_z)

    Fmotor1 = LQR_control(filtered_theta, filtered_theta_dot)
    pps = motor_drive(Fmotor1, Snelheid_magnitude, Richting_motor)
    if pps >-57 and pps < 90:
        pps_filtered = 0
    else:
        pps_filtered = pps
    Leonardo.write(f"{pps_filtered}\n".encode())


    # update the plot
    plott.append(time.time())
    plotVy.append(V_y)
    plotVz.append(V_z)
    plotSnelheid_magnitude.append(Snelheid_magnitude)
    plotpps.append(pps_filtered)
    update_real_time_plot(fig, ax, line_Vy, line_Vz, line_Snelheid_magnitude, line_pps, plott, plotVy, plotVz, plotSnelheid_magnitude, plotpps)

    ##Alle prints
    print ('pps',pps_filtered)
    print(motor_follow(Snelheid_magnitude, Richting_motor))
    print('Richting', Richting_motor)
    print('Snelheid', Snelheid_magnitude)
    
    time.sleep(0.01)
   

print("Finished")
Leonardo.write(f"{0}\n".encode())
