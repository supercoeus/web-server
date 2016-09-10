FROM debian/7.8/base-server:latest

ADD ./misc/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

ADD ./code /home/taohao/running/web-server/code

ADD ./conf /home/taohao/conf

EXPOSE 9999

WORKDIR /home/taohao/running/web-server/

ENV PYTHONPATH /home/taohao/conf

CMD ["python", "-m", "code"]

