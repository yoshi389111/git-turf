
# install "git-turf"
install:
	pip3 install -e .

# uninstall "git-truf"
uninstall:
	pip3 uninstall git-turf

fonts: git_turf/font_data.py
	cd misc ; make ; python3 conv_fonts.py > ../git_turf/font_data.py

test:
	python3 -m mypy git_turf
	python3 setup.py test

# create virtual environment
venv:
	python3 -m venv .venv

# install for development(at venv)
dev-install:
	pip install -r requirements.txt
