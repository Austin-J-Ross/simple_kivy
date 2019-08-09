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


from kivy.graphics import Line,Rectangle,Color
from kivy.uix.image import Image
from kivy.properties import StringProperty,NumericProperty,ListProperty
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
    particleBox:_particleBox
    ParticleBox:
        id:_particleBox
        size:self.size
        pos:self.pos
    Label:
        markup:True
        text:'[size=24px][color=#ff0000][b]'+str(root.particleBox.avgPressure)+'[/b][/color][/size]'
        pos:5,5


""")
import random    
import numpy as np

global pressure
pressure=0

class pressureReader(Label):
    pass

class particleGen(RelativeLayout):
    ParticlePosX=NumericProperty(0)
    ParticlePosY=NumericProperty(0)
    def __init__(self,  **kwargs):
        super(particleGen,self).__init__(**kwargs)
        self.ParticlePosX=50
        self.ParticlePosY=50
        self.velocityX=0
        self.velocityY=0
        self.accelerationX=1
        self.accelerationY=1
        self.mass=1
        self.schedule_events()
    def schedule_events(self):
        Clock.schedule_interval(self.moveParticle, 0.05)
        
    def moveParticle(self,dt):
        #first move particles
        self.ParticlePosX+=self.velocityX*dt+0.5*self.accelerationX*dt*dt
        self.ParticlePosY+=self.velocityY*dt+0.5*self.accelerationY*dt*dt
        #then check if particles have hit wall.
        #if they have then 
        if self.ParticlePosY > self.parent.height:
            self.parent.pressure+=self.mass*2*(abs(self.velocityY))/dt
            self.ParticlePosY = self.parent.height
            self.velocityY = -self.velocityY
        elif self.ParticlePosY < 0:
            self.parent.pressure+=self.mass*2*(abs(self.velocityY))/dt
            self.ParticlePosY = 0
            self.velocityY = -self.velocityY
        if self.ParticlePosX > self.parent.width:
            self.parent.pressure+=self.mass*2*(abs(self.velocityX))/dt
            self.ParticlePosX = self.parent.width
            self.velocityX = -self.velocityX
        elif self.ParticlePosX < 0:
            self.parent.pressure+=self.mass*2*(abs(self.velocityX))/dt
            self.ParticlePosX = 0
            self.velocityX = -self.velocityX            
    pass


    
class ParticleBox(RelativeLayout):
    pressure=NumericProperty(0)
    avgPressure=NumericProperty(0)
    def __init__(self,  **kwargs):
        super(ParticleBox, self).__init__(**kwargs)
        #ccreate list of widgets
        self.particlesInBox=[]
        self.size = (800, 600)
        for i in range(1000):
            particle=particleGen()
            particle.ParticlePosX=self.width*np.random.random()
            particle.ParticlePosY=self.height*np.random.random()
            particle.velocityX=200*random.choice([-1,1])*np.random.random()
            particle.velocityY=200*random.choice([-1,1])*np.random.random()
            particle.accelerationX=1**random.choice([-1,1])*np.random.random()
            particle.accelerationY=1**random.choice([-1,1])*np.random.random()
            self.particlesInBox.append(particle)
            self.add_widget(particle)
            self.pressure=0
            self.avgPressure=0

        self.schedule_events()        
    def schedule_events(self):
#        Clock.schedule_interval(lambda dt: self.checkPressure(), 2)
        Clock.schedule_interval(self.checkPressure, 2)

    def checkPressure(self,dt):
        oldPressure=self.pressure
        self.avgPressure=int(oldPressure/1000)
        print(oldPressure)
        self.pressure=0
        
class glassWindow(RelativeLayout):
    pass    
    
class Particles(App):
    def build(self):
        return glassWindow()

if __name__ == '__main__':
    Particles().run()