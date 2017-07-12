import glob, os
import re

from igcutils import IGCReader


def get_points_from_kml(filename):
    points = []
    with open(filename, 'r') as f:
        for l in f:
            try:
                coords = map(float, l.split(','))
                points.append(coords)
            except ValueError:
                pass
    return points


def pack_json(task, args):
    pack_str = '{cylinders:' + task.get_json()

    print 'Writing cylinders'

    pilotlist = []

    pilot_pattern = re.compile('(?P<pilotname>.*)%s' % args.track_suffix)
    for igc_file in glob.glob('*' + args.track_suffix):
        m = pilot_pattern.match(igc_file)
        pilotname = m.group('pilotname')
        print 'Pilot: %s [' % pilotname,

        task_file = pilotname + args.task_suffix
        task_poly_file = pilotname + args.task_poly_suffix

        igc = IGCReader(igc_file)
        pilot_parts = ['name:"%s"' % pilotname]
        pilot_parts.append('track:[' + ','.join(['{lat:%f,lon:%f}' % (p.lat, p.lon) for p in igc.track]) + ']')
        pilot_parts.append('graph:[' + ','.join(['{%s,%f}' % (p.time.time(), p.alt) for p in igc.track]) + ']')

        if os.path.exists(task_file):
            plist = get_points_from_kml(task_file)
            pilot_parts.append('task:[' + ','.join(['{lat:%f,lon:%f}' % (p[1], p[0]) for p in plist]) + ']')
            print 'task',

        if os.path.exists(task_poly_file):
            plist = get_points_from_kml(task_poly_file)
            pilot_parts.append('poly:[' + ','.join(['{lat:%f,lon:%f}' % (p[1], p[0]) for p in plist]) + ']')
            print 'poly',

        pilotlist.append('{' + ','.join(pilot_parts) + '}')
        print ']'

    pack_str += ', pilots:[' + ','.join(pilotlist) + ']}'

    with open(args.output_package, 'w') as p:
        p.write(pack_str)



pack_methods = {
    'json': pack_json
}
