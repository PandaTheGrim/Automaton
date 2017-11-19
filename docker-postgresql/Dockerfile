FROM library/centos:7

MAINTAINER automaton-team

RUN yum install -y curl git postgresql-dev python3 python3-devel python3-pip

RUN git clone https://github.com/Automaton-team/Automaton.git

WORKDIR /Automaton

RUN pip3 install -r ./requirements/base.txt

RUN python3 manage.py db migrate

EXPOSE 5000

ENTRYPOINT python3 manage.py runserver
