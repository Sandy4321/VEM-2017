#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def read_json_file(file_name):
	with open(file_name) as data_file:
		data = json.load(data_file)
	return data

def pull_requests_monthly_frequency(pull_requests):
	monthly_frequency = collections.OrderedDict()

	for pull_request in pull_requests:
		date = datetime.strptime(pull_request['created_at'],'%Y-%m-%dT%H:%M:%SZ').date().replace(day = 15)

		if date not in monthly_frequency:
			monthly_frequency[date] = 1
		else:
			monthly_frequency[date] = monthly_frequency[date] + 1

	return monthly_frequency

def open_pull_requests(pull_requests, project_name):
	paid_contributors_pull_requests = []
	unpaid_contributors_pull_requests = []

	for pull_request in pull_requests:
		if 'open' in pull_request['state']:
			if pull_request['user']['site_admin'] is True:
				paid_contributors_pull_requests.append(pull_request)
			elif pull_request['user']['site_admin'] is False:
				unpaid_contributors_pull_requests.append(pull_request)

	monthly_frequency_unpaid = pull_requests_monthly_frequency(unpaid_contributors_pull_requests)
	monthly_frequency_paid = pull_requests_monthly_frequency(paid_contributors_pull_requests)

	# Creating the chart
	fig, ax = plt.subplots()
	years = mdates.YearLocator()
	ax.xaxis.set_minor_locator(years)
	unpaid_line = ax.plot(monthly_frequency_unpaid.keys(), monthly_frequency_unpaid.values(), 'o-', linewidth=2, 
		label=u'Voluntários')
	paid_line = ax.plot(monthly_frequency_paid.keys(), monthly_frequency_paid.values(), 'o-', linewidth=2, 
		label=u'Empregados')
	ax.legend()
	fig.autofmt_xdate()
	plt.xlabel(u'Anos')
	plt.ylabel(u'$\it{Pull-requests}$ abertos')
	plt.savefig(project_name + '_open.png', bbox_inches='tight')

def closed_pull_requests(pull_requests, project_name):
	paid_contributors_pull_requests = []
	unpaid_contributors_pull_requests = []

	for pull_request in pull_requests:
		if 'closed' in pull_request['state'] and pull_request['merged_at'] is None:
			if pull_request['user']['site_admin'] is True:
				paid_contributors_pull_requests.append(pull_request)
			elif pull_request['user']['site_admin'] is False:
				unpaid_contributors_pull_requests.append(pull_request)

	monthly_frequency_unpaid = pull_requests_monthly_frequency(unpaid_contributors_pull_requests)
	monthly_frequency_paid = pull_requests_monthly_frequency(paid_contributors_pull_requests)

	# Creating the chart
	fig, ax = plt.subplots()
	years = mdates.YearLocator()
	ax.xaxis.set_minor_locator(years)
	unpaid_line = ax.plot(monthly_frequency_unpaid.keys(), monthly_frequency_unpaid.values(), 'o-', linewidth=2, 
		label=u'Voluntários')
	paid_line = ax.plot(monthly_frequency_paid.keys(), monthly_frequency_paid.values(), 'o-', linewidth=2, 
		label=u'Empregados')
	ax.legend()
	fig.autofmt_xdate()
	plt.xlabel(u'Anos')
	plt.ylabel(u'$\it{Pull-requests}$ fechados')
	plt.savefig(project_name + '_closed.png', bbox_inches='tight')

def merged_pull_requests(pull_requests, project_name):
	paid_contributors_pull_requests = []
	unpaid_contributors_pull_requests = []

	for pull_request in pull_requests:
		if 'closed' in pull_request['state'] and pull_request['merged_at'] is not None:
			if pull_request['user']['site_admin'] is True:
				paid_contributors_pull_requests.append(pull_request)
			elif pull_request['user']['site_admin'] is False:
				unpaid_contributors_pull_requests.append(pull_request)

	monthly_frequency_unpaid = pull_requests_monthly_frequency(unpaid_contributors_pull_requests)
	monthly_frequency_paid = pull_requests_monthly_frequency(paid_contributors_pull_requests)

	# Creating the chart
	fig, ax = plt.subplots()
	years = mdates.YearLocator()
	ax.xaxis.set_minor_locator(years)
	unpaid_line = ax.plot(monthly_frequency_unpaid.keys(), monthly_frequency_unpaid.values(), 'o-', linewidth=2, 
		label=u'Voluntários')
	paid_line = ax.plot(monthly_frequency_paid.keys(), monthly_frequency_paid.values(), 'o-', linewidth=2, 
		label=u'Empregados')
	ax.legend()
	fig.autofmt_xdate()
	plt.xlabel(u'Anos')
	plt.ylabel(u'$\it{Pull-requests}$ aceitos')
	plt.savefig(project_name + '_merged.png', bbox_inches='tight')

if __name__ == "__main__":
	# Atom: https://github.com/atom/atom
	atom_commits = read_json_file('atom_commits.json')
	atom_pull_requests = read_json_file('atom_pulls.json')
	atom_contributors = read_json_file('atom_contributors.json')

	# Hubot: https://github.com/github/hubot
	hubot_commits = read_json_file('hubot_commits.json')
	hubot_pull_requests = read_json_file('hubot_pulls.json')
	hubot_contributors = read_json_file('hubot_contributors.json')

	open_pull_requests(atom_pull_requests, 'atom')
	open_pull_requests(hubot_pull_requests, 'hubot')
	closed_pull_requests(atom_pull_requests, 'atom')
	closed_pull_requests(hubot_pull_requests, 'hubot')
	merged_pull_requests(atom_pull_requests, 'atom')
	merged_pull_requests(hubot_pull_requests, 'hubot')