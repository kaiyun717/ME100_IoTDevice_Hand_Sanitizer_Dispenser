"""
╔====================================================╗
║ Pckt Refill (Pocket Refill)                        ║
║ Author: Kai Yun                                    ║
║                                                    ║
║ University of California, Berkeley                 ║
║ Mechanical Engineering 100 :: Internet of Things   ║
║ Spring 2021 Final Project                          ║
╚====================================================╝
(The project was done with Aaron Wagner.)
"""

import sys
import time

import network
from mqttclient import MQTTClient

from sensors.hcsr04 import HCSR04


class Connection:

    def __init__(self):
        # MQTT connection information
        self.adafruit_io_url = 'io.adafruit.com'
        self.adafruit_username = 'kaileo'
        self.adafruit_aio_key = 'aio_HMru72OEBBhl9RjkzrzwZT7nT8KI'

        # Adafruit feed
        self.feed_name = 'kaileo/feeds/pckt-refill'

        # WiFi connection information
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        self.ip = wlan.ifconfig()[0]

    def wifi_connection(self):
        """Make the WiFi connection."""
        if self.ip == '0.0.0.0':
            print("No WiFi connection. "
                  "\nPlease make sure connection is set correctly.")
            sys.exit()
        else:
            print("Connected to WiFi at IP", self.ip)

    def adafruit_connection(self):
        """Make the AdaFruit connection."""
        print("Connecting to Adafruit...")
        self.mqtt = MQTTClient(self.adafruit_io_url,
                               port='1883',
                               user=self.adafruit_username,
                               password=self.adafruit_aio_key)
        time.sleep(0.5)
        print("AdaFruit connection made at:", self.adafruit_username)

    def return_ip(self):
        return self.ip

    def return_mqtt(self):
        return self.mqtt


class Dispenser:

    def __init__(self, initial_amount=1000, refill_standard=10):
        """
        Keeps track of how much hand sanitizer is left and related calculations.
        :param initial_amount: initial amount of filled hand sanitizer. (milliliter)
        :param refill_standard: refill standard chosen by the user. (percentile)
        """

        self.initial_amount = initial_amount    # milliliter
        self.refill_standard_percentile = refill_standard   # percentile
        self.refill_standard = initial_amount * self.refill_standard_percentile / 100  # ounces
        self.amount_left = initial_amount        # milliliter
        self.initial_amount_not_set = True       # Checks whether initial_amount has been set by user.

        # Number of usages so far.
        self.number_used = 0        # count
        # Amount used per usage.
        self.per_usage = 2         # milliliter
        # Distance standard for counting a usage.
        self.usage_standard = 10     # cm

    def initial_amount_callback(self, topic, feed):
        """
        Sets initial amount for the dispenser from AdaFruit dashboard.
        :param topic: name of the topic
        :param feed: feed input from AdaFruit feed
        :return: N/A
        """
        feed_str = feed.decode()

        if feed_str.isdigit() and self.initial_amount_not_set:
            self.initial_amount = int(feed_str)
            self.amount_left = self.initial_amount
            self.refill_standard = self.initial_amount * self.refill_standard_percentile / 100
            self.initial_amount_not_set = False
            print("Initial Amount:", self.initial_amount, "milliliter.")

    def used(self):
        """
        Count a usage.
        """
        self.number_used += 1

    def return_amount_left(self):
        """
        Calculate how much sanitizer is left and return the value.
        :return: amount_left
        """
        self.amount_left = self.initial_amount - self.number_used * self.per_usage

        return self.amount_left

    def return_initial_amount(self):
        """
        Make a way for the use to check the initial amount and return the value.
        :return: initial_amount
        """
        return self.initial_amount

    def return_refill_standard(self):
        """
        Return the refill_standard.
        :return: refill_standard
        """
        return self.refill_standard

    def return_refill_standard_percentile(self):
        """
        Return the refill_standard_percentile.
        :return: refill_standard_percentile
        """
        return self.refill_standard_percentile

    def return_usage_standard(self):
        """
        Return the distance standard for counting the usage.
        :return: distance_usage
        """
        return self.usage_standard

    def return_initial_amount_not_set(self):
        """
        Return the boolean `initial_amount_not_set`.
        :return: initial_amount_not_set
        """
        return self.initial_amount_not_set


class SonarSensor:

    def __init__(self):
        """
        Initiate HCSR04 SonarSensor.
        """
        self.sensor = HCSR04(trigger_pin=22, echo_pin=23, echo_timeout_us=1000000)

    def measure_distance(self):
        """
        This returns True when the sensor senses a usage.
        :return: distance
        """
        return self.sensor.distance_cm()
