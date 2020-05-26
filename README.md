# pyuHoo
Wrapper for [uHoo](https://www.uhooair.co.uk/) Business EU API

# Usage
To use the pyuHoo library:

1. Include `pyuHoo.py` in your module/project path
2. Import pyuHoo
3. Create a new `uHoo` instance using your account username and password:
```python
  import pyuHoo
  
  username = "xxxxxxxxxxx"
  password = "xxxxxxxxxxx"

  uHoo = pyuHoo.uHoo(username, password)
```

# Functions

## getDeviceList()
Gets the list of devices for your account.

Returns a `list` containing the MAC address, Serial Number and Name of each device:
```python
>>> uHoo.getDeviceList()
[
  {'macAddress': '000000000000', 'serialNumber': '000000000000000000000000', 'deviceName': 'My Device 1'},
  {'macAddress': '000000000001', 'serialNumber': '000000000000000000000001', 'deviceName': 'My Device 2'}
]
```

## getLatestData( serialNumber )
Gets the latest set of readings for the given serialNumber.

Returns a `dict` containing the recorded parameters:

```python
>>> uHoo.getLatestData('000000000000')
{
  'Temperature': '20.0',          #(°C or °F)
  'Relative Humidity': '46.4',    #(%)
  'PM2.5': '48.4',                #(ug/m^3)
  'TVOC': '66.0',                 #(ppb)
  'CO2': '1631.0',                #(ppm)
  'CO': '0.0',                    #(ppm)
  'Air Pressure': '1024.8',       #(hPa)
  'Ozone': '6.1',                 #(ppb)
  'NO2': '18.3',                  #(ppb)
  'Timestamp': 1553117957,        #(UTC Unix timestamp)
  'DateTime': '2019-03-20 21:39'  #(YYYY-MM-DD HH:MM 24-hour)
}
```

## getHourlyData( serialNumber, prevDateTime )
Gets the hourly data for the given serialNumber in the given hour.

Returns a `list` of `dict`s containing the recorded parameters:

```python
>>> uHoo.getHourlyData('000000000000', '2019-03-20 18:00:00')
[
  {'Temperature': '21.4', 'Relative Humidity': '44.9', ..., 'DateTime': '2019-03-20 18:00'}, 
  {'Temperature': '21.5', 'Relative Humidity': '44.7', ..., 'DateTime': '2019-03-20 18:01'}, 
  {'Temperature': '21.6', 'Relative Humidity': '44.2', ..., 'DateTime': '2019-03-20 18:02'},
  {...}
]
```

## getDailyData( serialNumber, prevDateTime )
Gets the daily data for the given serialNumber in the given day. Values are the average for each hour.

Returns a `list` of `dict`s containing the recorded parameters:

```python
>>> uHoo.getDailyData('000000000000', '2019-03-19 00:00:00')
[
  {'Temperature': '21.4', 'Relative Humidity': '44.9', ..., 'DateTime': '2019-03-20 00:00'}, 
  {'Temperature': '21.5', 'Relative Humidity': '44.7', ..., 'DateTime': '2019-03-20 01:00'}, 
  {'Temperature': '21.6', 'Relative Humidity': '44.2', ..., 'DateTime': '2019-03-20 02:00'},
  {...}
]
```

