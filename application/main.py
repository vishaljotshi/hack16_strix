from application import app
from views.punch_notification import *

import views.trigger



app.debug = True

if __name__ == "__main__":
    app.run()