ifeq ($(ENROLL_DOMAIN),)
  $(error ENROLL_DOMAIN is not set)
endif

ifeq ($(ENROLL_EMAIL),)
  $(error ENROLL_EMAIL is not set)
endif

RANDOM_STRING := $(shell openssl rand -hex 24)

update:
	git checkout master
	git pull
	docker-compose -f production.yml build
	docker-compose -f production.yml up -d
	@echo "waiting 10sec for postgresql to boot up"
	sleep 10
	docker-compose -f production.yml exec django python manage.py migrate
	docker-compose -f production.yml exec django python manage.py collectstatic --noinput --clear

setup:
	rm -rf .envs/.production/ || true

	cp -av .envs/.production_example/ .envs/.production/
	sed -i "s/__DOMAIN__/${ENROLL_DOMAIN}/g" '.envs/.production/.django'
	sed -i "s/__DJANGO_SECRET_KEY__/${RANDOM_STRING}/g" '.envs/.production/.django'
	sed -i "s/__EMAIL__/${ENROLL_EMAIL}/g" '.envs/.production/.django'

	docker-compose -f production.yml build
	docker-compose -f production.yml up -d
	@echo "waiting 10sec for postgresql to boot up"
	sleep 10
	docker-compose -f production.yml exec django python manage.py migrate
	docker-compose -f production.yml exec django python manage.py collectstatic  --noinput --clear
	docker-compose -f production.yml exec django python manage.py createsuperuser --email ${ENROLL_EMAIL} --username admin

destroy:
	docker-compose -f production.yml down -v

stop:
	docker-compose -f production.yml stop

restart:
	docker-compose -f production.yml stop
	docker-compose -f production.yml up -d

start:
	docker-compose -f production.yml up -d
	@echo "waiting 10sec for postgresql to boot up"
	sleep 10
	docker-compose -f production.yml exec django python manage.py migrate
	docker-compose -f production.yml exec django python manage.py collectstatic --noinput --clear

extract_translations: ## extract strings to be translated, outputting .po files
	# Extract Python and Django template strings
	mkdir -p locale/en/LC_MESSAGES/
	rm -f locale/en/LC_MESSAGES/{django,text}.po
	python manage.py makemessages -l en -v1 -d django
