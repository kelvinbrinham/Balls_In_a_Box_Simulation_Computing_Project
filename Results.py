#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:59:02 2019

@author: kev
"""

import Simulation_class
import Ball_Container_classes
import Other_functions

a = Simulation(3) #number of balls
a.run(10, True) #number of frames, animate True or False
Kinetic_energies = a.KE()
speeds = a.speeds()
print(np.std(speeds)) #Standard deviation of ball speeds
temp = np.average(a.Temperature()) #Avarege so it returns 1 value but Temperature is constant
p = a.Pressure()
print(a.Pressure())
print('Kinetic energy =', np.average(a.KE())) #Returns average but total KE is constant
print('Temperature =', np.average(a.Temperature())) #Returns avergae but Temperature is constant

#
#Plots histogram and fits a maxwell boltxmann
plt.plot(np.arange(1, a.n_balls + 1), speeds)
maxwell = stats.maxwell
params = maxwell.fit(speeds, floc=0)
x = np.linspace(0, 1.4, 100)
plt.hist(speeds, bins=20, normed=True)
plt.plot(x, maxwell.pdf(x, *params), lw = 3)
plt.xlabel('')
plt.ylabel('')
plt.title('')
#%%
#Plots straight line relationships
fit, cov = np.polyfit(c, 1/np.array(Pressures), 1, cov=True)
sig_0 = np.sqrt(cov[0,0])
sig_1 = np.sqrt(cov[1,1])
Y = np.poly1d(fit)
plt.plot(c, Y(c))
plt.title('Volume against 1/P')
plt.plot(c, 1/np.array(Pressures), 'x')
plt.savefig('Volume_against_1/P_VDW_1000_20.JPEG')
print('y intercept', Y(0))
