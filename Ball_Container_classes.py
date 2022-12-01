#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:43:30 2019

@author: kev
Kelvin Brinham
Start 24/10/19
Balls in a box project
Sidescript
"""

import numpy as np
import pylab as pl
from random import uniform
import matplotlib.pyplot as plt
import scipy.stats as stats
import Other_functions

class Ball:
    def __init__(self, m = 1, rad = 1, r=[0,0], v=[0,0]):
        self.mass = m
        self.radius = rad
        self.__position = np.array(r)
        self.velocity = np.array(v)
        self.sep = 0
        self.impulse = 0
        self.patch = pl.Circle(self.pos(), self.radius, fc='r')
    def rad(self):
        return self.radius
    def pos(self):
        return self.__position
    def mass(self):
        return self.mass
    def vel(self):
        return self.velocity
    def get_patch(self):
        return self.patch
    def move(self, dt):
        new_pos = self.__position + self.velocity*dt
        self.__position = new_pos
        self.patch.center = self.__position
    def time_to_collision(self, other):
        self.sep = self.pos() - other.pos()
        vrel = self.velocity - other.velocity
        R = self.radius + other.radius
        sep_vrel = np.dot(self.sep, vrel)
        mag_vrel = np.linalg.norm(vrel)
        mag_sep = np.linalg.norm(self.sep)
        dis = sep_vrel**2 - (mag_vrel**2)*(mag_sep**2 - R**2) #Discriminant of the quadratic
        dt = 0
        if dis < 0 :
            return None
        elif dis >= 0: 
            deltat1 = (-sep_vrel + np.sqrt(sep_vrel**2 - (mag_vrel**2)*(mag_sep**2 - R**2)))/mag_vrel**2
            deltat2 = (-sep_vrel - np.sqrt(sep_vrel**2 - (mag_vrel**2)*(mag_sep**2 - R**2)))/mag_vrel**2
            if self.radius or other.radius < 0: #these 5 lines are ball on container returning
                if deltat1 > 0 and deltat2 > 0:#the larger time
                    if deltat1 < deltat2:
                        dt = deltat1
                        return dt - 0.0001 #These 0.0001 times stop balls sticking
                    if deltat2 < deltat1:
                        dt = deltat2
                        return dt - 0.0001
                if deltat1 < 0 and deltat2 < 0:
                    return None
                if deltat1 < 0 and deltat2 > 0:
                    dt = deltat2
                    return dt - 0.0001
                if deltat1 > 0 and deltat2 < 0:
                    dt = deltat1
                    return dt - 0.0001
            if sep_vrel > 0:     #r.v >0 objects traveling away from each other return none
                return None
            if sep_vrel and self.radius and other.radius > 0:
                if deltat1 < deltat2:
                    dt = deltat1
                    return dt - 0.0001
                if deltat2 < deltat1:
                    dt = deltat2
                    return dt - 0.0001   #return smaller roots as balls going towards each other
    def collide(self, other):
        self.sep = (other.pos() - self.pos())
        sephat = self.sep/np.linalg.norm(self.sep)
        v1para = np.dot(self.velocity, sephat)
        v2para = np.dot(other.velocity, sephat)
        v1perp = self.velocity - v1para*sephat
        v2perp = other.velocity - v2para*sephat
        if other.mass == np.inf: #Ball on container collision
            v1paranew = -v1para
            v2paranew = 0
            self.velocity = v1paranew*sephat + v1perp
            other.velocity = v2paranew*sephat + v2perp
            momentum_change = np.linalg.norm(2*self.mass*v1para)
            Simulation.momentum_change_total += momentum_change
        elif self.mass == np.inf: #Ball on contaiuner collision
            v1paranew = 0
            v2paranew = -v2para
            self.velocity = v1paranew*sephat + v1perp
            other.velocity = v2paranew*sephat + v2perp
            momentum_change = np.linalg.norm(2*other.mass*v2para)
            Simulation.momentum_change_total += momentum_change
        else: #Ball on ball collision
            v1paranew = ((self.mass - other.mass)/(self.mass + other.mass))*v1para + (2*other.mass/(self.mass + other.mass))*v2para
            v2paranew = (2*self.mass/(self.mass + other.mass))*v1para + ((other.mass - self.mass)/(self.mass + other.mass))*v2para
            self.velocity = v1paranew*sephat + v1perp
            other.velocity = v2paranew*sephat + v2perp
            
class Container(Ball):
    def __init__(self, m = 1, rad = 10, r=[0,0], v=[0,0]):
        Ball.__init__(self, m, -rad, r, v) #-ve radius so physics equations work
        self.patch = pl.Circle(self.pos(), self.radius, ec='b', fill=False)
        self.volume = np.pi*(self.radius)**2 #Unusual as i say volume but because i work in 2D this gives area
        
