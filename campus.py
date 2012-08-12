from ctypes import cdll, c_long, c_double, c_bool, c_char_p

import os

if os.name=='posix':
    lib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),'libCampus.so'))
else:
    lib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),'libCampus.dll'))

lib.CampusTask_number_of_wpts.restype = c_long
lib.CampusTask_get_waypoints.restype = c_char_p
lib.CampusTask_make_cylinder.restype = c_char_p
lib.CampusTask_get_total_distance.restype = c_double
lib.CampusTask_get_goal_penalty.restype = c_double
lib.CampusTask_in_goal.restype = c_bool

# CampusTask wrapper
class CampusTaskWrapper(object):
    def __init__(self):
        self.obj = lib.CampusTask_new()

    def flush_task(self):
        lib.CampusTask_flush_task(self.obj)

    def flush_track(self):
        lib.CampusTask_flush_track(self.obj)

    def push_task_cylinder(self, lat, lon, radius):
        lib.CampusTask_push_task_cylinder(self.obj, c_double(lat), c_double(lon), c_double(radius))

    def push_track_point(self, lat, lon):
        lib.CampusTask_push_track_point(self.obj, c_double(lat), c_double(lon))

    def do_calculation(self):
        lib.CampusTask_do_calculation(self.obj)

    def number_of_wpts(self):
        return lib.CampusTask_number_of_wpts(self.obj)

    def get_waypoints(self):
        return lib.CampusTask_get_waypoints(self.obj)

    def make_cylinder(self, lat, lon, radius):
        return lib.CampusTask_make_cylinder(self.obj, c_double(lat), c_double(lon), c_double(radius))

    def get_total_distance(self):
        return lib.CampusTask_get_total_distance(self.obj)

    def get_goal_penalty(self):
        return lib.CampusTask_get_goal_penalty(self.obj)

    def in_goal(self):
        return lib.CampusTask_in_goal(self.obj)

class CampusTrack(object):
    def __init__(self, track):
        self.track = track
        self.waypoints = None
        
        self.total_distance = None
        self.goal_penalty = 0.0
        self.time_penalty = 0.0
        
        self.avg_speed = 0.0
        self.penalty_seconds = 0.0
        
        self.in_goal = False

        self.score = 0.0

    def export_kml(self, filename):
        header = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
    xmlns:gx="http://www.google.com/kml/ext/2.2">
  <Document>
    <name>Waypoints</name>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>Path</name>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>
'''
#          15.821767,44.705567,607.00
        footer = '''
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
'''
        with open(filename, 'w') as f:
            f.write(header)
            for wpt in self.waypoints:
                f.write('  %f,%f,0 \n' % (wpt[1], wpt[0]))
            f.write(footer)

from igcutils import IGCReader
from datetime import datetime

class CampusTask(CampusTaskWrapper):
    def __init__(self, task, max_time=2*3600+15*60+46):
        super(CampusTask, self).__init__()
        self.cylinders = task
        self.max_time = max_time
        for c in task:
            self.push_task_cylinder(*c)

    def process(self, track):
        total_time = 2*3600 + 15*60 + 46 # seconds
        
        if isinstance(track, list):
            track = CampusTrack(track)
            print 'Warning: No time data!'
        elif isinstance(track, IGCReader):
            
            # TODO: Crop still points.
            
            
            # TODO: Calculate time penalty. 
            start_time = track.track[0].time
            end_time = track.track[len(track.track)-1].time
            time_diff = (end_time - start_time).total_seconds() - self.max_time
            time_penalty = time_diff if time_diff>0 else 0.0 # seconds
            
            track = CampusTrack([p.xy() for p in track.track]) # if (p.time-start_time).total_seconds()<self.max_time])
        else:
            print 'Warning: No time data!'
            
        for p in track.track:
            self.push_track_point(*p)
        
        self.do_calculation()
        
        track.in_goal = self.in_goal()
        track.total_distance = self.get_total_distance()
        track.goal_penalty = self.get_goal_penalty()
        track.penalty_seconds = time_penalty
        
        # Apply time penalty.
        track.avg_speed = track.total_distance / total_time
        track.time_penalty = track.avg_speed * track.penalty_seconds
        track.score = (track.total_distance - track.goal_penalty - track.time_penalty) * 10
        
        track.waypoints = [track.track[int(i)] for i in self.get_waypoints().split('|')]
 
        self.flush_track()
       
        return track
        
    def export_kml(self, filename):
        header = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
    xmlns:gx="http://www.google.com/kml/ext/2.2">
  <Document>
    <name>Task</name>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>1</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff10</color>
      </PolyStyle>
    </Style>
'''
        placemark_begin = '''
    <Placemark>
      <name>Cylinder</name>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>
'''
#          15.821767,44.705567,607.00
        placemark_end = '''
        </coordinates>
      </LineString>
    </Placemark>
'''
        footer = '''
  </Document>
</kml>
'''
        with open(filename, 'w') as f:
            f.write(header)
            for cyl in self.cylinders:
                pts = self.make_cylinder(*cyl).split('|')[:-1]
                f.write(placemark_begin)
                for point in pts:
                    p = point.split(',')
                    f.write('  %s,%s,3000.0 \n' % (p[1], p[0]))
                f.write(placemark_end)
            f.write(footer)
        
        
        
        
