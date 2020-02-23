from python:3.8.1

ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8

RUN mkdir /src
WORKDIR /src
COPY . /src/

RUN pip install -r requirements.txt
RUN ["python", "gui/generate_gui.py"]
ENTRYPOINT ["python", "run_gui.py"]