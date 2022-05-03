from flask import Flask
from config import Config

app = Flask(__name__, static_url_path='/done/', static_folder='/done/')
app.config.from_object(Config)
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0") #host="0.0.0.0" will make the page accessable
                            #by going to http://[ip]:5000/ on any computer in 
                            #the network.
from module_app import routes
