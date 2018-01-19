# My project's README

#생성
(python manage.py dumpdata account_category > initial_data.json --setting=pickdata.settings.dev)

#loaddata
python manage.py loaddata init_data --settings=pickdata.settings.dev

#runserver
python manage.py runserver --settings=pickdata.settings.dev