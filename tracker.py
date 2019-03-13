#! /usr/bin/env python3

from libs import satTracker
import argparse


#
# Show Menu
#

parser = argparse.ArgumentParser(
   add_help=False,
   formatter_class=argparse.RawDescriptionHelpFormatter, # This will fix description and epilog format
   epilog="Examples: %(prog)s -weather")

# Adds arguments to help menu
parser.add_argument("-h", action="help",  help="Print this help message then exit.")

# Groundstation Location Information
parser.add_argument("-lat", dest="latitude", default=51.4844, help="Ground Station Latitude.")
parser.add_argument("-lon", dest="longitude", default=0.1302, help="Ground Station Longitude.")
parser.add_argument("-alt", dest="altitude", help="Ground Station Altitude.")

# Sats To Track
parser.add_argument("-weather", action="store_true", help="Weather Satalites: METEOR-M 2, NOAA 19, NOAA 18, NOAA 15.") ## Required argument
parser.add_argument("-afsk", action="store_true", help="AFSK Packet: PCSAT (NO-44), ISS (ZARYA).")
parser.add_argument("-bpsk", action="store_true", help="BPSK: JY1SAT (JO-97), FUNCUBE-1 (AO-73), NAYIF-1 (EO-88).")
parser.add_argument("-fm", action="store_true", help="FM Voice: RADFXSAT (FOX-1B), FOX-1CLIFF (AO-95), FOX-1D (AO-92), SAUDISAT 1C (SO-50).")

# Custom Satelite
parser.add_argument("-custom", dest="custom", help="Custom Satelite To Track")

# Define A custom List Of TLE's, This Can Also Be Used With Custom Name For Tracking Sats That Are Not Avalible
# Via The Online Method That Defaults With pyorbital 
parser.add_argument("-custom-tle", dest="custom_tle", help="Custom TLE File For Offline Tracking")

# Sets the default elevation for the satelite prediction
parser.add_argument("-elevation", dest="elevation", default=15, help="Minimum Satalite Elevation For Prediction.")

# Enable TCP Networking Client Defaults To Localhost Port 9999
parser.add_argument("-network", action="store_true", help="Enable TCP Network Stream Sat Name, Latitude, Longitude and Altitude over TCP Network.")
# Define Custom Host &/Or Port For TCP Client 
parser.add_argument("-host", dest="tcp_host", default="127.0.0.1", help="TCP Network Host IP Address.")
parser.add_argument("-port", dest="tcp_port", default=9999, help="TCP Network Port.")

# Enable Serial Port For Celestron Telescope Mount & Set Min Elevation Point Of Movement
parser.add_argument("-com", dest="serial_port",  help="Mount Serial Port.")
parser.add_argument("-min", dest="minMount", default=10, help="Minimum Mount Elevation Prior To Movement.")

# Disable AOS Sounds (Used When Sleeping), All Other Functions Will Operate
parser.add_argument("-s", action="store_true", help="Silent Mode (Disable AOS Alert Sounds).")


#
# Define The Parser
#
args = parser.parse_args()

#
# Satelites To Track
#

if args.weather:

   satList = ["METEOR-M 2", "NOAA 19", "NOAA 18", "NOAA 15"]

elif args.afsk:

   satList = ["PCSAT (NO-44)", "ISS (ZARYA)"]

elif args.fm:

   satList = ["RADFXSAT (FOX-1B)", "FOX-1CLIFF (AO-95)", "FOX-1D (AO-92)", "SAUDISAT 1C (SO-50)"]

elif args.bpsk:

   satList = ["JY1SAT (JO-97)", "FUNCUBE-1 (AO-73)", "NAYIF-1 (EO-88)"]

elif args.custom:

   satList = [args.custom]

else:

   satList = ["ISS (ZARYA)"]


#
# If network & TCP Host Port
#

if args.network:

   if args.tcp_host:
      host = args.tcp_host

   if args.tcp_port:
      port = int(args.tcp_port)


#
#  Define The Tracker
#

tracker = satTracker.SatTracker()

#
#  Set The Ground Stations Latitude & Longitude
#

if args.latitude and args.longitude:
   tracker.lat = args.latitude
   tracker.lon = args.longitude

#
# Connect To Remote Server & Ouput Lat, Lon
#

if args.network:
   client = tracker.connectClient(host, port)
   tracker.socket = True
else:
   client = None


#
# Connect To Telescope Mount (default: None)
#

if args.serial_port:
   tracker.port = args.serial_port

   if args.minMount:
      tracker.minMountElevation = int(args.minMount)
      print(tracker.minMountElevation)


#
# Set Minimum Elevation For Prediction (default: 15)
#

if args.elevation:
   tracker.minElevation = int(args.elevation)


#
# Disable AOS Sound
#

if args.s:
   print("Disabling AOS Alerts")
   tracker.sound = False


#
# Custom TLE File For Offline Use
#

if args.custom_tle:
   tracker.tle_file = args.custom_tle

#
# Return Next Pass Information
#

aos = tracker.FindPass(satList)

#
# Track The Sats
#

try:

   for sat in sorted(aos, key=lambda k: k["startPass"]):
      tracker.satName = sat["satName"]
      tracker.tracker(client, sat["startPass"], sat["maxEle"], sat["endPass"])

except KeyboardInterrupt:
   pass

