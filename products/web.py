from main import DB_URI
from products.api.app import create_app

app = create_app(database_uri=DB_URI)
