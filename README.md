# Reptile

> Download the [driver](https://chromedriver.chromium.org/downloads) according to your chrome version and os system, and put it in the reptile folder


```bash=
[environment]: python 3.9
[browser]: chrome

#clone repo
git clone https://github.com/murraykkkeed06/reptile.git

#move to folder
cd reptile

#build environment
conda create --name env 

#activate 
conda activate env

#install pip
conda install pip

#install requirement
pip install requirement.txt

#(optional)set permission
chmod 755 chromedirver

#execute
python main.py
```