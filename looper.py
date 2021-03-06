import PyHum
import os
from glob import glob
path = 'E:\\'	#USGS computer
path2 = 'C:\\'
path3 = 'D:\\'	#USU Computer

date= '2015_04'

os.chdir(os.path.normpath(os.path.join(path3, 'R4a', date)))
list1 = glob('*')


os.chdir(os.path.normpath(os.path.join(path2,'workspace', 'Reach_4a', 'Python_Scripts')))

numlist = [2]

def runthis(items):
   num = items
   #general settings   
   humfile = os.path.normpath(os.path.join('D:\\', 'R4a', date, list1[num], list1[num] +'.DAT'))
   sonpath = os.path.normpath(os.path.join('D:\\', 'R4a', date, list1[num]))
   doplot = 1 #yes


   # reading specific settings
   cs2cs_args = "epsg:26949" #arizona central state plane
   bedpick = 1 # auto bed pick
   c = 1450 # speed of sound fresh water
   t = 0.108 # length of transducer
   f = 455 # frequency kHz of sidescan sonar
   draft = 0.3 # draft in metres
   flip_lr = 1 # flip port and starboard
   model = 998 # humminbird model
   chunk_size = 1000 # chunk size = 1000 pings
   #chunk_size = 0 # auto chunk size
   cog = 1 # GPS course-over-ground used for heading
   calc_bearing = 0 #no
   filt_bearing = 1 #yes
    
   # correction specific settings
   maxW = 1000 # rms output wattage
   dofilt = 1 # apply a phase preserving filter (WARNING!! takes a very long time for large scans)

   # for shadow removal
   shadowmask = 0 #automatic shadow removal

   # for texture calcs
   win = 100 # pixel window
   shift = 10 # pixel shift
   density = win/2 
   numclasses = 4 # number of discrete classes for contouring and k-means
   maxscale = 20 # Max scale as inverse fraction of data length (for wavelet analysis)
   notes = 4 # Notes per octave (for wavelet analysis)

   # for mapping
   dogrid = 1 # yes
   res = 0.1 # grid resolution in metres
   mode = 1 # gridding mode (simple nearest neighbour)
   #mode = 2 # gridding mode (inverse distance weighted nearest neighbour)
   #mode = 3 # gridding mode (gaussian weighted nearest neighbour)
   dowrite = 0 #disable writing of point cloud data to file

   nn = 64 #number of nearest neighbours for gridding (used if mode > 1)
   influence = 1 #Radius of influence used in gridding. Cut off distance in meters 
   numstdevs = 4 #Threshold number of standard deviations in sidescan intensity per grid cell up to which to accept 

   # for downward-looking echosounder echogram (e1-e2) analysis
   ph = 7.0 # acidity on the pH scale
   temp = 10.0 # water temperature in degrees Celsius
   salinity = 0.0
   beam = 20.0
   transfreq = 200.0 # frequency (kHz) of downward looking echosounder
   integ = 5
   numclusters = 3 # number of acoustic classes to group observations
   
   # # read data in SON files into PyHum memory mapped format (.dat)
   # PyHum.read(humfile, sonpath, cs2cs_args, c, draft, doplot, t, f, bedpick, flip_lr, chunk_size, model, calc_bearing, filt_bearing, cog)

   # # correct scans and remove water column
   # PyHum.correct(humfile, sonpath, maxW, doplot, dofilt)

   # # remove acoustic shadows (caused by distal acoustic attenuation or sound hitting shallows or shoreline)
   # PyHum.rmshadows(humfile, sonpath, win, shadowmask, doplot)

   # # Calculate texture lengthscale maps using the method of Buscombe et al. (2015)
   # PyHum.texture(humfile, sonpath, win, shift, doplot, density, numclasses, maxscale, notes)

   # grid and map the scans
   PyHum.map(humfile, sonpath, cs2cs_args, dogrid, res, dowrite, mode, nn, influence, numstdevs)

   res = 0.5 # grid resolution in metres
   numstdevs = 5
   
   # grid and map the texture lengthscale maps
   PyHum.map_texture(humfile, sonpath, cs2cs_args, dogrid, res, dowrite, mode, nn, influence, numstdevs)

   # calculate and map the e1 and e2 acoustic coefficients from the downward-looking sonar
   PyHum.e1e2(humfile, sonpath, cs2cs_args, ph, temp, salinity, beam, transfreq, integ, numclusters, doplot)
for items in numlist:
   if __name__ == '__main__':
      runthis(items)