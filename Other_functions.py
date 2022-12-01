#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:07:04 2019

@author: kev
"""
import numpy as np
import pylab as pl
import random as ran
from random import uniform
import matplotlib.pyplot as plt
import scipy.stats as stats
import Simulation_class
import Ball_Container_classes

def Kinetic_energy(m, v):
    a = 0.5*m*np.dot(v, v)
    return a 

def rand_ball(r):
    a = 1 #SET BALL STARTING VELOCITY HERE
    rand_v = [ran.uniform(-a, a), ran.uniform(-a, a)] 
    return Ball(1, 0.5, r, rand_v) #Ball(Mass, radius,...) SET BALL MASS AND RADIUS HERE


def multi_ball(no_balls):
    ball_list = [] #list of balls
    list_r = []
    x = 10 #ENSURE TO INPUT CONTAINER RADIUS HERE
    square_side = (2/np.sqrt(2))*x #Size of the largest square that will fit in the circle container
    ball_rad = rand_ball([0,0]).rad() #Ball radius
    i = -0.5*square_side + 0.99*ball_rad
    while i <= (0.5*square_side - 0.99*ball_rad):
        list_r.append([i, ran.uniform((-0.5*square_side + 0.99*ball_rad), (0.5*square_side - 0.99*ball_rad))])
        i += 2.001*ball_rad #Gives each ball a set x coordinate and random y coordinate
    #Max number of balls allowed?
    for n in range(0, no_balls):
        a = rand_ball(list_r[n])#gives new random ball
        ball_list.append(a) #adds new random ball to ball_list
    return ball_list 



    
