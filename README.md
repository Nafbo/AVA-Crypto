# AVA-Crypto
<p>AVA-Crypto is a crypto dashboard, which allows you to view the balance and other features of your crypto wallet.</p>
<p>Thanks to the covalent and coingecko api, we give you the possibility to have the balance of your crypto wallets, but also the history of it, the transactions linked to your wallet, the global balance of all your wallets entered in the application and finally the current price of a selection of crypto currency.</p>
<p>To visualise all this we have developed a dash application, which is deployable locally, or globally using heroku.</p>
<p>Finally we have linked a database to our application, so that your information remains when you log into your account.</p>

## Locally deployable (with Dash)
<p>Install the <code>requirements.txt</code> to have all the necessary libraries to launch our application</p>
<pre><code>pip install -r requirements.txt</code></pre>
<p>Know launch the <code>main.py</code> file to run the dash application locally on your web browser</p>

## Cloud deployable (with Heroku)
<p>Before deploying our application on the cloud with heroku you need to create an account on:</p>
<p><code>https://dashboard.heroku.com/apps</code></p>
<p>Then you can link your terminal to Heroku with</p>
<pre><code>heroku login</code></pre>
<p>Clone the repository github heroku</p>
<pre><code>heroku git:clone -a avacrypto</code>
<code>cd avacrypto</code></pre>
<p>After that you have to build the project, and restart it</p>
<pre><code>heroku plugins:install heroku-builds</code>
<code>heroku builds:cancel</code>
<code>heroku restart</code></pre>
<p>To finish deploy the application in heroku</p>
<pre><code>git add .</code>
<code>git commit -am "YOUR COMMIT"</code>
<code>git push --force heroku main</code></pre>
