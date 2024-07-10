from flask import Flask
from flask_migrate import Migrate



from cakes import cake_bp
from drinks import drink_bp
from ice_cream import ice_cream_bp

app=Flask(__name__)





app.register_blueprint(drink_bp)
app.register_blueprint(cake_bp)
app.register_blueprint(ice_cream_bp)



if __name__=="__main__":
    app.run(port=8080,debug=True)


