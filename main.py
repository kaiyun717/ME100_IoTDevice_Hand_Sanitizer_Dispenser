import time

from machine import Pin

from pckt_refill import Connection, Dispenser, SonarSensor

if __name__ == "__main__":

    # Make the internet connections: WiFi, AdaFruit, MQTT, etc.
    connection = Connection()
    connection.wifi_connection()
    connection.adafruit_connection()

    # Initialize the Dispenser class.
    dispenser = Dispenser()

    mqtt = connection.return_mqtt()
    mqtt.set_callback(dispenser.initial_amount_callback)
    mqtt.publish(connection.feed_name, "Pckt Refill connection made!")
    print("Connection made with Pckt-Refill interface.\n")
    mqtt.subscribe(connection.feed_name)

    print("Waiting for the user to set initial amount...")
    while dispenser.return_initial_amount_not_set():
        mqtt.check_msg()
        time.sleep(2)
        continue

    initial_amount = dispenser.return_initial_amount()
    refill_standard_percentile = dispenser.return_refill_standard_percentile()
    usage_standard = dispenser.return_usage_standard()
    refill_standard = dispenser.return_refill_standard()

    # Print all the initial values for the Dispenser.
    print("Setting finished...")
    print("Initial Amount: ", initial_amount, "milliliter")
    print("Refill Standard: ", refill_standard_percentile, "%")
    print("Refill Standard: ", refill_standard, "milliliter")
    print("Usage Standard: ", usage_standard, "cm")

    # Initialize all the LED lights.
    led_yellow = Pin(4, mode=Pin.OUT)
    led_green = Pin(27, mode=Pin.OUT)
    led_red = Pin(21, mode=Pin.OUT)

    # Turn the green LED on to signal that the dispenser is full.
    led_green(1)

    time.sleep(5)

    # Initialize the SonarSenor.
    sonar_sensor = SonarSensor()

    while True:
        distance = sonar_sensor.measure_distance()

        print("Distance:", distance)

        if distance < usage_standard:
            led_green(0)
            led_yellow(1)
            time.sleep(1)
            led_yellow(0)
            led_green(1)

            dispenser.used()

        amount_left = dispenser.return_amount_left()

        if amount_left <= refill_standard:
            led_green(0)
            led_red(1)
            print("NEED REFILL!!!")
            time.sleep(10)

            # No need to turn it off in real usage.
            # Turn off when it's refilled.

            mqtt.publish(connection.feed_name, "Dispenser empty. Need REFILL!")
            break

        print("Amount Left:", amount_left, "milliliter")
        time.sleep(0.5)
