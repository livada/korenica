#! /usr/bin/python
"""Usage:

python korenica.py [option] input.igc [output.kml] | [task_cylinders.kml]

options:
    --verbose (default)  - Verbose track info output
    --csv                - Only CSV output
    --csv-header         - Print header for CSV output
    --task-cylinders     - Output task cylinders to kml file
    -h --help            - Print this help 

"""

if __name__ == '__main__':
    from igcutils import IGCReader
    from campus import CampusTask
    
    import sys
    
    if len(sys.argv)<2:
        print 'Invalid option.\n'
        print __doc__
        sys.exit()
    
    task = CampusTask([ (44.704578, 15.819669,  2.0), # startni cilindar 
                        (44.871002, 15.632666, 20.0), # 1. cilindar Plitvice
                        (44.604398, 15.417794, 28.0), # 2. cilindar Licki Osik - kolodvor
                        (44.554233, 15.957067, 20.0), # 3. cilindar Donji Lapac
                        (44.697325, 15.781533, 0.4)]) # cilj u kampu
    
    if sys.argv[1] in ('-h', '--help'): 
        print __doc__
        
    elif sys.argv[1] == '--task-cylinders':
        kmlfilename = sys.argv[2] if len(sys.argv)>2 else 'task_cylinders.kml'
        task.export_kml(kmlfilename)
        
    elif sys.argv[1] == '--csv-header':
        print "'filename', 'distance', 'speed', 'penalty time', 'time penalty distance', 'in goal', 'penalty distance', 'task points', 'area coef.', 'area bonus', 'total score';"
        sys.exit()
        
    elif sys.argv[1] in ('--csv', '--verbose') or sys.argv[1].endswith('.igc'):
        
        if sys.argv[1] in ('--csv', '--verbose'):
            if len(sys.argv)<3:
                print 'Must specify input igc file.\n'
                print __doc__
                sys.exit()
            infile_igc = sys.argv[2]
            kmlfilename = sys.argv[3] if len(sys.argv)>3 else None
        else:
            infile_igc = sys.argv[1]
            kmlfilename = sys.argv[2] if len(sys.argv)>2 else None


        verbose = not sys.argv[1]=='--csv'
        
        if verbose:
            print '#'*44
            print '# Processing: %s' % infile_igc
    
        igc = IGCReader(infile_igc)

        if verbose:
            print 'Track Points:', len(igc.track)
        
        track = task.process(igc)
    
        if verbose:
            print '\nCourse coordinates:'
            print '\n'.join(map(lambda x: '%.5f %.5f' % x, track.waypoints))
            print
            print 'Total distance: %.2f km (avg.speed %.2f km/h)' % (track.total_distance, track.avg_speed*3600)
            print 'In goal:', track.in_goal
            print 'Goal penalty: %.2f km' % track.goal_penalty
            print 'Time penalty: %.2f km (for %.1f seconds)' % (track.time_penalty, track.penalty_seconds)
            print 'Task score: %.1f' % track.score
            print 'Area bonus: %.1f points (%.2f%%)' % (track.score*track.poly_coef, track.poly_coef*100.)
            print 'Total score: %.1f' % track.score * (1.0 + track.poly_coef)
        else:
            print "'%s'," % infile_igc, track
    
        if kmlfilename:
            track.export_kml(kmlfilename)
            track.export_poly_kml(kmlfilename[:-4]+'_poly.kml')
    else:
        print 'Invalid arguments.\n'
        print __doc__
        sys.exit()
    
