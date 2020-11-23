PIP=/usr/bin/pip3 

RED='\x1B[0;31m'
NC='\x1B[0m'


# Installation of Quartz is harder
#
# See explanation at https://stackoverflow.com/questions/42530309/no-such-file-requirements-txt-error-while-installing-quartz-module
#
echo "${RED}### SETUP Quartz${NC}"
rm -f quartz-0.0.1.dev0.tar.gz
echo "${RED}### Download Quartz${NC}"
$PIP download --no-deps --no-build-isolation quartz
echo "${RED}### Unzip Quartz${NC}"
gunzip quartz-0.0.1.dev0.tar.gz
tar xvf quartz-0.0.1.dev0.tar
sed "s/requirements.txt/quartz.egg-info\/requires.txt/" < quartz-0.0.1.dev0/setup.py > quartz-0.0.1.dev0/setup2.py
mv quartz-0.0.1.dev0/setup2.py quartz-0.0.1.dev0/setup.py
echo "${RED}### Install Quartz${NC}"
sudo $PIP install -e quartz-0.0.1.dev0
rm -rf quartz-0.0.1.dev0*

rm -rf .eggs
