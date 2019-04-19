FROM python:3

COPY example_dotfiles  /root

RUN echo 'ping localhost &' > /bootstrap.sh
RUN echo 'sleep infinity' >> /bootstrap.sh
RUN chmod +x /bootstrap.sh

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD /bootstrap.sh
