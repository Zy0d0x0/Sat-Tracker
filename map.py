import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import socket, argparse

#
# Show Menu
#

parser = argparse.ArgumentParser(
   add_help=False,
   formatter_class=argparse.RawDescriptionHelpFormatter, # This will fix description and epilog format
   epilog="Examples: %(prog)s -host 127.0.0.1 -p 4444")

## Adds arguments to help menu
parser.add_argument("-h", action="help",  help="Print this help message then exit")
parser.add_argument("-host", dest="host", default="127.0.0.1", help="TCP Network Host IP Address")
parser.add_argument("-port", dest="port", default=9999, help="TCP Network Port")


args = parser.parse_args()





bind_ip = args.host
bind_port = args.port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print('Listening on {}:{}'.format(bind_ip, bind_port))

plt.figure(figsize=(7, 7))


def draw_map(plt,satName, lat, lon, pathLat, pathLon):

   try:

      m = Basemap(projection='ortho', resolution=None, lat_0=lat, lon_0=lon)
      m.bluemarble(scale=0.5)

      pathLat.append(lat)
      pathLon.append(lon)

      x, y = m(lon, lat)

      plt.text(x, y, satName, fontsize=12,fontweight='bold',
               ha='left',va='bottom',color='red')

      x, y = m(pathLon,pathLat)

      plt.plot(x, y, marker=None, color='yellow')

      plt.draw()
      plt.pause(1)
      plt.clf()
      
   except:
         pass





def clean_data(request):

   try:

      packetCheck = str(request, 'utf-8').count('#')

      if packetCheck == 1:

         satName, lon, lat, alt, terminator = str(request, 'utf-8').split(',')

         lat = float(lat)
         lon = float(lon)
         alt = float(alt)

         return satName, lat, lon, alt

      else:
         raise('Malformed Packet')

   except:
      return None, 0.0, 0.0, 0.0      


def handle_client_connection(client_socket, plt):

   pathLat = [] 
   pathLon = []
   saveSat = []

   while 1:

      try:

         request = client_socket.recv(1024)
         print('Received {}'.format(request))

         satName, lat, lon, alt = clean_data(request)

         if satName is not None:
            draw_map(plt, satName, lat, lon, pathLat, pathLon)

         else:
            print("Skipping Malformed Packet")

         client_socket.send(b'ACK!')

      except:
         break

   client_socket.close()

while True:
   client_sock, address = server.accept()
   print('Accepted connection from {}:{}'.format(address[0], address[1]))
   handle_client_connection(client_sock, plt)  
