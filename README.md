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
╭───────────────────────┬────────┬───────────────────┬─────────────────┬─────────────────┬─────────────╮
│                       │   RSSI │ BSSID             │ Security        │ Chan. (Freq.)   │ Bandwidth   │
├───────────────────────┼────────┼───────────────────┼─────────────────┼─────────────────┼─────────────┤
│ Some WiFi             │    -90 │ 11:22:33:44:55:66 │ WPA2 Enterprise │ 157(5GHz)       │ 80MHz       │
│ Some Other WiFi       │    -81 │ 22:33:44:55:66:77 │ WPA2 Personal   │ 11(2GHz)        │ 20MHz       │
│ Some Other Other WiFi │    -85 │ 33:44:55:66:77:88 │ WPA2 Personal   │ 1(2GHz)         │ 40MHz(+1)   │
╰───────────────────────┴────────┴───────────────────┴─────────────────┴─────────────────┴─────────────╯
```

### Further usage info

`wifi_scan.py` supports a `--filter` (`-f`) argument, which can be used to find any particular SSID.

```bash
./wifi_scan.py -f "Some WiFi"
```

...which would result in similar output to the folowing:

``` python
╭───────────┬────────┬───────────────────┬───────────────┬─────────────────┬─────────────╮
│           │   RSSI │ BSSID             │ Security      │ Chan. (Freq.)   │ Bandwidth   │
├───────────┼────────┼───────────────────┼───────────────┼─────────────────┼─────────────┤
│ Some WiFi │    -74 │ 11:22:33:44:55:66 │ WPA2 Personal │ 11(2GHz)        │ 20MHz       │
╰───────────┴────────┴───────────────────┴───────────────┴─────────────────┴─────────────╯
```
