# Mac OS Wifi Scanner

macOS has no `iwlist`, so this script aims to fill that gap using macOS-native CoreWLAN and CoreLocation frameworks (PyObjC).

## Prerequisites

Install the required dependencies into a virtual environment:

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

``` txt
╭───────────────────────┬────────┬───────────────────┬─────────────────┬────────┬───────┬─────────────╮
│ SSID                  │   RSSI │ BSSID             │ Security        │ Chan.  │ Freq. │ Bandwidth   │
├───────────────────────┼────────┼───────────────────┼─────────────────┼────────┼───────┼─────────────┤
│ Some Other WiFi       │    -81 │ 22:33:44:55:66:77 │ WPA2 Personal   │ 11     │ 2GHz  │ 20MHz       │
│ Some Other Other WiFi │    -85 │ 33:44:55:66:77:88 │ WPA2 Personal   │ 1      │ 2GHz  │ 40MHz  (+1) │
│ Some WiFi             │    -90 │ 11:22:33:44:55:66 │ WPA2 Enterprise │ 157    │ 5GHz  │ 80MHz       │
╰───────────────────────┴────────┴───────────────────┴─────────────────┴────────┴───────┴─────────────╯
```

### Additional usage info

#### Filtering results by known SSID

`wifi_scan.py` supports a `--filter` (`-f`) argument, which can be used to limit results to any particular SSID.

```bash
./wifi_scan.py -f "Some WiFi"
```

Example output where only one matching network with that specific SSID is being broadcast:

``` txt
╭───────────┬────────┬───────────────────┬───────────────┬────────┬───────┬─────────────╮
│ SSID      │   RSSI │ BSSID             │ Security      │ Chan.  │ Freq. │ Bandwidth   │
├───────────┼────────┼───────────────────┼───────────────┼────────┼───────┼─────────────┤
│ Some WiFi │    -74 │ 11:22:33:44:55:66 │ WPA2 Personal │ 11     │ 2GHz  │ 20MHz       │
╰───────────┴────────┴───────────────────┴───────────────┴────────┴───────┴─────────────╯
```

#### Displaying Hidden SSID Networks

`wifi_scan.py` also supports a `--show-hidden` (`-H`) flag, which includes networks that are not broadcasting an SSID. Hidden networks have an empty "SSID" value.

```bash
./wifi_scan.py -H
```

Example output with one hidden network:

``` txt
╭───────────────────────┬────────┬───────────────────┬─────────────────┬────────┬───────┬─────────────╮
│ SSID                  │   RSSI │ BSSID             │ Security        │ Chan.  │ Freq. │ Bandwidth   │
├───────────────────────┼────────┼───────────────────┼─────────────────┼────────┼───────┼─────────────┤
│                       │    -71 │ 44:33:22:11:00:aa │ WPA2 Personal   │ 1      │ 2GHz  │ 40MHz  (+1) │
│ Some Other WiFi       │    -81 │ 22:33:44:55:66:77 │ WPA2 Personal   │ 11     │ 2GHz  │ 20MHz       │
│ Some Other Other WiFi │    -85 │ 33:44:55:66:77:88 │ WPA2 Personal   │ 1      │ 2GHz  │ 40MHz  (+1) │
│ Some WiFi             │    -90 │ 11:22:33:44:55:66 │ WPA2 Enterprise │ 157    │ 5GHz  │ 80MHz       │
╰───────────────────────┴────────┴───────────────────┴─────────────────┴────────┴───────┴─────────────╯
```
