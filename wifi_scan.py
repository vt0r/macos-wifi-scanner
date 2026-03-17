#!/usr/bin/env python3
"""
wifi_scan.py - a script to dump the list of available SSIDs and basic info
"""
import argparse
import sys
import objc
import CoreLocation
from tabulate import tabulate

parse = argparse.ArgumentParser("Hello, I'm a Wi-Fi scanner for macOS\n\n" +
                                "Please accept the location access request for python if prompted.")
parse.add_argument("--filter", '-f', help="Single SSID to filter on", default=None)
parse.add_argument("--show-hidden", '-H', help="Include networks that are not broadcasting an SSID",
                   action="store_true", default=False)

args = parse.parse_args()
filter_ssid = args.filter
show_hidden = args.show_hidden

# Request location access, so that we can view the SSIDs and MACs
# pylint: disable-next=no-member
location_manager = CoreLocation.CLLocationManager.alloc().init()  # type: ignore
location_manager.startUpdatingLocation()


def scan(concrete_ssid=None, include_hidden=False):
    """
    Loads the CoreWLAN bundle, instantiates a WLAN interface(),
    dumps the list of available networks, including ones with hidden SSIDs,
    then prints the SSID, RSSI, BSSID for each result

    Optional arguments:
      concrete_ssid  - default: None  - the SSID of any one single network to filter on
      include_hidden - default: False - whether to include hidden networks (those not broadcasting an SSID)
    """
    bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
    objc.loadBundle('CoreWLAN', bundle_path=bundle_path, module_globals=globals())  # type: ignore

    # This is the part where we setup the wireless interface
    # pylint: disable-next=undefined-variable
    iface = CWInterface.interface()  # type: ignore # noqa: F821
    # Here, we scan for all networks filtered by the SSID provided by the user, if applicable
    # If no SSID was provided, we just show all networks within range of our adapter.
    networks = iface.scanForNetworksWithName_includeHidden_error_(concrete_ssid, True, None)

    # Here, we return a list of dicts (rows), one per nearby network, where each dict contains the SSID and
    # its associated parameters ('RSSI', 'BSSID', etc). Networks not broadcasting an SSID have an empty "SSID" value.
    rows = [
        {
            'SSID': i.ssid() if i.ssid() is not None else '',
            'RSSI': i.rssiValue(),
            'BSSID': i.bssid(),
            'Security': str(i.informationElementData).split('security=')[1].split(',')[0],
            'Chan.': str(i.wlanChannel()).split('channelNumber=')[1].split(',')[0].split('(')[0],
            'Freq.': str(i.wlanChannel()).split('channelNumber=')[1].split(',')[0].split('(')[1].split(')')[0],
            'Bandwidth': str(i.wlanChannel()).split('channelWidth=')[1].split('{')[1].split('}')[0].replace('(', '  (')
        }
        for i in networks[0].allObjects()
        if i.ssid() is not None or include_hidden
    ]
    # Sort by RSSI, showing the strongest signal first
    rows.sort(key=lambda r: r['RSSI'], reverse=True)

    return rows


# Try to get the list of results
try:
    result = scan(filter_ssid, show_hidden)

    # Nothing was returned. Was the SSID misspelled? Dump all available networks to help the user out...
    if filter_ssid is not None and (result == [] or result is None):
        raise ValueError('No matching SSID was found within range.')
    # Nothing was returned, even though the user did not provide a filter. Dump hidden networks to help the user out...
    elif filter_ssid is None and show_hidden is False and (result == [] or result is None):
        raise ValueError('No networks appear to be within range.')
    # Nothing was returned at all, even though the user did not provide a filter and is asking for hidden networks.
    # Are they in a desert or a faraday cage or something?
    elif filter_ssid is None and show_hidden is True and (result == [] or result is None):
        raise RuntimeError('No networks appear to be within range.')

# This might help the user better notice an obvious issue, so just print them all...
except ValueError as error:
    print(f"WARN: {repr(error)} Attempting to show full list of available networks instead...\n")
    # Show all available networks, including hidden ones
    result = scan(None, True)

# Nothing we can really do here, as there are no visible networks.
# Just go ahead and skip attempting to generate the table, then exit non-zero.
except RuntimeError as error:
    print(f"ERROR: {repr(error)} Please ensure your wireless adapter is enabled and working properly " +
          "and that you are within range of at least one wireless network.")
    sys.exit(1)

# This block will run whether or not we hit an exception above that should exit.
finally:
    # To be extra safe, don't bother generating the results output when there are no results.
    if (result != [] and result is not None):
        # Pretty print the results in a nicely formatted table, thanks to 'tabulate'
        # The column headers will be the keys from each row dict (SSID, RSSI, etc)
        # Each network and its properties will be printed to a row within the table.
        print(tabulate(result, headers="keys", tablefmt="rounded_outline"))
