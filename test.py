import pyuHoo

username = "xxxxxxxxxxx"
password = "xxxxxxxxxxx"

uHoo = pyuHoo.uHoo(username, password)

try:
    deviceList = uHoo.getDeviceList()
    print(deviceList)

    for device in deviceList:
        print(f"Latest data for device {device['serialNumber']}:")
        print(uHoo.getLatestData(device["serialNumber"]))
        print(f"Hourly data for device {device['serialNumber']}:")
        print(uHoo.getHourlyData(device["serialNumber"], "2019-03-20 18:00:00"))
        print(f"Daily data for device {device['serialNumber']}:")
        print(uHoo.getDailyData(device["serialNumber"], "2019-03-20 00:00:00"))

except pyuHoo.uHooException as e:
    print(e.message)
