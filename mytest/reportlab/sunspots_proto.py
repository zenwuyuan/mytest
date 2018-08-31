from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF
import urllib.request


data = [
    (2007,8,113.2,114.3,112.2),
    (2007,9,112.8,115.8,109.8),
    (2007,10,111.0,116.0,106.0),
    (2007,11,109.8,116.8,102.8),
    (2007,12,107.3,115.3,99.3),
    (2008,1,105.2,114.2,96.2),
    (2008,2,104.1,114.1,96.2),
    (2008,3,99.3,110.9,88.9),
    (2008,4,94.8,106.8,82.8),
    (2008,5,91.2,104.2,78.2),
    ]

data = []
for line in urllib.request.urlopen('ftp://ftp.swpc.noaa.gov/pub/weekly/Predict.txt').readlines():
    line = line.decode()
    if not line.isspace() and not line[0] in ['#',':']:
        data.append([float(n) for n in line.split()])


drawing = Drawing(200,150)

pred = [row[2]-40 for row in data]
high = [row[3]-40 for row in data]
low = [row[4]-40 for row in data]
print(pred)
times = [200*((row[0] + row[1]/12.0) - 2007)-110 for row in data]

drawing.add(PolyLine(list(zip(times,pred)),strokeColor=colors.blue))
drawing.add(PolyLine(list(zip(times,high)),strokeColor=colors.red))
drawing.add(PolyLine(list(zip(times,low)),strokeColor=colors.green))

drawing.add(String(65,115,'Sunspots',fontSize = 18,fillColor = colors.red))
renderPDF.drawToFile(drawing,'sunspots_proto.pdf','Sunspots')



data1 = []
for line in urllib.request.urlopen('ftp://ftp.swpc.noaa.gov/pub/weekly/Predict.txt').readlines():
    line = line.decode()
    if not line.isspace() and not line[0] in ['#',':']:
        data1.append([float(n) for n in line.split()])

print(data1)
