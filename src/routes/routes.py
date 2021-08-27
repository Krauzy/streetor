from src.static.single import Single
from src.pages.home import render_home
from src.pages.database import render_database

def route():
    if Single.get_instance().route == 'Home':
        render_home()
    else:
        render_database()