from flask import current_app


def setValue(slider):
    value = slider.value if slider.value <= slider.max else slider.max
    print(value)
    current_app.potentiometer.wiper = value
