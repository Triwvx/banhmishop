from flask_app import app

from flask_app.controllers.users_controllers import User
from flask_app.controllers.orders_controllers import Order

if __name__=="__main__":
    app.run(debug=True)