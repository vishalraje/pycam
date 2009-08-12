#!/bin/bash
#
# run-cvEyeTracker
# 
# DESCRITPION, 
# 	Run cvEyetracker taking a full log, and filtering the programs
# 	output so that the screen only displays unusual events.
#
# AUTHOR
#   Rob Ramsay, 18:44  1 Sep 2008

e2s sudo ./cvEyeTracker \
| tee ./logs/cvEyeTracker-$(rtime -o).log  \
|  perl -e '
	while (<STDIN>) {
		unless (	/Time elapsed/ 
					or /\(corneal reflection\)/ 
					or /\(corneal\)/ 
					or /corneal reflection:/ 
					or /ellipse a:/ 
					or /^\s*$/ ) 
			{ print }
	}'

