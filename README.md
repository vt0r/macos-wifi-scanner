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
{'SOME WIFI': {'BSSID': '11:11:11:11:11:11', 'RSSI': -45},
 'ANOTHER_WIFI': {'BSSID': '11:11:11:11:11:11', 'RSSI': -57}}
```

### Further usage info

`wifi_scan.py` supports a `--filter` (`-f`) argument, which can be used to find any particular SSID.

```bash
./wifi_scan.py -f SOME_WIFI_SSID
```

...which would result in similar output to the folowing:

``` python
{'SOME WIFI': {'BSSID': '11:11:11:11:11:11', 'RSSI': -45}
```
