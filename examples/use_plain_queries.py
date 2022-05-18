from sqlalchemy.orm import Session

session: Session


result = session.execute("SELECT * FROM products")
result.fetchall()  # take all rows as "row proxy"
result.first()  # takes first row

# what one can do with row proxy?
row = result.first()

# (all three methods works for field access)
row.title  # attribute access (if a column named "title" exists)
row[0]  # index access (if a column named "title" exists)
row['title']  # key access (if a column named "title" exists)
