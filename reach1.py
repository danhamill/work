import PyHum
import os
from glob import glob

os.chdir(os.path.normpath(os.path.join('E:\\', 'Reach_1', '2013_12')))
list1 = glob('*')

path = 'E:\\'
path2 = 'C:\\'

os.chdir(os.path.normpath(os.path.join(path2,'users','dhamill', 'scripts', 'work')))

num = 12

def runthis():
   #general settings   
   humfile = os.path.normpath(os.path.join(path, 'Reach_1', '2013_12', list1[num], list1[num] +'.DAT'))
   sonpath = os.path.normpath(os.path.join(path, 'Reach_1', '2013_12', list1[num]))
   doplot = 1 #yes
   #print humfile+ '\n'
   #print sonpath+ '\n' 
   # reading specific settings
   cs2cs_args = "epsg:26949" #arizona central state plane
   bedpick = 1 # 1 for auto bed pick, 2 for manual
   c = 1450 # speed of sound fresh water
   t = 0.108 # length of transducer
   f = 455 # frequency kHz
   draft = 0.3 # draft in metres
   flip_lr = 1 # flip port and starboard
   model = 998 # humminbird model
   chunk_size = 1000 # chunk size = 1000 pings
   #chunk_size = 0 # auto chunk size
   
   # correction specific settings
   maxW = 1000 # rms output wattage
   dowrite = 1
   
   # for texture calcs
   win = 50 # pixel window
   shift = 10 # pixel shift
   density = win/2 
   numclasses = 4 # number of discrete classes for contouring and k-means
   maxscale = 20 # Max scale as inverse fraction of data length (for wavelet analysis)
   notes = 4 # Notes per octave (for wavelet analysis)
   
   # for shadow removal
   shadowmask = 0 #automatic shadow removal
   kvals = 8 # number of k-means for automated shadow removal# for mapping
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
   
   # read data in SON files into PyHum memory mapped format (.dat)
   PyHum.read(humfile, sonpath, cs2cs_args, c, draft, doplot, t, f, bedpick, flip_lr, chunk_size, model)
   
   # correct scans and remove water column
   PyHum.correct(humfile, sonpath, maxW, doplot)
   
   # remove acoustic shadows (caused by distal acoustic attenuation or sound hitting shallows or shoreline)
   PyHum.rmshadows(humfile, sonpath, win, shadowmask, kvals, doplot)
   
   # Calculate texture lengthscale maps using the method of Buscombe et al. (2015)
   PyHum.texture(humfile, sonpath, win, shift, doplot, density, numclasses, maxscale, notes)
   
   # grid and map the scans
   PyHum.map(humfile, sonpath, cs2cs_args, dogrid, calc_bearing, filt_bearing, res, cog, dowrite)
   
   res = 0.5 # grid resolution in metres
   
   # grid and map the texture lengthscale maps
   PyHum.map_texture(humfile, sonpath, cs2cs_args, dogrid, calc_bearing, filt_bearing, res, cog, dowrite)
   
   # calculate and map the e1 and e2 acoustic coefficients from the downward-looking sonar
   PyHum.e1e2(humfile, sonpath, cs2cs_args, ph, temp, salinity, beam, transfreq, integ, numclusters, doplot)
 
if __name__ == '__main__':
   runthis()