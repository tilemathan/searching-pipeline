#!/usr/bin/python
from sigpyproc.Readers import *

import sys

FIL = sys.argv[1]
Start = int(sys.argv[2])
End = int(sys.argv[3])
Name = sys.argv[4]

F = FilReader(FIL)
F.split(Start,End,Name)
