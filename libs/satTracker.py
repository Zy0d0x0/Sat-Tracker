#! /usr/bin/env python3

from pyorbital.orbital import Orbital
from datetime import datetime, timedelta
from time import strftime, gmtime, localtime
import geopy.distance
from libs import nexstar as ns
from playsound import playsound
import time, os, socket, sys


# Change Client To Server

class SatTracker():

   #
   # Define Serial Port For Nexstar Telescope Mount
   #

   port = None

   #
   # Send Data Over TCP Socket 
   #

   socket = False

   #
   # Minimum Satelite Elevation
   #

   minElevation = 0

   #
   # Define Satelite To Track
   #

   satName = None

   #
   # Set Home Postion 
   #

   lat = 0.0     # Latitude
   lon = 0.0     # Set Longitude
   alt = 0.0     # Set Altitude

   #
   # Disable / Enable AOS Sound
   #

   sound = True

   #
   # Minumum Mount Elevation Prior To Hardware Movment Of Telescope
   #

   minMountElevation = 0

   #
   # Custom TLE File For Offline Use
   #

   tle_file = None

   #
   # Adjust Clock UTC/BST Daylight Savings
   #

   delta =  datetime.now() - datetime.utcnow()
   delta = str(delta).strip(":")[0]
   offset = timedelta(hours=int(delta))

   #
   # This Will Return The Predicted Pass Time For 24 Hours
   #

   def NextPasses(self, orb):
      aos = []

      print("Searching Passes For {} (UTC +{})".format(self.satName, self.offset))

      NexPasses = orb.get_next_passes(datetime.utcnow(), 
      24, self.lon, self.lat, self.alt, horizon=self.minElevation)

      for Pass in NexPasses:
         RiseTime, FallTime, MaxEle = Pass

         aos.append(
         {

         "satName": self.satName, 
         "startPass" : str(RiseTime + self.offset), 
         "maxEle" : str(MaxEle + self.offset),
         "endPass" : str(FallTime + self.offset)

         })

      return aos

   #
   # Find Passes For Multiple Sats
   #

   def FindPass(self, satList):
      Pass = []

      for satName in satList:
         self.satName = satName
         orb = self.tleCheck()
         aos = self.NextPasses(orb)

         for passes in aos:
            Pass.append(passes)

      return Pass

   #
   # Check If Custom TLE Supplied Or Use Internet
   #

   def tleCheck(self):

      if self.tle_file is not None:

         try:
            orb = Orbital(self.satName, tle_file=self.tle_file)
         except KeyError:
            print("Satalite Not Found Offline, Check Satalite Exists In TLE File")
            sys.exit(0)

      else:

         try:
            orb = Orbital(self.satName)
         except KeyError:
            print("Satalite Not Found Online, Try Using -custom-tle")
            sys.exit(0)

      return orb

   #
   # Current GMT Time
   #

   def findCurrentTime(self):
 
      local = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

      return local


   #
   # Find Latitude & Longitude Of Sat
   #

   def SatLocationLatLon(self, orb):
      now = datetime.utcnow()
      return orb.get_lonlatalt(now)

   #
   # Find The Azimuth Of The Sat
   #

   def SatAzimuthElevation(self, orb):
      now = datetime.utcnow()
      return orb.get_observer_look(now, self.lon, self.lat, self.alt)

   #
   # Find The Distance Of The Sat
   #

   def SatDistance(self, lat, lon):
      Satelite = (lat, lon)
      Ground_Station = (self.lat, self.lon)
      distanceMiles = geopy.distance.distance(Satelite,Ground_Station).miles
      distanceKilometers = geopy.distance.distance(Satelite,Ground_Station).km
      return int(distanceMiles), int(distanceKilometers)

   #
   # Find The Direction Of Satlite
   #

   def direction_lookup(self, degrees_temp):
      if degrees_temp < 0:
         degrees_final = 360 + degrees_temp
      else:
         degrees_final = degrees_temp
      compass_brackets = ["North", "North East", "East", "South East", 
                          "South", "South West", "West", "North West", "North"]
      compass_lookup = round(degrees_final / 45)
      return compass_brackets[int(compass_lookup)]

   #
   # Find The Location Of Sat On Compass
   #

   def SatHeading(self, azimuth):
      return self.direction_lookup(azimuth)

   #
   # Move The Mount To Satelite Position
   #

   def mountMovePostion(self, compass_angle, elevation, controller):

      gotoInProgress = controller.getGotoInProgress()  
 

      if not gotoInProgress and int(elevation) >= 0:
         print("Moving Mount To {} Postion".format(self.satName))
         controller.gotoPosition(compass_angle, elevation)

   #
   # Get The Current Postion Of The Mount
   #

   def mountGetPostion(self, controller):

      if self.port is not None:
         controllerAzimuth, controllerElevation = controller.getPosition()

         if int(controllerAzimuth) == 359:
            controllerAzimuth = 0.0
         if int(controllerElevation) == 359:
            controllerElevation = 0.0

         return controllerAzimuth, controllerElevation

   #
   # Make Mount Go Home Postion
   #

   def mountGoHome(self, controller):

      print("Setting Home Postion Of Mount")
      self.mountMovePostion(0.0, 0.0, controller)


   #
   # Connect To Telescope Mount
   #

   def connectMount(self):
      if self.port is not None:
         try:

            print("Connecting To Mount")
            controller = ns.NexstarHandController(self.port)

            #Get A Bigger Cable Until Worked Out, Yeah Big No No
            #self.mountGoHome(controller)

         except:
 
            print("Failed To Connect To Mount - Skipping")
            time.sleep(1)
            self.port = None
            controller = None

      return controller


   #
   # Connect To TCP Server
   #

   def connectClient(self, address, port):

      try:
         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         client.connect((address, int(port)))
         return client
      except:
         print("Failed To Connect To Host")
         time.sleep(1)
         self.socket = False



   #
   # Send Data To TCP Server
   #

   def sendData(self, client, lon, lat, alt):

      try:

         message = "{},{:.2f},{:.2f},{:.2f},#".format(self.satName, lon, lat, alt)
         client.send(message.encode())

      except:
            print("Failed To Send Packet")
            self.socket = False


   #
   # Print Results
   #

   def showResults(self, orb, currLocal, startPass, MaxEle, endPass):

      os.system("cls || clear")
              
      print("Tracking: {}\n".format(self.satName))

      print("Time: {} (UTC +{})\n".format(currLocal, self.offset))

      print("AOS: {}".format(startPass))
      print("Max: {}".format(MaxEle))
      print("LOS: {}\n".format(endPass))

      lon, lat, alt = self.SatLocationLatLon(orb)             
      print("Latitude: {}\nLongitude: {}".format(lat,lon))
      print("Altitude: {:.2f} Kilometres\n".format(alt))

      miles, km = self.SatDistance(lat, lon)
      print("Distance Miles: {}".format(miles))
      print("Distance Kilometres: {}".format(km))

      azi, ele = self.SatAzimuthElevation(orb)
      heading = self.SatHeading(azi)
      print("Approaching From: {}\n".format(heading))

      print("Azimuth: {:.2f}".format(azi))
      print("Elevation: {:.2f}{}\n".format(ele, u"\u00b0"))

      return lat, lon, alt, ele, azi


   #
   # Track The Sats
   #


   def tracker(self, client, startPass, MaxEle, endPass):

      if self.port is not None:
         controller = self.connectMount()

      orb = self.tleCheck()

      while 1:

   
         currLocal = self.findCurrentTime()
         startPass = startPass.split(".")[0]
         MaxEle = MaxEle.split(".")[0]
         endPass = endPass.split(".")[0]
         lat, lon, alt, ele, azi = self.showResults(orb, currLocal, startPass, MaxEle, endPass)

         #
         # Display & Move Telescope Mount To Postion
         #

         if self.port is not None:
            controllerAzimuth, controllerElevation = self.mountGetPostion(controller)
            print("Mount Azimuth: {:.2f}".format(controllerAzimuth))
            print("Mount Elevation: {:.2f}{}\n".format(controllerElevation, u"\u00b0"))

            if int(ele) >= self.minMountElevation:
               self.mountMovePostion(azi, ele, controller)

         #
         # Send Data To Socket Server
         #

         if self.socket:
            self.sendData(client, lon, lat, alt)

         #
         # Play AOS Alert Tone 
         #

         if currLocal in startPass:
            if self.sound:
               playsound('alert.wav')


         if currLocal >= endPass:
            break
   

         #
         # Sleep For A Second As So Stats Can Be Seen
         #
         time.sleep(1)

   
