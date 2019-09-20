#!/usr/bin/env python
import time

__author__ = 'Jacob Walker'

import requests
import turtle
import Tkinter

api_url = "http://api.open-notify.org"


def get_people_in_space():
    """Returns a list of astronauts from the api."""
    req = requests.get(api_url + '/astros.json')
    j = req.json()
    return j['people']


def print_people_in_space(people):
    """Format and print a list of given astronauts"""
    list_format = '\n'.join(['{}:   {}'.format(x['craft'], x['name']) for x in people])
    print('There are currently {} in space:\nCraft | Name\n{}'.format(len(people), list_format))


def get_iss_current_position():
    """Return the current location of the ISS from the api"""
    req = requests.get(api_url + '/iss-now.json')
    j = req.json()
    return {'timestamp': j['timestamp'], 'position': j['iss_position']}


def get_next_pass(lat, lon):
    payload = {'lat': lat, 'lon': lon, 'n': 1}
    req = requests.get(api_url + '/iss-pass.json', payload)
    j = req.json()
    return j['response'][0]['risetime']


def draw_map(current_position, next_passover):
    """Finally draw up the gui for us"""
    background = './map.gif'
    satellite = './iss.gif'
    indy_cords = (86.1581, 39.7684)
    screen = turtle.Screen()
    screen.bgpic(background)
    screen.addshape(satellite)
    screen.setup(720, 360)
    screen.setworldcoordinates(180, -90, -180, 90)

    iss = turtle.Turtle()
    iss.pencolor("blue")
    iss.penup()
    iss.setpos(indy_cords)
    iss.pendown()
    iss.shape(satellite)
    iss.goto(float(current_position["longitude"]), float(current_position["latitude"]))

    indy = turtle.Turtle()
    indy.hideturtle()
    indy.penup()
    indy.pencolor('yellow')
    indy.setpos(indy_cords)
    indy.dot()
    indy.write("Next Passover: {}".format(time.ctime(next_passover)))
    screen.exitonclick()


def main():
    people = get_people_in_space()
    print_people_in_space(people)
    current_location = get_iss_current_position()
    next_pass = get_next_pass(39.7684, 86.1581)
    draw_map(current_location["position"], next_pass)


if __name__ == '__main__':
    main()
