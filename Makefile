docker:
	docker-compose $(filter-out $@,$(MAKECMDGOALS))

build:
	docker-compose build --parallel --build-arg $(filter-out $@,$(MAKECMDGOALS))

start:
	docker-compose up -d --build $(filter-out $@,$(MAKECMDGOALS))

logs:
	docker-compose logs -f $(filter-out $@,$(MAKECMDGOALS))

stop:
	docker-compose stop $(filter-out $@,$(MAKECMDGOALS))

clean:
	echo "Removing: containers images networks volumes..."
	docker-compose down --rmi all --volumes

define _run_web_api # Launch commands will be inside this container
	docker-compose exec -T web_api $(1)
endef

define _run_serverless_functions # Launch commands will be inside this container
	docker-compose exec -T serverless $(1)
endef

check_sort:
	$(call _run_web_api, isort . -c)

sort:
	$(call _run_web_api, isort .)

flake8:
	$(call _run_web_api, flake8)

check_black:
	$(call _run_web_api, black . --check)

black:
	$(call _run_web_api, black .)


lint_web_api:
	make flake8
	make check_sort
	make check_black

enforce_lint_web_api:
	make sort
	make black
	make flake8

lint_serverless_functions:
	$(call _run_serverless_functions, flake8)
	$(call _run_serverless_functions, isort . -c)
	$(call _run_serverless_functions, black . --check --exclude=".serverless|unzip_requirements.py|layers")

enforce_lint_serverless_functions:
	$(call _run_serverless_functions, isort .)
	$(call _run_serverless_functions, black . --exclude=".serverless|unzip_requirements.py|layers")
	$(call _run_serverless_functions, flake8)

invoke_sample:
	docker-compose exec serverless npx sls invoke local --stage=local -f sample

%: #Ignores unknown commands (and extra params)
	@:
