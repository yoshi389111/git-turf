FROM python:3

WORKDIR /app

COPY . /app

RUN pip3 install -e .

WORKDIR /workspace

RUN git config --global safe.directory '*'

ENTRYPOINT [ "git-turf" ]

CMD [ "-h" ]