import numpy as np
import control as ct
from control import matlab as cm
import matplotlib.pyplot as plt


## Variables
g = 9.81
l = 0.5 #m
m = 0.5 #kg


## ABCD Matrices
A = np.array([[ 0 , -g/l], [1, 0]]);

B = np.array([[0],[1/(m*l)]]);

C = np.array([[0, 1]]);

D = np.array([0]);

## Q matrix en R matrix

Q = np.array([[1, 0],
              [0, 1]]);

R = np.array([[1]]);

#Maak het systeem
sys = ct.ss(A, B, C, D);

#Definieer inputs en outputs en states

states = ["theta_dot", "theta"]
inputs = ["Fmotor1"]
outputs = ["theta"]

#Bereken de K-matrix
K, _, _ = ct.lqr(A, B, Q, R);

#Bereken de nieuwe A en B matrixen
A_aug = A - B@K

#Nieuw LQR systeem: 
syslqr = ct.ss(A_aug, B, C, D, states=states, input=inputs, output=outputs); 
print(syslqr);

#Check of reachable
# Calculate the controllability matrix
#Cm = ct.ctrb(A, B)

# Check if the system is reachable
#rank_Cm = np.linalg.matrix_rank(Cm)
#is_reachable = rank_Cm == A.shape[0]

#print("Controllability Matrix:")
#print(Cm)
#print("Rank of the Controllability Matrix:", rank_Cm)
#print("Is the system reachable?", is_reachable)

#Functie LQR die de berekening doet en de waarden voor de motorkracht teruggeeft
def LQR_control(theta_dot, theta):
    x =  np.array([[theta_dot], [theta]])
    Fmotor1 = -K @ x
    if Fmotor1 > 0:
        Fmotor1 = 0
    return Fmotor1

# Voorbeeldwaarden, moet echte sensorwaarden in
#theta_dot_example = 0.1  # Example angular velocity in rad/s
#theta_example = 0.05  # Example angle in rad
#Fmotor1 = LQR_control(theta_dot_example, theta_example)
#print("Motor force needed:", Fmotor1)
