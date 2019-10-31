# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 18:17:48 2019

@author: Austin
"""
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix import widget
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
from kivy.uix.widget import Widget

Builder.load_string("""
<Particle@RelativeLayout>:                    
    canvas:
        Color:
            rgba:1,1,1,1
        Ellipse:
            size:5,5
            pos:root.x_pos,root.y_pos



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
                text:'[size=24px][color=#ffffff][b]Temperature:[/b][/color][/size]'
                size_hint_y:None
                height:20
            RelativeLayout:
                size:self.size
                pos:self.pos
            Slider:
                id: _vslide
                value: 200
                range: (100,1000)
                step: 10
            Label:
                markup:True
                text:'[size=24px][color=#ffffff][b]'+str(int(root.particle_box.temperature))+'[/b][/color][/size]'      
        ParticleBox:
            id:_particleBox
            size:self.size
            pos:self.pos

""")
import random
import numpy as np

global pressure
pressure = 0


def create_first_grid(box):
    app: App = App.get_running_app()
    app.point_dict = {}
    app.box_height = box.height
    app.box_width = box.width
    print(box.width, box.height)
    for i in range(int(800)+1):
        for j in range(int(800)+1):
            app.point_dict[(i, j)] = []
    print(app.point_dict.keys())
    pass



def create_grid(box):
    app: App = App.get_running_app()
    app.point_dict = {}
    app.box_height = box.height
    app.box_width = box.width
    print(box.width, box.height)
    for i in range(int(box.height)+1):
        for j in range(int(box.height)+1):
            app.point_dict[(i, j)] = []
    print(app.point_dict.keys())
    pass


def remove_from_grid(wid: Widget):
    app = App.get_running_app()
    if wid in app.point_dict[wid.coordinate]:
        app.point_dict[wid.coordinate].remove(wid)
    pass


def place_in_grid(wid: Widget):
    app = App.get_running_app()
    if wid not in app.point_dict[wid.coordinate]:
        app.point_dict[wid.coordinate].append(wid)
    pass


class Particle(RelativeLayout):
    x_pos = NumericProperty(0)
    y_pos = NumericProperty(0)
    velocity = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Particle, self).__init__(**kwargs)
        self.x_pos = 50
        self.y_pos = 50
        self.velocity = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.mass = 1
        self.time_added = time.time()
        self.schedule_events()

    @property
    def coordinate(self):
        widx = self.x_pos
        widy = self.y_pos
        x = int(widx/5)
        y = int(widy/5)
        return (x, y)

    def schedule_events(self):
        Clock.schedule_interval(self.move, 0.05)
        Clock.schedule_interval(self.collide, 0.05)

    def collide(self, dt):
        app = App.get_running_app()
        if self.coordinate[0] > 0 and self.coordinate[1] > 0:
            if len(app.point_dict[self.coordinate]) > 1:
                print("collide!")
                for wid in app.point_dict[self.coordinate]:
                    if wid != self:
                        vel_x = wid.velocity_x
                        vel_y = wid.velocity_y
                        if vel_y > vel_x:
                            mod = (-1, 1)
                        else:
                            mod = (1, -1)

                        wid.velocity_x, wid.velocity_y = mod[0]*self.velocity_x, mod[1]*self.velocity_y
                        self.velocity_x, self.velocity_y = mod[0]*vel_x, mod[1]*vel_y
                        break

    def move(self, dt):
        # first move particles
        remove_from_grid(self)
        self.x_pos += self.velocity_x * dt + 0.5 * self.accelerationX * dt * dt
        self.y_pos += self.velocity_y * dt + 0.5 * self.accelerationY * dt * dt
        # then check if particles have hit wall.
        # if they have then
        if self.parent:
            if self.y_pos > self.parent.height:
                self.parent.pressure += self.mass * 2 * (abs(self.velocity_y)) / dt
                self.y_pos = self.parent.height
                self.velocity_y = -self.velocity_y
            elif self.y_pos < 0:
                self.parent.pressure += self.mass * 2 * (abs(self.velocity_y)) / dt
                self.y_pos = 0
                self.velocity_y = -self.velocity_y
            if self.x_pos > self.parent.width:
                self.parent.pressure += self.mass * 2 * (abs(self.velocity_x)) / dt
                self.x_pos = self.parent.width
                self.velocity_x = -self.velocity_x
            elif self.x_pos < 0:
                self.parent.pressure += self.mass * 2 * (abs(self.velocity_x)) / dt
                self.x_pos = 0
                self.velocity_x = -self.velocity_x
            place_in_grid(self)
        else:
            Clock.unschedule(self.move)

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
        create_first_grid(self)
        print(self.width, self.height)
        self.particles_in_box = {}
        self.size = (800, 600)
        self.velocity = 200
        self.temperature = (1/1000)*0.5*self.velocity**2
        self.number_particles = 100
        self.last_height = self.height
        self.last_width = self.width
        for i in range(self.number_particles):
            particle = Particle()
            particle.x_pos = self.width * np.random.random()
            particle.y_pos = self.height * np.random.random()
            particle.velocity_x = self.velocity * random.choice([-1, 1]) * np.random.random()
            particle.velocity_y = self.velocity * random.choice([-1, 1]) * np.random.random()
            particle.accelerationX = 1 ** random.choice([-1, 1]) * np.random.random()
            particle.accelerationY = 1 ** random.choice([-1, 1]) * np.random.random()
            self.particles_in_box[i] = particle
            self.add_widget(self.particles_in_box[i])
            self.pressure = 0
            self.avgPressure = 0

        self.schedule_events()


    def schedule_events(self):
        #        Clock.schedule_interval(lambda dt: self.checkPressure(), 2)
        Clock.schedule_interval(self.check_pressure, 2)
        Clock.schedule_interval(self.check_velocity, 0.5)
        Clock.schedule_interval(self.check_number, 0.5)
        # Clock.schedule_interval(self.check_window, 20)

    def check_pressure(self, dt):
        oldPressure = self.pressure
        self.avgPressure = int(oldPressure / 1000)
        self.pressure = 0

    def check_number(self, dt):
        oldPressure = self.pressure
        self.avgPressure = int(oldPressure / 1000)
        self.pressure = 0

    def check_velocity(self, dt):
        if self.velocity != self.parent.parent.vslide.value:
            self.velocity = self.parent.parent.vslide.value
            self.temperature = (1/1000)*0.5*self.velocity**2
            for i, particle in enumerate(self.particles_in_box.keys()):
                self.remove_widget(self.particles_in_box[i])
            self.particles_in_box = {}
            for i in range(self.number_particles):
                particle = Particle()
                particle.x_pos = self.width * np.random.random()
                particle.y_pos = self.height * np.random.random()
                particle.velocity_x = self.velocity * random.choice([-1, 1]) * np.random.random()
                particle.velocity_y = self.velocity * random.choice([-1, 1]) * np.random.random()
                particle.accelerationX = 1 ** random.choice([-1, 1]) * np.random.random()
                particle.accelerationY = 1 ** random.choice([-1, 1]) * np.random.random()
                self.particles_in_box[i] = particle
                self.add_widget(self.particles_in_box[i])

    def check_window(self, dt):
        if self.last_height != self.height or self.last_width != self.width:
            print(self.width, self.height)
            create_grid(self)
            self.last_height = self.height
            self.last_width = self.width
            print("resized!")
        pass


class glassWindow(RelativeLayout):
    pass


class Particles(App):
    def build(self):
        return glassWindow()


if __name__ == '__main__':
    Particles().run()