from fastapi import FastAPI , status
from database import Base, engine , Book
from schema import BookRequest
from sqlalchemy.orm import Session
from fastapi import HTTPException



# Create the database
Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/")
def root():
    return "Book"

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(book: BookRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the book database model
    bookobj = Book(title = book.title , description = book.description )


    # add it to the session and commit it
    session.add(bookobj)
    session.commit()

    # grab the id given to the object from the database
    id = bookobj.id

    # close the session
    session.close()

    # return the id
    return f"created book item with id {id}"

@app.get("/todo/{id}")
def read_todo(id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the book item with the given id
    bookobj = session.query(Book).get(id)

    # close the session
    session.close()
    if not bookobj:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return bookobj

@app.put("/todo/{id}")
def update_todo(id: int , book: BookRequest):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    bookobj = session.query(Book).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if bookobj:
        bookobj.title = book.title
        bookobj.description = book.description
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not bookobj:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return bookobj

@app.delete("/todo/{id}")
def delete_todo(id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    bookobj = session.query(Book).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if bookobj:
        session.delete(bookobj)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None

@app.get("/todo")
def read_todo_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all todo items
    books_list = session.query(Book).all()

    # close the session
    session.close()

    return books_list