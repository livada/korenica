import re
from datetime import datetime
        
class IGCPoint(object):
    def __init__(self, lat, lon, alt, time):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.time = time
        
    def xy(self):
        return self.lat, self.lon
        
class IGCReader(object):
    igc_line_re = re.compile(r'B(?P<time>\d{6})(?P<lat>\d{7}[NS])(?P<lon>\d{8}[WE])A(?P<baro>\d{5})(?P<GNSS>\d{5})')

    def __init__(self, filename):
        self.track = []
        with open(filename, 'r') as f:
            for line in f:
                m = IGCReader.igc_line_re.match(line)
                if m is not None:
                    md = m.groupdict() 
                    ts = datetime.strptime(md['time'], "%H%M%S")
                    alt = float(md['GNSS'])
                    lat = (1.0 if md['lat'][7]=='N' else -1.0) * (float(md['lat'][0:2]) + float(md['lat'][2:4]+'.'+md['lat'][4:7])/60)
                    lon = (1.0 if md['lon'][8]=='E' else -1.0) * (float(md['lon'][0:3]) + float(md['lon'][3:5]+'.'+md['lon'][5:8])/60)
                    self.track.append(IGCPoint(lat, lon, alt, ts))
                            

