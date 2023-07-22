import models
from fastapi import FastAPI, HTTPException
from typing import List
from starlette import status
from schemas import Note
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Маршрут "/notes/" с методом GET для получения всех заметок.
# Используется объект сессии session для выполнения запроса
# к базе данных и получения всех объектов models.NoteDB.
# Заметки возвращаются в формате списка.


@app.get("/notes/", response_model=List[Note])
def get_all_notes():
    session = SessionLocal()
    notes = session.query(models.NoteDB).all()
    return notes


# Маршрут "/notes/" с методом POST для создания новой заметки.
# Параметр note типа Note, который передается в запросе,
# используется для создания нового объекта models.NoteDB,
# который затем добавляется в базу данных с помощью session.add()
# и сохраняется с помощью session.commit().


@app.post("/notes/")
def create_note(note: Note):
    session = SessionLocal()
    db_note = models.NoteDB(id=note.id, title=note.title, content=note.content)
    session.add(db_note)
    session.commit()
    return {"message": "Note created successfully"}

# Маршрут "/notes/{id}" с методом GET для получения
# заметки по ее идентификатору. Значение идентификатора
# передается как параметр id. Используется метод session.query().get(),
# чтобы найти заметку по ее идентификатору. Если заметка не найдена,
# генерируется исключение HTTPException с кодом состояния 404.
# В противном случае, заметка возвращается.


@app.get("/notes/{id}", response_model=Note)
def get_note_by_id(id: int):
    session = SessionLocal()
    note = session.query(models.NoteDB).get(id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# Маршрут "/notes/{id}" с методом DELETE для удаления заметки по ее идентификатору.
# Значение идентификатора передается как параметр id. Используется метод session.query().get(),
# чтобы найти заметку по ее идентификатору. Если заметка не найдена,
# генерируется исключение HTTPException с кодом состояния 404. В противном случае,
# заметка удаляется из базы данных с помощью session.delete() и изменения сохраняются с помощью
# session.commit(). Возвращается сообщение об успешном удалении.

@app.delete("/notes/{id}")
def delete_note_by_id(id: int):
    session = SessionLocal()
    note = session.query(models.NoteDB).get(id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"message": "Note deleted successfully"}
