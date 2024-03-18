import psutil
import time
from plyer import notification

def check_battery():
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent
    return plugged, percent

def main():
    while True:
        plugged, percent = check_battery()

        if plugged and (percent == 20 or percent > 90):
            if percent == 20:
                message = "Nivel de batería al 20%!"
            else:
                message = "¡Batería al " + str(percent) + "%!"
            notification.notify(
                app_name="Battery Checker",
                title="Alerta de Batería",
                message=message,
                timeout=10
            )
        time.sleep(10)

if __name__ == "__main__":
    main()
