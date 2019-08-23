
install:
	pip3 install -e .

uninstall:
	pip3 uninstall git-turf

fonts: git_turf/font_data.py
	cd misc ; make ; python3 conv_fonts.py > ../git_turf/font_data.py

test:
	python3 setup.py test

checkstyle:
	flake8
	isort -df
	mypy .

formatting:
	isort -y
	black .
