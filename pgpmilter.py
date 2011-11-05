#!/usr/bin/python

"""PGPMilter is a milter using python-milter that rejects all non-GPG mail.
Thrown together in 2011 by Moritz Bartl 

> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.

> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.

> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.

See the pymilter project at http://bmsi.com/python/milter.html
based on Sendmail's milter API http://www.milter.org/milter_api/api.html

"""

import Milter
import StringIO
import time
import email
import sys
import os
from socket import AF_INET, AF_INET6
from Milter.utils import parse_addr
if True:
  from multiprocessing import Process as Thread, Queue
else:
  from threading import Thread
  from Queue import Queue

_PGPHEADER = "-----BEGIN PGP MESSAGE-----"
maxmsglen = 5000
socket = os.getenv("HOME") + "/milter/pgpmilter.sock"

class pgpMilter(Milter.Base):

  def __init__(self):  # A new instance with each new connection.
    self.id = Milter.uniqueID()  # Integer incremented with each call.
    self.mailbody = None

  @Milter.noreply
  def connect(self, IPname, family, hostaddr):
    self.mailbody = StringIO.StringIO()
    return Milter.CONTINUE

  def body(self, chunk):
    self.mailbody.write(chunk)
    currentBody = self.mailbody.getvalue()
    if currentBody.find(_PGPHEADER)>-1:
      return Milter.ACCEPT 
    if len(currentBody) > maxmsglen:
      self.setreply('550','5.7.1','We only accept PGP encrypted mail. PGP header not found within %s first characters of body' % maxmsglen)
      return Milter.REJECT
    return Milter.CONTINUE

  # end of mail
  def eom(self):
    self.setreply('550','5.7.1','We only accept PGP encrypted mail')
    return Milter.REJECT

## ===
    
def main():
  bt = Thread()
  bt.start()
  timeout = 60
  # Register with Milter factory 
  Milter.factory = pgpMilter
  # we don't modify mails, so no flags
  Milter.set_flags(0)
  Milter.runmilter("pgpmilter",socket,timeout)
  bt.join()

if __name__ == "__main__":
  if len(sys.argv) >= 2:
    socket = sys.argv[1] 
  if len(sys.argv) >= 3:
    maxmsglen = sys.argv[2]
  main()
