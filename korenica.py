"""Usage:

python korenica.py input.igc [output.kml] [task_cylinders.kml]

"""

if __name__ == '__main__':
    from igcutils import IGCReader
    from campus import CampusTask
    
    import sys
    
    if len(sys.argv)<2:
        print 'You must specify input IGC filename.\n'
        sys.exit()
    
    if sys.argv[1] in ('-h', '--help'): 
        print __doc__
        
    infile_igc = sys.argv[1]

    print '#'*44
    print '# Processing: %s' % infile_igc
    
    task = CampusTask([ (44.704578, 15.819669,  2.0), # startni cilindar 
                        (44.871002, 15.632666, 20.0), # 1. cilindar Plitvice
                        (44.604398, 15.417794, 28.0), # 2. cilindar Licki Osik - kolodvor
                        (44.554233, 15.957067, 20.0), # 3. cilindar Donji Lapac
                        (44.697325, 15.781533, 0.4)]) # cilj u kampu
    
    if len(sys.argv)>3:
        task.export_kml(sys.argv[3])
    
    igc = IGCReader(infile_igc)
    print 'Track Points:', len(igc.track)
    track = task.process(igc)
    
    print '\nCourse coordinates:'
    print '\n'.join(map(lambda x: '%.5f %.5f' % x, track.waypoints))
    print
    print 'Total distance: %.2f km (avg.speed %.2f km/h)' % (track.total_distance, track.avg_speed*3600)
    print 'In goal:', track.in_goal
    print 'Goal penalty: %.2f km' % track.goal_penalty
    print 'Time penalty: %.2f km (for %.1f seconds)' % (track.time_penalty, track.penalty_seconds)
    print 'Total score: %.1f' % track.score
    
    if len(sys.argv)>2:
        track.export_kml(sys.argv[2])
    
    
