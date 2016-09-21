

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
bus_line = sys.argv[2]
output_file = sys.argv[3]

def get_bus_info(mta_key, bus_line, output_file):
    
    def get_jsonparsed_data(url):
        
        response = urllib.urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)
    

    url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + mta_key + "&VehicleMonitoringDetailLevel=calls&LineRef=" + bus_line
    buses= get_jsonparsed_data(url)
    
    my_buses = buses['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    numbuses = len(buses['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])
    
    
    lat=[]
    for i in range(numbuses):
        lat.append(my_buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude'])
        
    
    lon=[]
    for i in range(numbuses):
        lon.append(my_buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude'])
        
      
    stop_point_name=[]
    for i in range(numbuses):
        stop_point = my_buses[i]["MonitoredVehicleJourney"]["MonitoredCall"]['StopPointName']
        if not stop_point == "":
            stop_point_name.append(stop_point)
        else:
            stop_point_name.append("N/A")
        
    presentable_distance=[]
    for i in range(numbuses):
        presentable = my_buses[i]["MonitoredVehicleJourney"]["MonitoredCall"]['Extensions']['Distances']['PresentableDistance']
        if not presentable == "":
            presentable_distance.append(presentable)
        else:
            presentable_distance.append("N/A")
        
    show_bus_info=pd.DataFrame({'Latitude': lat, 'Longitude': lon, 'Stop Name': stop_point_name, 'Stop Status': presentable_distance})
    
    show_bus_info.to_csv(output_file)


get_bus_info(mta_key, bus_line, output_file)
