# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 18:17:48 2019

@author: Austin
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout

from kivy.uix.carousel import Carousel
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.core.window import Window

from kivy.graphics import Line, Rectangle, Color
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
import numpy as np
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock

Builder.load_string("""
<particleGen@RelativeLayout>:                    
    canvas:
        Color:
            rgba:1,1,1,1
        Ellipse:
            size:30,30
            pos:root.ParticlePosX,root.ParticlePosY



<ParticleBox>:


<glassWindow>:
    particle_box:_particleBox
    grid1:_grid1
    grid2:_grid2
    vslide:_vslide
    GridLayout:
        id:_grid1
        cols:2
        GridLayout:
            id:_grid2
            cols:2
            size_hint_x: None
            width: 300
            Label:
                markup:True
                text:'[size=24px][color=#ffffff][b]pressure[/b][/color][/size]'
            Label:
                markup:True
                text:'[size=24px][color=#ff0000][b]'+str(root.particle_box.avgPressure)+'[/b][/color][/size]'
                pos:5,5
            Label:
                markup:True
                text:'[size=24px][color=#ffffff][b]Temperature[/b][/color][/size]'
            Slider:
                id: _vslide
                value: 200
                range: (100,1000)
                step: 10
            Label:
                markup:True
                text:'[size=24px][color=#ffffff][b]Value[/b][/color][/size]'  
            Label:
                markup:True
                text:'[size=24px][color=#ffffff][b]'+str(root.particle_box.temperature)+'[/b][/color][/size]'      
        ParticleBox:
            id:_particleBox
            size:self.size
            pos:self.pos



""")
import random
import numpy as np

global pressure
pressure = 0


class pressureReader(Label):
    pass


class particleGen(RelativeLayout):
    ParticlePosX = NumericProperty(0)
    ParticlePosY = NumericProperty(0)
    velocity = NumericProperty(0)

    def __init__(self, **kwargs):
        super(particleGen, self).__init__(**kwargs)
        self.ParticlePosX = 50
        self.ParticlePosY = 50
        self.velocity = 0
        self.velocityX = 0
        self.velocityY = 0
        self.accelerationX = 1
        self.accelerationY = 1
        self.mass = 1
        self.schedule_events()


    def schedule_events(self):
        Clock.schedule_interval(self.moveParticle, 0.05)

    def moveParticle(self, dt):
        # first move particles
        self.ParticlePosX += self.velocityX * dt + 0.5 * self.accelerationX * dt * dt
        self.ParticlePosY += self.velocityY * dt + 0.5 * self.accelerationY * dt * dt
        # then check if particles have hit wall.
        # if they have then
        if self.ParticlePosY > self.parent.height:
            self.parent.pressure += self.mass * 2 * (abs(self.velocityY)) / dt
            self.ParticlePosY = self.parent.height
            self.velocityY = -self.velocityY
        elif self.ParticlePosY < 0:
            self.parent.pressure += self.mass * 2 * (abs(self.velocityY)) / dt
            self.ParticlePosY = 0
            self.velocityY = -self.velocityY
        if self.ParticlePosX > self.parent.width:
            self.parent.pressure += self.mass * 2 * (abs(self.velocityX)) / dt
            self.ParticlePosX = self.parent.width
            self.velocityX = -self.velocityX
        elif self.ParticlePosX < 0:
            self.parent.pressure += self.mass * 2 * (abs(self.velocityX)) / dt
            self.ParticlePosX = 0
            self.velocityX = -self.velocityX

    pass


class ParticleBox(RelativeLayout):
    pressure = NumericProperty(0)
    avgPressure = NumericProperty(0)
    velocity = NumericProperty(200)
    temperature = NumericProperty((1/1000)*0.5*200**2)
    number_particles = NumericProperty(200)
    def __init__(self, **kwargs):
        super(ParticleBox, self).__init__(**kwargs)
        # ccreate list of widgets
        self.particlesInBox = []
        self.size = (800, 600)
        self.velocity = 200
        self.temperature = (1/1000)*0.5*self.velocity**2
        self.number_particles = 200
        for i in range(self.number_particles):
            particle = particleGen()
            particle.ParticlePosX = self.width * np.random.random()
            particle.ParticlePosY = self.height * np.random.random()
            particle.velocityX = self.velocity * random.choice([-1, 1]) * np.random.random()
            particle.velocityX = self.velocity * random.choice([-1, 1]) * np.random.random()
            particle.accelerationX = 1 ** random.choice([-1, 1]) * np.random.random()
            particle.accelerationY = 1 ** random.choice([-1, 1]) * np.random.random()
            self.particlesInBox.append(particle)
            self.add_widget(particle)
            self.pressure = 0
            self.avgPressure = 0

        self.schedule_events()


    def schedule_events(self):
        #        Clock.schedule_interval(lambda dt: self.checkPressure(), 2)
        Clock.schedule_interval(self.checkPressure, 2)
        Clock.schedule_interval(self.check_velocity, 0.5)
        Clock.schedule_interval(self.check_number, 0.5)

    def checkPressure(self, dt):
        oldPressure = self.pressure
        self.avgPressure = int(oldPressure / 1000)
        print(oldPressure)
        self.pressure = 0

    def check_number(self, dt):
        oldPressure = self.pressure
        self.avgPressure = int(oldPressure / 1000)
        print(oldPressure)
        self.pressure = 0

    def check_velocity(self, dt):
        if self.velocity != self.parent.parent.vslide.value:
            self.velocity = self.parent.parent.vslide.value
            self.temperature = (1/1000)*0.5*self.velocity**2
            for particle in self.particlesInBox:
                self.remove_widget(particle)
            self.particlesInBox = []
            for i in range(1000):
                particle = particleGen()
                particle.ParticlePosX = self.width * np.random.random()
                particle.ParticlePosY = self.height * np.random.random()
                particle.velocityX = self.velocity * random.choice([-1, 1]) * np.random.random()
                particle.velocityX = self.velocity * random.choice([-1, 1]) * np.random.random()
                particle.accelerationX = 1 ** random.choice([-1, 1]) * np.random.random()
                particle.accelerationY = 1 ** random.choice([-1, 1]) * np.random.random()
                self.particlesInBox.append(particle)
                self.add_widget(particle)
                self.pressure = 0
                self.avgPressure = 0


class glassWindow(RelativeLayout):
    pass


class Particles(App):
    def build(self):
        return glassWindow()


if __name__ == '__main__':
    Particles().run()