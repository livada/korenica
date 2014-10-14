/*
 * CampusTask.cpp
 *
 *  Created on: Feb 18, 2012
 *      Author: bokun
 */

#include "CampusTask.h"
#include <assert.h>


CampusTask::CampusTask() {
	this->distance_cache = new double[(MAX_TRACK_PTS * (MAX_TRACK_PTS+1)/2)];
	for (unsigned long i=0; i<(MAX_TRACK_PTS * (MAX_TRACK_PTS+1)/2); i++)
		this->distance_cache[i] = 0.0;
}

CampusTask::~CampusTask() {
	delete[] this->distance_cache;
}

void CampusTask::flush_task() {
	this->cylinder_lat.clear();
	this->cylinder_lon.clear();
	this->cylinder_radius.clear();

	this->goal_lat = 0.0;
	this->goal_lon = 0.0;
	this->goal_radius = 0.0;

	this->points_in_cylinder.clear();
	this->dist_from_goal.clear();
	this->min_dist_from_goal.clear();
	this->min_dist_from_goal_index.clear();

	this->wpt_lat.clear();
	this->wpt_lon.clear();

	this->waypoint_indices.clear();
	this->test_indices.clear();
	this->waypoint_dist = 0.0;

//	std::cout << "Task cleared." << std::endl;
}

void CampusTask::flush_track() {
	this->track_lat.clear();
	this->track_lon.clear();

	for (unsigned long i=0; i<MAX_TRACK_PTS * (MAX_TRACK_PTS-1)/2; i++)
		this->distance_cache[i] = 0.0;

	this->points_in_cylinder.clear();
	this->dist_from_goal.clear();
	this->min_dist_from_goal.clear();
	this->min_dist_from_goal_index.clear();

	this->wpt_lat.clear();
	this->wpt_lon.clear();

	this->waypoint_indices.clear();
	this->test_indices.clear();
	this->waypoint_dist = 0.0;

//	std::cout << "Track cleared." << std::endl;
}

void CampusTask::push_task_cylinder(double lat, double lon, double radius) {
	this->cylinder_lat.push_back(lat);
	this->cylinder_lon.push_back(lon);
	this->cylinder_radius.push_back(radius);
}
void CampusTask::push_track_point(double lat, double lon) {
	this->track_lat.push_back(lat);
	this->track_lon.push_back(lon);
}

void CampusTask::waypoint_recursion(unsigned long index, unsigned long cylinder){
	// Try without this cylinder first.
	if (cylinder+1<this->cylinder_lat.size())
		this->waypoint_recursion(index, cylinder+1);
	// With this cylinder...
	this->test_indices.push_back(index);
	for(unsigned long i=0; i<this->points_in_cylinder[cylinder].size(); i++){
		// Skip points already consumed.
		if (this->points_in_cylinder[cylinder][i]<index)
			continue;
		// Try with this point in this cylinder.
		this->test_indices.back() = this->points_in_cylinder[cylinder][i];
		// Recurse in the rest of the cylinders.
		if (cylinder+1<this->cylinder_lat.size())
			this->waypoint_recursion(this->test_indices[cylinder]+1, cylinder+1);
		// Test for current task distance.
		double test_d = this->task_distance(this->test_indices);
		if (test_d > this->waypoint_dist) {
			this->waypoint_indices = this->test_indices;
			this->waypoint_dist = test_d;
		}
	}
	this->test_indices.pop_back();
}

void CampusTask::do_calculation() {
//	std::cout << "Grab last cylinder as goal." << std::endl;

	this->goal_lat = this->cylinder_lat.back();
	this->goal_lon = this->cylinder_lon.back();
	this->goal_radius = this->cylinder_radius.back();

	this->cylinder_lat.pop_back();
	this->cylinder_lon.pop_back();
	this->cylinder_radius.pop_back();

//	std::cout << "Precalculation..." << std::endl;
	double d;
	for (unsigned int cyl=0; cyl<this->cylinder_lat.size(); cyl++){
		this->points_in_cylinder.push_back(vector<unsigned long>());
		for (unsigned long i=0; i<this->track_lat.size(); i++){
			d = this->calc_inverse(
					this->cylinder_lat[cyl], this->cylinder_lon[cyl],
					this->track_lat[i], this->track_lon[i]);
			if (d<this->cylinder_radius[cyl])
				this->points_in_cylinder[cyl].push_back(i);
		}
	}

	// Calculate complexity.
	double complexity = 1.0;
	for (unsigned int cyl=0; cyl<this->points_in_cylinder.size(); cyl++)
		if (this->points_in_cylinder[cyl].size())
			complexity *= this->points_in_cylinder[cyl].size();
//	std::cout << std::endl;
//	std::cout << "Complexity: " << complexity / 1e+9 << " G" << std::endl;
//	std::cout << "Cache size: " << (this->track_lat.size() * (this->track_lat.size()+1)/2) / 1e+6 << " M" << std::endl;

	// Precalculate distance to goal for each track point.
	for (unsigned long i=0; i<this->track_lat.size(); i++){
		d = this->calc_inverse(
				this->goal_lat, this->goal_lon,
				this->track_lat[i], this->track_lon[i]);
		if (d<this->goal_radius) d = 0.0;
		this->dist_from_goal.push_back(d);
		this->min_dist_from_goal.push_back(d);
		this->min_dist_from_goal_index.push_back(0);
	}

	// Precalculate index of the point closest to goal from this point on.
	unsigned long d_index = this->min_dist_from_goal.size()-1;
	d = this->min_dist_from_goal[d_index];
	for(long i=d_index; i>=0; i--) {
		if (this->min_dist_from_goal[i]<d) {
			d = this->min_dist_from_goal[i];
			d_index = i;
		}
		this->min_dist_from_goal[i] = d;
		this->min_dist_from_goal_index[i] = d_index;
	}

//	std::cout << "Starting calculation..." << std::endl;
	this->waypoint_dist = 0.0;
	this->waypoint_recursion(0, 0);

//	std::cout << "Done calculation." << std::endl;
}

