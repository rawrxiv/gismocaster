init:
	pip3 install -r requirements.txt
	python3 web/manage.py migrate	
	python3 web/manage.py loaddata component topic template topicvalue componentvalue setting
	python3 web/manage.py createsuperuser --username admin --password admin --email admin@admin.com

install:
	sudo sed  's|{path}|'${PWD}'|' ./etc/gismocaster.service > /etc/systemd/system/gismocaster.service
	# sudo cp ./etc/gismocaster.conf /etc/gismocaster.conf
	sudo systemctl enable gismocaster.service
	sudo systemctl start gismocaster.service

docker:	
	docker build -t gismocaster .

