help:	## Help to run
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

up:
	docker-compose up -d

down:
	docker-compose down