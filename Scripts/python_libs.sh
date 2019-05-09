#!/bin/bash

if [ "$EUID" -ne 0 ]; then 
    echo "Favor rodar como root"
    echo "sudo ./python_libs.sh"
    exit
fi


apt install python3-pip -y

pip3 install bs4
pip3 install pandas
pip3 install pysolr

