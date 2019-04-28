#!/bin/bash
sudo docker run --rm -it --name devtest -v `pwd`:/app:z dotties /bin/bash
