Installation env:
python -m venv env
.\env\Scripts\activate
deactivate

Fonctionnement Heroku:
heroku login
heroku git:remote -a avacrypto ou heroku git:clone -a avacrypto
heroku plugins:install heroku-builds
heroku builds:cancel
heroku restart
git add .
git commit -am "YOUR COMMIT"
git push --force heroku main