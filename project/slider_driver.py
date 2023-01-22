from flask import app


def setValue(slider):
    value = slider.value if slider.value <= slider.max else slider.max
    print(value)
    app.potentiometer.wiper = value
