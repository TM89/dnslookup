import socket
import datetime
import time
import dbus
from urlparse import urlparse
import sys

sitenotup = True
ip = ''
bus = dbus.SessionBus()
notifications = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
interface = dbus.Interface(notifications, 'org.freedesktop.Notifications')
id = 4856


def notify(title, body, timeout = None):
  if timeout == None:
    timeout = 2500
  interface.Notify(title, id, '', title, body, '', '', timeout)

def is_valid_ipv4(address):
  try:
    socket.inet_pton(socket.AF_INET, address)
  except AttributeError:
    try:
      socket.inet_aton(address)
    except socket.error:
      return False
    return address.count('.')
  except socket.error:
    return False
  return True
  
def is_valid_ipv6(address):
  try:
    socket.inet_pton(socket.AF_INET6, address)
  except socket.error:
    return False
  return True

  
print 'Program started'  
print 'Enter name of site: '
address = raw_input()
parseresult = urlparse(address)
print parseresult
if parseresult.netloc == '':
  print 'Not a valid url, program terminated.'
  sys.exit(0)
  
address = parseresult.netloc

while sitenotup:
  try:
    ip = socket.gethostbyname(address)
    if is_valid_ipv4(ip) or is_valid_ipv6:
      notify('Host is up!', 'Found the site ' + address + ' at ' + ip, 2500)
      sitenotup = False
  except socket.gaierror:
    print 'Host not reachable' + datetime.datetime.now().time().isoformat()
  time.sleep(30)
  
print 'Program terminated.'
