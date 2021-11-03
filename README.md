# Pckt Refill
(Pocket Refill)
**IoT Device :: Hand Sanitizer Dispenser**
_UC Berkeley Spring 2021 MEC ENG 100 (Internet of Things) Final Project_

- Project Members: Kai Yun, Aaron Wagner
- Project Objective: This is the code for an add-on IoT Device that measures the amount of hand sanitizer left in a dispenser. The device communicates with users to alert when it needs to be refilled. The user can also set the standard of when to have the device send an alert.

## Concept
<img src="https://user-images.githubusercontent.com/70457814/112840763-b04c6900-90da-11eb-9ea5-3ade7bda4b37.png" width=800x>

With the understanding of the demand that hand-sanitizer has and will have in the years to come following Covid, we are able to recognize the issue that needed to be addressed. With automatic hand-sanitizer dispensers facing unprecedented usage, it was common, especially within UC Berkeley, to approach, and receive nothing from a dispenser, that would often go unfilled for days at a time.

Consequently, our solution is to create a device that measures the usage of each individual hand-sanitizer dispenser and returns an email notification to the janitorial staff when any dispenser needs to be refilled. In detail, we wanted a device that would measure each usage by a count system that would identify when a hand is placed under the dispenser nozzle. Following this, the count respectively subtracts one usage amount of hand-sanitizer fluid from the actual capacity of fluid that is set by the janitorial staff. For example, the janitorial staff may refill a dispenser, and in using an app, they set the fluid amount of the dispenser to 64 ounces. The aforementioned count would subtract one usage amount of fluid, let us say 1 ounce, from the manually set total of 64 and will store this value and title it as the ‘amount left’ until the next usage and so forth. When the amount left reaches a specified value, a notification will be sent to staff alerting them that this specific hand sanitizer, let us call it Etcheverry Hall #1, needs to be refilled. The notification will be sent at an optimal time that allows the janitorial staff to view, prepare, and then refill the dispenser which minimizes the amount of time when the dispenser is empty. When refilled, the staff would set the fluid capacity value again, and the process would be repeated.

## Circuit Design and Components
<img src="https://user-images.githubusercontent.com/70457814/140209928-113f08f0-2944-4458-b916-c5eb55f9f6b4.png" width=600px>
<img src="https://user-images.githubusercontent.com/70457814/140209958-8b8bb0f5-bdb9-4024-a5c4-9f22d979e8e6.png" width=300px>

- Adafruit HUZZAH32 – ESP32 Feather Board
- LEDs (red, green, yellow)
- HC-SR04 Ultrasonic Sonar Distance Sensor
- 6V Battery

## Software: Computation and Connection
- Communication Protocal: Message Queuing Telemetry Transport (MQTT)
- Cloud Provider: Adafruit IO MQTT Broker
- IFTTT Applet

## Test Result
- Device Demonstration:
https://drive.google.com/file/d/15Vhqhs-s5xEQFrBj75mmauE7lBEffv5K/view?usp=sharing

- Email notification
<img src="https://user-images.githubusercontent.com/70457814/140216300-e1781437-d7f1-4873-823d-b863dbaf143a.png" width=500px>

## Discussion
This device is simply a proof-of-concept project. By further developing an app for the device, this project may have real potential. **The sensor device itself can be simply attached to already-exisitng hand sanitizer dispensers; the potential business model comes from the service it provides via monthly subscriptions, etc.** 
