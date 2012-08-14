/*
 * CampusTask.h
 *
 *  Created on: Feb 18, 2012
 *      Author: bokun
 */

#ifndef CAMPUSTASK_H_
#define CAMPUSTASK_H_

#define MAX_TRACK_PTS 8000
#define XY(x,y) (y*(y-1)+x) // x,y with x<y!!


#include <iostream>
#include <vector>
#include <sstream>

#include <GeographicLib/Geodesic.hpp>

using namespace GeographicLib;
using namespace std;

class CampusTask {
private:
	vector<double> track_lat;
	vector<double> track_lon;

	vector<double> cylinder_lat;
	vector<double> cylinder_lon;
	vector<double> cylinder_radius;

	double goal_lat;
	double goal_lon;
	double goal_radius;

	vector< vector<unsigned long> > points_in_cylinder;
	vector<double> dist_from_goal;
	vector<double> min_dist_from_goal;
	vector<unsigned long> min_dist_from_goal_index;

	vector<double> wpt_lat;
	vector<double> wpt_lon;

	vector<unsigned long> waypoint_indices, test_indices;
	double waypoint_dist;

	double *distance_cache;

	double task_distance(vector<unsigned long>);
	void waypoint_recursion(unsigned long index, unsigned long cylinder);

	double cached_distance(unsigned long i1, unsigned long i2);

	double calc_inverse(double lat1, double lon1, double lat2, double lon2);

public:
	CampusTask();
	virtual ~CampusTask();

    void flush_task();
    void flush_track();

    void push_task_cylinder(double lat, double lon, double radius);
    void push_track_point(double lat, double lon);

    void do_calculation();

    long number_of_wpts();
    const char* get_waypoints();
    const char* get_leg_distances();
    const char* get_poly_leg_distances();

    const char* make_cylinder(double lat, double lon, double radius);

    double get_total_distance();
    double get_goal_penalty();
    unsigned long get_last_index();
    bool in_goal();
};

extern "C" {
	CampusTask* CampusTask_new(){ return new CampusTask(); }

    void CampusTask_flush_task(CampusTask* task){ task->flush_task(); }
    void CampusTask_flush_track(CampusTask* task){ task->flush_track(); }

    void CampusTask_push_task_cylinder(CampusTask* task, double lat, double lon, double radius)
			{ task->push_task_cylinder(lat, lon, radius); }
    void CampusTask_push_track_point(CampusTask* task, double lat, double lon)
			{ task->push_track_point(lat, lon); }

    void CampusTask_do_calculation(CampusTask* task){ task->do_calculation(); }
    long CampusTask_number_of_wpts(CampusTask* task){ return task->number_of_wpts(); }
    const char* CampusTask_get_waypoints(CampusTask* task){ return task->get_waypoints(); }
    const char* CampusTask_get_leg_distances(CampusTask* task){ return task->get_leg_distances(); }
    const char* CampusTask_get_poly_leg_distances(CampusTask* task){ return task->get_poly_leg_distances(); }
    const char* CampusTask_make_cylinder(CampusTask* task, double lat, double lon, double radius)
    		{ return task->make_cylinder(lat, lon, radius); }
    double CampusTask_get_total_distance(CampusTask* task){ return task->get_total_distance(); }
    double CampusTask_get_goal_penalty(CampusTask* task){ return task->get_goal_penalty(); }
    unsigned long CampusTask_get_last_index(CampusTask* task){ return task->get_last_index(); }
    bool CampusTask_in_goal(CampusTask* task){ return task->in_goal(); }
}

#endif /* CAMPUSTASK_H_ */
