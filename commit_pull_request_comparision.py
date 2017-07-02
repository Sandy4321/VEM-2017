#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import json

def read_json_file(file_name):
	with open(file_name) as data_file:
		data = json.load(data_file)
	return data

def commits_employees(commits):
	authors = collections.OrderedDict()
	for commit in commits:
		if commit['author'] is not None and commit['author']['site_admin'] is True:
			if commit['author']['login'] not in authors:
				authors[commit['author']['login']] = 1
			else:
				authors[commit['author']['login']] += 1
	return authors

def pull_requests_employees(pull_requests):
	authors = collections.OrderedDict()

	for pull_request in pull_requests:
		if pull_request['user']['site_admin'] is True:
			if pull_request['user']['login'] not in authors:
				authors[pull_request['user']['login']] = 1
			else:
				authors[pull_request['user']['login']] += 1
	return authors

hubot_commits = read_json_file('hubot_commits.json')
atom_commits = read_json_file('atom_commits.json')
atom_pull_requests = read_json_file('atom_pulls.json')
hubot_pull_requests = read_json_file('hubot_pulls.json')
commits_employees = commits_employees(hubot_commits)
pull_requests_employees = pull_requests_employees(hubot_pull_requests)

for author in commits_employees:
	if author not in pull_requests_employees:
		print 'O funcionário ' + str(author) + ' fez ' + str(commits_employees[author]) + ' commit\'s' + ' e não criou pull-requests.'
	else:
		print 'O funcionário ' + str(author) + ' fez ' + str(commits_employees[author]) + ' commit\'s' + ' e criou ' +  str(pull_requests_employees[author]) + ' pull-requests.'
