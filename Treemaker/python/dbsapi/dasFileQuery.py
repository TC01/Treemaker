# A fork of https://github.com/cms-sw/cmssw/blob/CMSSW_7_6_X/HLTrigger/Configuration/python/Tools/dasFileQuery.py,
# which can query DAS and return a list of files.

import sys
import json
import das_client_fork as das_client

def dasFileQuery(dataset, instance='prod/master'):
	query   = 'dataset dataset=%s instance=%s' % (dataset, instance)
	host    = 'https://cmsweb.cern.ch'      # default
	idx     = 0                             # default
	limit   = 0                             # unlimited
	debug   = 0                             # default
	thr     = 300                           # default
	ckey    = ""                            # default
	cert    = ""                            # default
	jsondict = das_client.get_data(host, query, idx, limit, debug, thr, ckey, cert)

	# check if the pattern matches none, many, or one dataset
	if not jsondict['data'] or not jsondict['data'][0]['dataset']:
		sys.stderr.write('Error: the pattern "%s" does not match any dataset\n' % dataset)
		sys.exit(1)
		return []
	elif len(jsondict['data']) > 1:
		sys.stderr.write('Error: the pattern "%s" matches multiple datasets\n' % dataset)
		for d in jsondict['data']:
			sys.stderr.write('    %s\n' % d['dataset'][0]['name'])
		sys.exit(1)
		return []
	else:
		# expand the dataset name
		dataset = jsondict['data'][0]['dataset'][0]['name']
		query = 'file dataset=%s' % dataset
		jsondict = das_client.get_data(host, query, idx, limit, debug, thr, ckey, cert)
		# parse the results in JSON format, and extract the list of files
		files = sorted( f['file'][0]['name'] for f in jsondict['data'] )
		return files
