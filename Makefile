.PHONY: fetch_recommendations silent_fetch_recommendations# setup

setup:
	python -c 'import sys;import os;sys.path.append(os.path.abspath("."))'

fetch_recommendations:
	# make setup
	python scripts/fetch_recommendations.py

silent_fetch_recommendations:
	make setup	
	python scripts/fetch_recommendations.py --silent