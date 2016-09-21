from __future__ import print_function
import os
import numpy as np
import pandas as pd
import sys
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

mta_key = sys.argv[1]
buslineref = sys.argv[2]

def show_bus_locations(mta_key, buslineref):

    def get_jsonparsed_data(url):
        
        response = urllib.urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + mta_key + "&VehicleMonitoringDetailLevel=calls&LineRef=" + buslineref
    buses= get_jsonparsed_data(url)

    numbuses = len(buses['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])
    my_buses = buses['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

    print ("Bus Line: " + buslineref)
    print ("Number of Active Buses: " + str(numbuses))
    for x in range(numbuses):
            vehiclelocate = my_buses[x]['MonitoredVehicleJourney']['VehicleLocation']
            print ("Bus number %i is at %f latitude and %f longitude " % (x, vehiclelocate['Latitude'], vehiclelocate['Longitude']))

show_bus_locations(mta_key, buslineref)