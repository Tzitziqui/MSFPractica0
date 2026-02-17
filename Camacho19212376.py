"""
Práctica 0: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Tchandra Yahoel Camacho Llanes
Número de control: 19212376
Correo institucional: l19212376@tijuana.tecnm.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
u1 = np.ones(N) #Step
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1 #Impulse
u3 = t/tend #Ramp
u4 = np.sin(m.pi/2*t) #Sine function

# Componentes del circuito RLC y función de transferencia
R,L,C = 10E3,10E-6,10E-6
num = [1]
den =  [C*L,C*R,1]
sys = ctrl.tf(num,den)
print(f"Funcion de transferencia del sistema: {sys}\n")

# Componentes del controlador
kP,kI,kD = 9.536,317.728,0.029
Cr = 1E-6
Re = 1/(Cr*kI)
Rr = kP*Re
Ce = kD/Rr
print(f"El valor de capacitancia Cr es de {Cr} Faradios.\n")
print(f"El valor de resistencia de Re es de {Re} Ohms.\n")
print(f"El valor de resistencia de Rr es de {Rr} Ohms.\n")
print(f"El valor de capacitancia de Ce es de {Ce} Faradios.\n")

numPID = [Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
denPID = [Re*Cr,0]
PID =ctrl.tf(numPID,denPID)
print(f"Funcion de transferencia del controlador PID: {PID}\n")

# Sistema de control en lazo cerrado
x = ctrl.series(PID,sys)
sysPID = ctrl.feedback(x,1, sign = -1)
print(f"Funcion de transferencia del sistema de control en lazo cerrado: {sysPID}")

# Respuesta del sistema en lazo abierto y en lazo cerrado
_,PAu1 = ctrl.forced_response(sys,t,u1,x0)
_,PAu2 = ctrl.forced_response(sys,t,u2,x0)
_,PAu3 = ctrl.forced_response(sys,t,u3,x0)
_,PAu4 = ctrl.forced_response(sys,t,u4,x0)

_,PIDu1 = ctrl.forced_response(sysPID,t,u1,x0)
_,PIDu2 = ctrl.forced_response(sysPID,t,u2,x0)
_,PIDu3 = ctrl.forced_response(sysPID,t,u3,x0)
_,PIDu4 = ctrl.forced_response(sysPID,t,u4,x0)

clr0 = np.array([10,196,224])/255
clr1 = np.array([133,64,157])/255
clr2 = np.array([238,167,39])/255
clr3 = np.array([255,239,95])/255
clr4 = np.array([66,122,57])/255

fg1 = plt.figure() #Respuesta al escalon
plt.plot(t,u1,'-',color = clr0,label='Pao(t)') #Entrada
plt.plot(t,PAu1,'--',color=clr2,label='PA(t)') #Respuesta en lazo abierto
plt.plot(t,PIDu1,':',color=clr4,label='PID(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center', ncol=3,fontsize=9,frameon=True)
plt.show()
fg1.savefig('step_python.pdf',bbox_inches='tight')

fg2 = plt.figure() #Respuesta al impulso
plt.plot(t,u2,'-',color = clr0,label='Pao(t)') #Entrada
plt.plot(t,PAu2,'--',color=clr2,label='PA(t)') #Respuesta en lazo abierto
plt.plot(t,PIDu2,':',color=clr4,label='PID(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center', ncol=3,fontsize=9,frameon=True)
plt.show()
fg2.savefig('impulse_python.pdf',bbox_inches='tight')

fg3 = plt.figure() #Respuesta al rampa
plt.plot(t,u3,'-',color = clr0,label='Pao(t)') #Entrada
plt.plot(t,PAu3,'--',color=clr2,label='PA(t)') #Respuesta en lazo abierto
plt.plot(t,PIDu3,':',color=clr4,label='PID(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1); plt.yticks(np.arange(0,1.1,0.1))
plt.xlabel('t[s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center', ncol=3,fontsize=9,frameon=True)
plt.show()
fg3.savefig('ramp_python.pdf',bbox_inches='tight')

fg4 = plt.figure() #Respuesta a la funcion sin
plt.plot(t,u4,'-',color = clr0,label='Pao(t)') #Entrada
plt.plot(t,PAu4,'--',color=clr2,label='PA(t)') #Respuesta en lazo abierto
plt.plot(t,PIDu4,':',color=clr4,label='PID(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-1,1); plt.yticks(np.arange(-1,1.1,0.2))
plt.xlabel('t[s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center', ncol=3,fontsize=9,frameon=True)
plt.show()
fg4.savefig('sin_python.pdf',bbox_inches='tight')