long CampusTask::number_of_wpts() {
	return this->waypoint_indices.size() + 1;
}

const char* CampusTask::get_waypoints() {
	stringstream ss;

	for (unsigned long i=0; i<this->waypoint_indices.size(); i++) {
		ss << this->waypoint_indices[i];
		ss << "|";
	}
	ss << this->min_dist_from_goal_index[this->waypoint_indices.back()];
	string s(ss.str());
	return s.c_str();
}

const char* CampusTask::get_leg_distances() {
	stringstream ss;

	if (this->waypoint_indices.size()<2) return "0";

	for (unsigned long i=0; i<this->waypoint_indices.size()-1; i++) {
		ss << this->cached_distance(this->waypoint_indices[i], this->waypoint_indices[i+1]);
		ss << "|";
	}
	ss << this->dist_from_goal[this->waypoint_indices.back()];

	string s(ss.str());
	return s.c_str();
}

const char* CampusTask::get_poly_leg_distances() {
	stringstream ss;

	if (this->waypoint_indices.size()<4) return "0";

	for (unsigned long i=1; i<this->waypoint_indices.size()-1; i++) {
		ss << this->cached_distance(this->waypoint_indices[i], this->waypoint_indices[i+1]);
		ss << "|";
	}
	ss << this->cached_distance(this->waypoint_indices.back(), this->waypoint_indices[1]);

	string s(ss.str());
	return s.c_str();
}

const char* CampusTask::make_cylinder(double lat, double lon, double radius) {
	stringstream ss;
	Math::real azi, lat2, lon2, azi2, m12;

	for (azi=0.0; azi<=360.0; azi += 3.0) {
		Geodesic::WGS84.Direct(lat, lon, azi, radius*1000.0, lat2, lon2, azi2, m12);
		ss << lat2 << "," << lon2;
		ss << "|";
	}
	string s(ss.str());
	return s.c_str();
}


double CampusTask::calc_inverse(double lat1, double lon1, double lat2, double lon2){
	Math::real s12, azi1, azi2, m12;
	Geodesic::WGS84.Inverse(lat1, lon1, lat2, lon2, s12, azi1, azi2, m12);
	return s12/1000.0;
}

double CampusTask::cached_distance(unsigned long i1, unsigned long i2){
	if (i1==i2) return 0.0;
	if (i1>i2) swap(i1,i2);

	long Z = XY(i1,i2);

	assert(Z<(MAX_TRACK_PTS * (MAX_TRACK_PTS+1)/2));

	if (this->distance_cache[Z] == 0.0) {
		double d;
		d = this->calc_inverse(
				this->track_lat[i1], this->track_lon[i1],
				this->track_lat[i2], this->track_lon[i2]);
		this->distance_cache[Z] = d;
	}
	return this->distance_cache[Z];
}

double CampusTask::task_distance(vector<unsigned long> task){
	double task_dist = 0.0;

	if (task.size() == 0) 
		return 0.0;

	if (task.size() > 1) {
		for(unsigned long i=0; i<task.size()-1; i++)
			task_dist += this->cached_distance(task[i], task[i+1]);
	}

	unsigned long last_index = task.back();

	double dist_to_goal = this->dist_from_goal[last_index];

	return task_dist + dist_to_goal - this->min_dist_from_goal[last_index];
}

double CampusTask::get_total_distance() {
	return this->waypoint_dist;
}

double CampusTask::get_goal_penalty(){
	return this->min_dist_from_goal[this->waypoint_indices.back()];
}

unsigned long CampusTask::get_last_index(){
	return this->min_dist_from_goal_index[this->waypoint_indices.back()];
}

bool CampusTask::in_goal() {
	return this->min_dist_from_goal[this->waypoint_indices.back()]==0.0;
}
