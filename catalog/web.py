from main import DB_URI

from catalog.api import create_app

app = create_app(database_uri=DB_URI)
