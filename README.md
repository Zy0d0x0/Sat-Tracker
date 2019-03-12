# Sat-Tracker

Python based satelite tracker.


# Installation

```

pip install -e requirements.txt

```


# Satelites Currently Supported.

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

* Custom satelite name will allow tracking if found in the Norad list supplied online.

* Custom TLE (Two Line Element) will allows a conjunction of custom satelite name and file supplied.

# Com Port

The RS232 serial com port currently will only interface with Celetron telescope mounts. 


# Current Known Bugs Todo.

* Ensure Celestron Next Remote does not go below 0 degree's as there is no need for this. This will also prevent the antenna crashing into the mount.

* Add auto update if time has gone over 24 hour running period.

* Add custom list of sats to track.

