#
# Unreal Game Sync Server(Python Version) Docker file
#
FROM python:3.9

# Install python modules
RUN python -m pip install --upgrade pip
RUN pip install flask dbutils cryptography pymysql gevent

# Workdir
WORKDIR /data

# Copy api files
COPY api /data/api/
COPY sh /data/sh/

# Add execute attribute
RUN chmod +x /data/sh/*.sh

# Entry Point
ENTRYPOINT ["/bin/bash", "/data/sh/start.sh"]
