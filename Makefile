
first-install:
	pip3 install --user pipenv
	pip3 install --user --upgrade pipenv
	# A new install of pipenv will require restarting the shell.
	# Also verify ~/.local/bin is in your PATH
	PIPENV_VENV_IN_PROJECT=1 pipenv --python 3.8
	pipenv install

install:
	pipenv install --dev

activate:
	pipenv shell -c

test:
	pipenv run pytest

format:
	pipenv run python -m black .

update:
	sudo pip3 install --upgrade pipenv

build-dist:
	pipenv run python setup.py sdist bdist_wheel

