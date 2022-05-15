from likes.api import create_app
from main import DB_URI

app = create_app(database_uri=DB_URI)
