from qgis.core import *
from qgis.gui import *
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from datetime import datetime, timedelta

start = datetime.strptime("01-01-1979", "%d-%m-%Y")
end = datetime.strptime("31-12-2011", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/TIFF/"

for date in date_generated:

    day = int(date.strftime("%Y%m%d"))
     
    d = datetime.strptime(str(day), '%Y%m%d')
    time_needed = [d + timedelta(hours = 12), d + timedelta(days = 1)]
    
    Layer = QgsRasterLayer(path + "daily-prec_" + str(day) + ".tiff")
    
    entries = []
     
    # Define band1
    layer1 = QgsRasterCalculatorEntry()
    layer1.ref = 'layer1@1'
    layer1.raster = Layer
    layer1.bandNumber = 1
    entries.append( layer1 )
    
    calc = QgsRasterCalculator('((layer1@1) >= 0) * layer1@1 * 1000', 
                                path + 'daily-prec_' + str(day) + '.tiff', 
                                'GTiff', 
                                Layer.extent(), 
                                Layer.width(), 
                                Layer.height(), 
                                entries )
                                 
    calc.processCalculation()