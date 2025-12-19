#!/usr/bin/env python3
"""
wifi_scan.py - a script to dump the list of available SSIDs and basic info
"""
import argparse
import objc
import CoreLocation
from tabulate import tabulate

parse = argparse.ArgumentParser("Hello, I'm a Wi-Fi scanner for macOS\n\n" +
                                "Please allow the location request for python if prompted.")
parse.add_argument("--filter", '-f', help="Single SSID to filter on", default=None)

args = parse.parse_args()
filter_ssid = args.filter

# Request location access, so that we can view the SSIDs
# pylint: disable-next=no-member
location_manager = CoreLocation.CLLocationManager.alloc().init()
location_manager.startUpdatingLocation()


def scan(concrete_ssid=None):
    """
    Loads the CoreWLAN bundle, instantiates an interface(),
    dumps the list of available networks, including ones with hidden SSIDs,
    then prints the SSID, RSSI, BSSID for each result

    Optional argument:
      concrete_ssid - the SSID of one single network to filter on
    """
    bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
    objc.loadBundle('CoreWLAN',
                    bundle_path=bundle_path,
                    module_globals=globals())

    # pylint: disable-next=undefined-variable
    iface = CWInterface.interface()  # type: ignore # noqa: F821
    networks = iface.scanForNetworksWithName_includeHidden_error_(concrete_ssid, True, None)
    return {
        i.ssid(): {
            'RSSI': i.rssiValue(),
            'BSSID': i.bssid(),
            'Security': str(i.informationElementData).split('security=')[1].split(',')[0],
            'Chan. (Freq.)': str(i.wlanChannel()).split('channelNumber=')[1].split(',')[0],
            'Bandwidth': str(i.wlanChannel()).split('channelWidth=')[1].split('{')[1].split('}')[0]
        }
        for i in networks[0].allObjects() if i.ssid() is not None
    }


result = scan(filter_ssid)

if result is None:
    print("Sorry, couldn't find that SSID")

print(tabulate(result.values(), headers="keys", tablefmt="rounded_outline", showindex=result.keys()))
