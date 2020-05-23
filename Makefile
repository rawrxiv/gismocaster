init:
	pip3 install -r requirements.txt
	python3 web/manage.py migrate	
	python3 web/manage.py loaddata dpstype
	python3 web/manage.py createsuperuser --username admin --password admin --email admin@admin.com

install:
	sudo sed  's|{path}|'${PWD}'|' ./etc/mqttdevices.service > /etc/systemd/system/mqttdevices.service
	sudo cp ./etc/mqttdevices.conf /etc/mqttdevices.conf
	sudo systemctl enable mqttdevices.service
	sudo systemctl start mqttdevices.service

docker:	
	docker build -t mqttdevices .