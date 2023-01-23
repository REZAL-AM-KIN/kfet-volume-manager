from flask import current_app

from project import DEV


def setValue(slider):
    value = slider.value if slider.value <= slider.max else slider.max
    print("Change value:" +str(value))
    if not DEV:
        current_app.potentiometer.wiper = 127-value #172-value parce que 0 est la valeur max et 127 la valeur min sur l'amphi
    else:
        print("NO I2C, DEV MODE IS ACTIVE")
