help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

up:
	docker-compose up -d

down:
	docker-compose down

python-path: 
	export PYTHONPATH=$PYTHONPATH:$$(pwd)

run:
	python3 src/app.py

consumer:
	python3 events/consumer.py