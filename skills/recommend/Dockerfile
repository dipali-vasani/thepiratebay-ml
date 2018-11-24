FROM continuumio/anaconda3:5.2.0

ADD src/requirements.txt /requirements.txt



RUN apt-get install -y libatlas3-base
RUN pip install -r requirements.txt

ADD src/__main__.py /__main__.py
ADD src/data.csv /data.csv


WORKDIR /

CMD ["python","__main__.py"]