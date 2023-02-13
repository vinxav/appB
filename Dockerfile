FROM fedora:latest
RUN dnf update -y
RUN dnf install -y python python-pip
RUN pip install Flask
RUN pip install cryptography
RUN pip install requests

ADD appB.py /home/appB.py
WORKDIR /home
EXPOSE 5000
CMD flask --app appB.py run -h 0.0.0.0
