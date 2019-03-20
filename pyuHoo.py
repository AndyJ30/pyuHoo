import requests
import json
from hashlib import sha256

class uHoo:
    """
    Wrapper class for uHoo Business EU API
    
    :param username: Your uHoo account email
    :param password: Your uHoo account password
    """

    apiBase = "https://api.uhooinc.eu/v1"

    def __init__(self, username, password):
        self.username = username
        self.password = self.hashPassword(password)

    @staticmethod
    def hashPassword(password):
        """
        Generate the hashed password required for authentication
        
        :param password: the plaintext password
        :returns: str hash
        """

        #Replace these with the actual salt values:
        salt1 = "0000000000000000000000000000000000000000000000000000000000000000" 
        salt2 = "xxxxxxxxxxx"
        
        _password = salt1 + password + salt2
        h = sha256()
        h.update(_password.encode("utf-8"))
        return h.hexdigest()
    
    def getDeviceList(self):
        """
        Get list of device names and serial numbers for your account.

        :returns: list of devices
        """
        path = "/getdevicelist"
        return self.uHooRequest(path)

    def getLatestData(self, serialNumber):
        """
        Get latest data for single uHoo
        
        :param serialNumber: the serial number of the uHoo from `getDeviceList()`
        :returns: dict
            Temperature (°C or °F)
            Relative Humidity (%)
            PM2.5 (ug/m^3)
            TVOC (ppb)
            CO2 (ppm)
            CO (ppm)
            Air Pressure (hPa)
            Ozone (ppb)
            NO2 (ppb)
            Timestamp (Unixtime in UTC)
            DateTime (YYYY-MM-DD HH:MM in 24-hour format)
        """

        path = "/getlatestdata"
        parameters = {"serialNumber" : serialNumber}
        return self.uHooRequest(path, parameters)

    def getHourlyData(self, serialNumber, prevDateTime):
        """
        Get hourly data for single uHoo 
        
        :param serialNumber: the serial number of the uHoo from `getDeviceList()`
        :param prevDateTime: the beginning of the hour to retrieve, in `YYYY-MM-DD HH:00:00` format
        :returns: list of up to 60 records in the same format as `getLatestData()`, one for each minute.
        """
        
        path = "/gethourlydata"
        parameters = {"serialNumber" : serialNumber, "prevDateTime" : prevDateTime}
        return self.uHooRequest(path, parameters)

    def getDailyData(self, serialNumber, prevDateTime):
        """
        Get daily data for single uHoo 
        
        :param serialNumber: the serial number of the uHoo from `getDeviceList()`
        :param prevDateTime: the beginning of the day to retrieve, in `YYYY-MM-DD 00:00:00` format
        :returns: list of up to 24 records in the same format as `getLatestData()`, one for each hour. Each record contains the average values for each hour.
        """
        
        path = "/getdailydata"
        parameters = {"serialNumber" : serialNumber, "prevDateTime" : prevDateTime}
        return self.uHooRequest(path, parameters)

    def uHooRequest(self, path, parameters = None):
        url = self.apiBase + path
        postData = {"username" : self.username, "password" : self.password}
        if parameters:
            postData.update(parameters)
        r = requests.post(url, postData)
        if r.status_code == 401:
            raise uHooException(r)

        return json.loads(r.text) if r.status_code == 200 else None

class uHooException(Exception):
    """
    Exception wrapper for uHoo API
        `status`: the status code returned
        `message`: the error message
    """
    def __init__(self, response): 
        response = json.loads(response.text)
        self.status = response["status"]
        self.message = response["message"]            

def uHooApi_Test():

    import getpass

    print("Enter your login details to test the api.")
    username = input("Username: ")
    password = getpass.getpass()

    print("Running uHoo API tests:")
    u = uHoo(username, password)
    
    try:
        deviceList = u.getDeviceList()
        print(deviceList)

        for device in deviceList:
            print(f"Latest data for device {device['deviceName']}:")
            print(u.getLatestData(device["serialNumber"]))
            print(f"Hourly data for device {device['deviceName']}:")
            print(u.getHourlyData(device["serialNumber"], "2019-03-20 18:00:00"))
            print(f"Daily data for device {device['deviceName']}:")
            print(u.getDailyData(device["serialNumber"], "2019-03-20 00:00:00"))
    except uHooException as e:
        print(e.message)
    
if __name__ == "__main__":
    uHooApi_Test()
