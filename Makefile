setup: create-env init

create-env:
	python3 -m venv env

install:
	./env/bin/python3 -m pip install $(package)

lock:
	./env/bin/pip3 freeze > requirements.txt

list:
	./env/bin/pip3 list

init:
	./env/bin/pip3 install -r requirements.txt

notebook:
	jupyter nbconvert --execute --to html --template basic --output-dir=./output compare.ipynb

build:
	./env/bin/jupyter-book build ./public

create-book:
	./env/bin/jupyter-book create $(name)/

