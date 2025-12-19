# Mac OS Wifi Scanner

There is no `iwlist` on Mac OS, that is why I've created my own script to get all SSID around me via cli ;)

## Prerequisites

Before running anything, check out the `requirements.txt` and make sure you have everything neccessary to run this script installed. To install all needed requirements:

```bash
# Create a Python virtualenv
python3 -m venv .venv

# Source the active script to use venv
source .venv/bin/activate

# Install module requirements
pip3 install -r requirements.txt
```

## Running the script

```bash

./wifi_scan.py

```

### Sample output

```python
{'SOME_WIFI': {'BSSID': '11:22:33:44:55:66',
               'Channel': '11(2GHz)',
               'Channel Width': '20MHz',
               'RSSI': -85,
               'Security': 'WPA2/WPA3 Personal'},
 'SOME_OTHER_WIFI': {'BSSID': '22:33:44:55:66:77',
                     'Channel': '11(2GHz)',
                     'Channel Width': '20MHz',
                     'RSSI': -82,
                     'Security': 'WPA2 Personal'},
 'SOME_OTHER_OTHER_WIFI': {'BSSID': '33:44:55:66:77:88',
                           'Channel': '40(5GHz)',
                           'Channel Width': '80MHz',
                           'RSSI': -56,
                           'Security': 'WPA2 Personal'}}
```

### Further usage info

`wifi_scan.py` supports a `--filter` (`-f`) argument, which can be used to find any particular SSID.

```bash
./wifi_scan.py -f SOME_WIFI_SSID
```

...which would result in similar output to the folowing:

``` python
{'SOME_WIFI': {'BSSID': '11:22:33:44:55:66',
               'Channel': '11(2GHz)',
               'Channel Width': '20MHz',
               'RSSI': -85,
               'Security': 'WPA2/WPA3 Personal'}}
```
