FROM python

RUN pip install torch==2.0.0+cpu torchvision==0.15.0+cpu -f https://download.pytorch.org/whl/torch_stable.html -i https://pypi.douban.com/simple/ some-package

WORKDIR /workspace

COPY cat.jpg /workspace
COPY function.py /workspace
COPY imagenet_classes.txt /workspace

RUN wget -O resnet.pth https://download.pytorch.org/models/resnet50-19c8e357.pth

CMD python3 function.py
