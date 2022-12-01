#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:18:27 2019

@author: kev

Kelvin Brinham
Start 24/10/19
Balls in a box project
Mainscript
"""
import numpy as np
import pylab as pl
import random as ran
from random import uniform
import matplotlib.pyplot as plt
import scipy.stats as stats
import Ball_Container_classes
import Other_functions

class Simulation:
    time_total = 0 #Time the simulation has been running
    momentum_change_total = 0 #Adds up total momentum change
    no_container_collisions = 0 #Adds up total number of container collision
    
    def __init__(self, n): #n = number of balls
        self.n_balls = n
        #SET CONTAINER RADIUS IN LINE BELOW 'Container(np.inf, RADIUS,...)
        self.cont = Container(np.inf, 10, [0,0], [0,0])#Container with infinite mass, radius 10 and [0,0] position and velocity
        self.list_total = multi_ball(self.n_balls) #Creates list of n balls
        self.list_total.append(self.cont) #Adds container to list of n balls so list contains n+1 objects
        self.ball_mass = self.list_total[0].mass #Mass of an individual ball
        self.square_side = (2/np.sqrt(2))*self.cont.radius #Length of the side of the biggest square that fits into the container
        ball_radius = self.list_total[0].radius #Radius of an individual ball
        self.max_num_balls = -(self.square_side - 1.98*ball_radius)/(2.001*ball_radius) - 1 #Calculates the max number of balls that can fit into the container
        print('Max number of balls:', int(self.max_num_balls))
    
    def next_collision(self):
        i = 0
        dts = []#list of [T, i, o]/ time, T, and corrisponding balls/container that collide
        list_of_times_only = [a[0] for a in dts] #list of just T's which are numbers
        while i <= self.n_balls:
            o = 0
            while o <= self.n_balls:
                if i == o:
                    o += 1
                else:
                    T = self.list_total[o].time_to_collision(self.list_total[i]) #Iterates over list_total 
                    list_of_times_only = [a[0] for a in dts]
                    if T in list_of_times_only or T == None or T <= 0: 
                        o += 1
                    else:
                        dts.append([T, i, o]) 
                        o += 1
            i += 1
        list_of_times_only = [a[0] for a in dts] #list of just T's which are numbers
        min_time = min(list_of_times_only) #Time to next collision
        colliding_object = dts[list_of_times_only.index(min_time)] #[T, i, o] for colliding objects
        self.collider = self.list_total[colliding_object[1]] #1st colliding object 
        self.collidee = self.list_total[colliding_object[2]] #2nd colliding object
        for c in range(self.n_balls + 1): #Iterates over list_total to move each ball to the time of the next collision
            self.list_total[c].move(min_time) 
        if self.collidee.mass != np.inf and self.collider.mass != np.inf: #2 balls are colliding
            KE_collidee = Kinetic_energy(self.collidee.mass, self.collidee.vel())
            KE_collider = Kinetic_energy(self.collider.mass, self.collider.vel())
        else:
            if self.collidee.mass == np.inf: #Ball is colliding with container
                KE_collider = Kinetic_energy(self.collider.mass, self.collider.vel())
                KE_collidee = 0
                self.no_container_collisions += 1
            else:                           #Ball is colliding with container
                KE_collidee = Kinetic_energy(self.collidee.mass, self.collidee.vel())
                KE_collider = 0     
                self.no_container_collisions += 1
        KE_bef = KE_collidee + KE_collider#Kinetic energy of collising objects before collision
        self.time_total += min_time #Adds time between collsiions to the total 'timer'
        self.collidee.collide(self.collider) #Collides the 2 objects
        KE_aft = KE_collidee + KE_collider #Kinetic energy of collising objects after collision
        if (KE_aft - KE_bef) != 0:
            print('Kinetic Energy not conserved!')
    
    def run(self, num_frames, animate=False):
        self.number_of_frames = num_frames 
        self.KE_Total_list = [] #List of total KE for each collision
        self.Temp_Total_list = []#list of total temperature for each collision
        if animate:
            f = pl.figure(figsize=(5,5))
            ax = pl.axes(xlim=(self.cont.radius,-self.cont.radius), ylim=(self.cont.radius,-self.cont.radius)) #-ve signs because container has -ve radius, sets frame size to size of the container
            ax.add_artist(self.cont.get_patch())
            for b in range(0, self.n_balls):
                ax.add_patch(self.list_total[b].get_patch()) #Iterates to add each balls patch
        for frame in range(num_frames):
            self.next_collision()
            self.KE_Total_list.append(Simulation.KE_work(self))
            self.Temp_Total_list.append(Simulation.Temperature_work(self))
            if animate:
                pl.pause(0.01)
        if animate:
            pl.show()
    
    def KE(self):
        return self.KE_Total_list #list of total KE for each collisiom
    
    def Temperature(self):
        return self.Temp_Total_list #list of Temperature for each collision
   
    def speeds(self):
        self.speeds = [] #Speeds = magnatude(velocities)
        for i in range(0, self.n_balls):
            speed = np.linalg.norm([self.list_total[i].vel()[0], self.list_total[i].vel()[1]])
            self.speeds.append(speed)
        return self.speeds
    
    def KE_work(self):
        KE_list = []
        for a in range(0, self.n_balls):
            b = Kinetic_energy(self.list_total[a].mass, self.list_total[a].vel())
            KE_list.append(b)
        self.KE_total_each = np.average(KE_list)
        return self.KE_total_each
    
    def Temperature_work(self):
        N = self.n_balls
        Kb = 1.38064852*10**-23
        a = ((self.KE_total_each)/(N*Kb))
        return a
    
    def Pressure(self):
        circumference = 2*np.pi*-self.cont.radius
        if self.no_container_collisions == 0:
            return 'Pressure = 0 as no balls struck the container walls'
        else:
            a = (self.momentum_change_total)/(self.time_total*circumference)
            return a
    



