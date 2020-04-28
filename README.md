# Sat-Tracker

Python based satellite tracker.


# Installation

```

apt-get install python3-geopy python3-pyorbital
python3 -m pip install playsound

```

# Example

```
(tracker-prod) sat-tracker>python tracker.py -h
usage: tracker.py [-h] [-lat LATITUDE] [-lon LONGITUDE] [-alt ALTITUDE]
                  [-weather] [-afsk] [-bpsk] [-fm] [-custom CUSTOM]
                  [-custom-tle CUSTOM_TLE] [-elevation ELEVATION] [-network]
                  [-host TCP_HOST] [-port TCP_PORT] [-com SERIAL_PORT]
                  [-min MINMOUNT] [-s]

optional arguments:
  -h                    Print this help message then exit.
  -lat LATITUDE         Ground Station Latitude.
  -lon LONGITUDE        Ground Station Longitude.
  -alt ALTITUDE         Ground Station Altitude.
  -weather              Weather Satalites: METEOR-M 2, NOAA 19, NOAA 18, NOAA
                        15.
  -afsk                 AFSK Packet: PCSAT (NO-44), ISS (ZARYA).
  -bpsk                 BPSK: JY1SAT (JO-97), FUNCUBE-1 (AO-73), NAYIF-1
                        (EO-88).
  -fm                   FM Voice: RADFXSAT (FOX-1B), FOX-1CLIFF (AO-95),
                        FOX-1D (AO-92), SAUDISAT 1C (SO-50).
  -custom CUSTOM        Custom Satelite To Track
  -custom-tle CUSTOM_TLE
                        Custom TLE File For Offline Tracking
  -elevation ELEVATION  Minimum Satalite Elevation For Prediction.
  -network              Enable TCP Network Stream Sat Name, Latitude,
                        Longitude and Altitude over TCP Network.
  -host TCP_HOST        TCP Network Host IP Address.
  -port TCP_PORT        TCP Network Port.
  -com SERIAL_PORT      Mount Serial Port.
  -min MINMOUNT         Minimum Mount Elevation Prior To Movement.
  -s                    Silent Mode (Disable AOS Alert Sounds).

Examples: tracker.py -weather

(tracker-prod) sat-tracker>
```


# Satellites Currently Supported.

Weather:

* METEOR-M 2
* NOAA 19
* NOAA 18
* NOAA 15


FM:

* RADFXSAT (FOX-1B)
* FOX-1CLIFF (AO-95)
* FOX-1D (AO-92)
* SAUDISAT 1C (SO-50)

AFSK:

* PCSAT (NO-44)
* ISS (ZARYA)

BPSK:

* JY1SAT (JO-97)
* FUNCUBE-1 (AO-73)
* NAYIF-1 (EO-88).

CUSTOM:

* Custom satellite name will allow tracking if found in the [NORAD](https://www.celestrak.com/NORAD/elements/) lists.


* Custom TLE (Two Line Element) will allows a conjunction of custom satellite name and file supplied.

# Com Port

The RS232 serial com port currently will only interface with Celetron telescope mounts. 


