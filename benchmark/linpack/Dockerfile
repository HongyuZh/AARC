FROM python
COPY function.py function.py
RUN pip3 install -i http://mirrors.cloud.aliyuncs.com/pypi/simple/ --trusted-host mirrors.cloud.aliyuncs.com --default-timeout=60 --no-cache-dir numpy
CMD python3 function.py 