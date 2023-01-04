# WebApp1

Simple Implementation of the tutorial available [here](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3#step-3-using-html-templates). There was no attempt to make the website good looking, functional or secure. Where possibile instead I tried to keep code easy and well commented. This should go without saying but do not use this repo for any reason beyond purely educational ones.

### How to deploy
This repo is setted for local testing. Launching `python3 app.py` makes the website available on localhost. To deploy on an external host, modify in `settings.py` the entries of `debug` (set it to `False`) and path if needed (so the website does not actually have to be hosted on the root `https://www.mywebsite.com` but even in sub-paths `https://www.mywebsite.com/test/` by setting `path=/test/`).