
all: misaki_gothic.bdf k6x8.bdf

clean:
	rm misaki_bdf_2019-06-03a.zip k6x8bb02.tar.gz

misaki_gothic.bdf: misaki_bdf_2019-06-03a.zip
	# required `unzip` command
	# $ sudo apt-get install unzip  # Ubuntu
	# $ sudo yum install unzip  # CentOS
	unzip misaki_bdf_2019-06-03a.zip misaki_gothic.bdf

misaki_bdf_2019-06-03a.zip:
	curl -O https://littlelimit.net/arc/misaki/misaki_bdf_2019-06-03a.zip

k6x8.bdf: k6x8bb02.tar.gz
	tar zxvf k6x8bb02.tar.gz k6x8.bdf

k6x8bb02.tar.gz:
	curl -O https://littlelimit.net/arc/k6x8/k6x8bb02.tar.gz
