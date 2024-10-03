import time
import psutil
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

try:
    client = OpenRGBClient()
except Exception as e:
    print(f"Ошибка при создании клиента OpenRGB: {e}")
    exit(1)

print("Доступные методы и атрибуты клиента OpenRGB:", dir(client))


def get_cpu_temperature():
    sensors = psutil.sensors_temperatures()
    if 'coretemp' in sensors:
        temps = sensors['coretemp']
        return temps[0].current
    return None

while True:
    try:
        try:
            temperature = get_cpu_temperature()
        except Exception as e:
            print(f"Ошибка при получении температуры процессора: {e}")
            continue

        if temperature is None:
            print("Не удалось получить температуру процессора.")
            continue

        print(f"Скрипт запущен. Температура процессора: {temperature}°C")

        if temperature < 40:
            color = [0, 0, 255]
        elif 40 <= temperature < 50:
            color = [255, 255, 0]
        else:
            color = [255, 0, 0]

        try:
            devices = client.devices
        except Exception as e:
            print(f"Ошибка при получении устройств: {e}")
            continue

        if devices is None or len(devices) == 0:
            print("Устройства не найдены.")
            continue

        for device in devices:
            try:
                device_name = device.name
            except Exception as e:
                print(f"Ошибка при получении имени устройства: {e}")
                continue

            print(f"Обнаружено устройство: {device_name}")

            print("Атрибуты устройства:", dir(device))

            try:
                leds = device.leds
            except Exception as e:
                print(f"Ошибка при получении светодиодов устройства {device_name}: {e}")
                continue

            if leds is None or len(leds) == 0:
                print(f"Устройство {device_name} не содержит светодиодов.")
                continue

            num_leds = len(leds)
            print(f"Количество светодиодов: {num_leds}")

            try:
                print(f"Установка цвета {color} на устройство {device_name}")
                device.clear()

                colors_to_set = [RGBColor(color[0], color[1], color[2])] * num_leds

                device.set_colors(colors_to_set)
                print("Цвет установлен успешно!")
            except Exception as e:
                print(f"Ошибка при установке цвета на устройстве {device_name}: {e}")

        try:
            time.sleep(10)
        except Exception as e:
            print(f"Ошибка при вызове time.sleep(): {e}")
            break

    except Exception as e:
        print(f"Ошибка: {e}")
        break