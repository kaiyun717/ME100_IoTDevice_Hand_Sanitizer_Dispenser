"""
Pckt Refill (Pocket Refill)
(ME 100 - Spring 2021 :: Final Project)
=====================================
All classes and functions related to the IoT add-on device for hand sanitizer dispenser.
 - Connection: Initialize connection with WiFi and MQTT.
 - Dispenser: Keeps track of the hand sanitizer left in the dispenser. Lights up the red
              LED when no more is left. Triggers an email notification, or maybe an app.
 - SonarSensor: Sensing the distance between the dispenser and the hand to count a usage.
 - LEDSignal: Lights up the red LED when dispenser needs a refill. Keeps the green LED on
              when it is not empty.
"""
from mqttclient import MQTTClient
import network
import sys
import time

from ina219 import INA219
from machine import Pin
from board import LED


class Connection:

    def __init__(self):
        # MQTT connection information
        self.adafruit_io_url = 'io.adafruit.com'
        self.adafruit_username = 'kaileo'                # Not determined yet
        self.adafruit_aio_key = '<TBD>'                  # Not determined yet

        # Adafruit feed
        self.feed_name = 'kaileo/feeds/Pckt-Refill'      # Not determined yet


        # WiFi connection information
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        self.ip = wlan.ifconfig()[0]

    def wifi_connection(self):
        """Make the WiFi connection."""
        if self.ip == '0.0.0.0':
            print("no wifi connection")
            sys.exit()
        else:
            print("Connected to WiFi at IP", self.ip)

    def adafruit_connection(self):
        """Make the AdaFruit connection."""
        print("Connecting to Adafruit")
        self.mqtt = MQTTClient(self.adafruit_io_url,
                               port='1883',
                               user=self.adafruit_username,
                               password=self.adafruit_aio_key)
        time.sleep(0.5)
        print("Connected!")

    def sub_callback(self, topic, msg):
        # Make the callback method for Adafruit
        pass

    def return_ip(self):
        return self.ip

    def return_mqtt(self):
        return self.mqtt


class Dispenser:

    def __init__(self, initial_amount=1000, refill_standard=10):
        """
        Keeps track of how much hand sanitizer is left and related calculations.
        :param initial_amount: initial amount of filled hand sanitizer. (ounces)
        :param refill_standard: refill standard chosen by the user. (ounces)
        """
        self.initial_amount = initial_amount
        self.total_left = initial_amount
        self.refill_standard = refill_standard

        # Number of usages so far.
        self.number_used = 0    # count
        # Amount used per usage.
        self.per_usage = 10     # ounces

    def used(self):
        self.number_used += 1

    def amount_left(self):
        self.total_left = self.initial_amount - self.number_used * self.per_usage

        return self.total_left

    def return_refill_standard(self):
        """
        Make a way for the user to set the refill_standard and return the value.
        :return:
        """
        return self.refill_standard


class SonarSensor:

    def __init__(self):
        """
        Figure out how to connect the sensor.
        """
        pass

    def sense_usage(self):
        """
        This returns True when the sensor senses a usage.
        :return:
        """
        pass


class LEDSignal:

    def __init__(self):
        # Automatically have the green light on.
        self.p14 = Pin(14, mode=Pin.OUT)
        pass

    def turn_red(self):
        """
        If there is no more left, turn the red LED on.
        :return:
        """
        pass


if __name__ == "__main__":

    # Connections made including WiFi and MQTT
    connection = Connection()
    connection.wifi_connection()
    connection.adafruit_connection()

    # Set up MQTT
    mqtt = connection.return_mqtt()
    mqtt.set_callback(connection.sub_callback)
    mqtt.publish(connection.feed_name, ...)     # Not determined yet

    # SonarSensor initialization.
    sensor = SonarSensor()

    # LED light initialization.
    led = LEDSignal

    # Dispenser related initialization.
    dispenser = Dispenser()
    refill_standard = dispenser.return_refill_standard()

    # Use a CALLBACK (Interrupt) instead of a while loop!!! Review Lab 6 Step 1 Code for reference!!!
    while True:

        if sensor.sense_usage():
            dispenser.used()

        amount_left = dispenser.amount_left()

        if amount_left < refill_standard:
            led.turn_red()

            # Send email to user.

        else:
            continue
