from PyQt4.QtGui import QProgressBar
from PyQt4.QtCore import Qt
import os

os.chdir(os.path.normpath(os.path.join(path2,'users','dhamill', 'scripts', 'work','rasterhome')))

l = iface.activeLayer()
w = l.width()
h = l.height()
p = l.dataProvider()
b = p.block(0, p.extent(), w, h)
f = file('test1.xyz', 'w')
f.write('Easting,Northing,Elevation\n')
pix_x = l.rasterUnitsPerPixelX()
pix_y = l.rasterUnitsPerPixelY()
half_x = pix_x / 2
half_y = pix_y / 2
 
bar = QProgressBar(None)
bar.setMaximum(h)
bar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
progressMessageBar = iface.messageBar().createMessage("Exporting to XYZ...")
progressMessageBar.layout().addWidget(bar)
iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)
 
extent = p.extent()
 
count = 0
y = extent.yMinimum()
while y < extent.yMaximum():
    y += pix_y
    bar.setValue(count)
    count += 1
    x = extent.xMinimum()
    while x < extent.xMaximum():
        
        x += pix_x
        pos = QgsPoint(x - half_x, y - half_y)
        result = p.identify(pos, QgsRaster.IdentifyFormatValue).results()[1]
        if result > 0:
            f.write('%s,%s,%s\n' % (pos.x(), pos.y(), result))
f.close()
iface.messageBar().clearWidgets()