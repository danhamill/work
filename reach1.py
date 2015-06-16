import PyHum
import os
from glob import glob

os.chdir(os.path.normpath(os.path.join(os.path.expanduser('~'), 'Reach_1', '2013_12')))
list1 = glob('*')

path = 'c:\\'

os.chdir(os.path.normpath(os.path.join(path, 'workspace', 'Reach_4a', 'Python_Scripts')))

num = 4 

#general settings   
humfile = os.path.normpath(os.path.join(os.path.expanduser('~'), 'Reach_1', '2013_12', list1[num], list1[num] +'.DAT'))
sonpath = os.path.normpath(os.path.join(os.path.expanduser('~'), 'Reach_1', '2013_12', list1[num]))
doplot = 1 #yes
#print humfile+ '\n'
#print sonpath+ '\n' 
# reading specific settings
cs2cs_args = "epsg:26949" #arizona central state plane
bedpick = 1 # auto bed pick
c = 1450 # speed of sound fresh water
t = 0.108 # length of transducer
f = 455 # frequency kHz
draft = 0.3 # draft in metres
flip_lr = 1 # flip port and starboard
model = 998 # humminbird model
#chunk_size = 1000 # chunk size = 1000 pings
chunk_size = 0 # auto chunk size

# correction specific settings
maxW = 1000 # rms output wattage

# for texture calcs
win = 50 # pixel window
shift = 10 # pixel shift
density = win/2 
numclasses = 4 # number of discrete classes for contouring and k-means
maxscale = 20 # Max scale as inverse fraction of data length (for wavelet analysis)
notes = 4 # Notes per octave (for wavelet analysis)

# for mapping
dogrid = 1 # yes
calc_bearing = 0 #no
filt_bearing = 1 #yes
res = 0.2 # grid resolution in metres
cog = 1 # GPS course-over-ground used for heading

# for downward-looking echosounder echogram (e1-e2) analysis
ph = 7.0 # acidity on the pH scale
temp = 10.0 # water temperature in degrees Celsius
salinity = 0.0
beam = 20.0
transfreq = 200.0
integ = 5
numclusters = 3

PyHum.read(humfile, sonpath, cs2cs_args, c, draft, doplot, t, f, bedpick, flip_lr, chunk_size, model)
#
PyHum.correct(humfile, sonpath, maxW, doplot)

#PyHum.texture(humfile, sonpath, win, shift, doplot, density, numclasses, maxscale, notes)

#PyHum.map(humfile, sonpath, cs2cs_args, dogrid, calc_bearing, filt_bearing, res, cog)

#res = 0.5 # grid resolution in metres

#PyHum.map_texture(humfile, sonpath, cs2cs_args, dogrid, calc_bearing, filt_bearing, res, cog)

#PyHum.e1e2(humfile, sonpath, cs2cs_args, ph, temp, salinity, beam, transfreq, integ, numclusters, doplot)


