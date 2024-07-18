import json
import sys
import requests
import time
import schedule
import email
import smtplib

def job():

    #API key removed for security
    cisco_meraki_api_Key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    #Organization ID removed for security
    organizationId = 'XXXXXX'
    #Create base URL for API calls for networks
    baseUrl = 'https://api.meraki.com/api/v1/'
    network_api_url = "organizations/{}/networks".format(organizationId)

    #Necessary headers for requests to be allowed
    headers = {
        'X-Cisco-Meraki-API-Key': cisco_meraki_api_Key,
        'Authorization': 'Bearer 75dd5334bef4d2bc96f26138c163c0a3fa0b5ca6',
        'Content-Type': 'application/json'
        }

    #Make request to GET networks, print result code
    get_networks = requests.get(baseUrl+network_api_url,headers=headers)
    print(get_networks)

    #Parse returned data as JSON
    networks = get_networks.json()

    #Prepare file for writing
    f = open('network_results.txt', "w+")
    f.close()

    #Leave this block for future test calls so as not to disrupt other sites.
    #TEST NETWORK ID: 
    #test_request = requests.get(baseUrl+"networks//clients",headers=headers)
    #print(test_request)
    #devices = test_request.json()
    #for device in devices:
    #    serial = device['recentDeviceSerial']
    #    reboot_request = requests.post(baseUrl+"/networks//devices/{}/reboot".format(serial),headers=headers)
    #    print(reboot_request)

    #Loop across every network and attempt to reboot all devices on the network, saving results to file.
    for net in networks:
        try:
            net_id = net['id']
            name = net['name']
            print("Making API Call")
            reboot_api_call = requests.get(baseUrl+"/networks/{}/devices".format(net_id),headers=headers)
            print(reboot_api_call)
            devices = reboot_api_call.json()
            for device in devices:
                serial = device['serial']
                if name == "Mayor Office" or name == "Spare MX67W 1":
                    print("Rebooting {} at {}".format(serial,name))
                    reboot_request = requests.post(baseUrl+"/networks/{}/devices/{}/reboot".format(net_id,serial),headers=headers)
                else:
                    print("Skipped")
                time.sleep(10)
        except:
            print("Error rebooting {}".format(name))
            continue

    #Close file, re-open for reading
    f.close()
    return

schedule.every().day.at("04:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
