from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

load_dotenv()

app = Flask(__name__)

DB_USER  = os.getenv("DB_USER", "root")
DB_PASSWORD =  os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "books1_db")
SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')


app.config["SQLALCHEMY_DATABASE_URI"] = (
  f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Book(db.Model):
  __tablename__ = "books1"

  id = db.Column(db.Integer, primary_key = True)
  naslov = db.Column(db.String(200), nullable = False)
  autor = db.Column(db.String(200), nullable = False)
  godina_izdanja = db.Column(db.Integer, nullable = False)

  def to_dict(self):
    return {
      "id": self.id,
      "naslov": self.naslov,
      "autor": self.autor,
      "godina_izdanja": self.godina_izdanja
    }
  
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(EncryptedType(db.String, SECRET_KEY, AesEngine), nullable=False)
    year = db.Column(db.Integer, nullable=True)
  
    #def to_dict(self):
     #   return {'id': self.id, 'title': self.title, 'author': #self.author, 'year': self.year}
    def to_dict(self):
      return {
          "id": self.id,
          "username": self.username,
          "year": self.year
      }
    
class Biblioteka(db.Model):
  __tablename__ = "biblioteka"

  naziv = db.Column(db.String(200), primary_key = True)

class Biblioteka1(db.Model):
  __tablename__ = "biblioteka1"

  naziv = db.Column(db.String(200), primary_key = True)

  
@app.route("/")
def home_page():
  return "Nalazite se na pocetnoj stranici vase demo aplikacije radjene u flasku."
  
@app.route("/api/books1", methods=["GET"])
def get_books1():
  books = Book.query.all()
  return jsonify([book.to_dict() for book in books])

@app.route("/api/books1/<int:book_id>", methods=["GET"])
def get_specific_book(book_id):
  book =  Book.query.get(book_id)

  if not book:
    return "Nema trazene knjige u bazi!"
  
  return jsonify(book.to_dict())

@app.route("/api/books1", methods=["POST"])
def dodaj_knjigu():
  data = request.get_json()

  new_book = Book(
    naslov = data["naslov"],
    autor = data["autor"],
    godina_izdanja = data["godina_izdanja"]
  )

  db.session.add(new_book)
  db.session.commit()

  return "Kjniga dodata"

@app.route("/api/books1/<int:book_id>", methods = ["PUT"])
def izmijeni_knjigu(book_id):
  knjiga = Book.query.get(book_id)

  if not knjiga:
    return "Knjiga ne postoji u bazi"
  
  data = request.get_json()

  knjiga.naslov = data.get("naslov", knjiga.naslov)
  knjiga.autor = data.get("autor", knjiga.autor)
  knjiga.godina_izdanja = data.get("godina_izdanja", knjiga.godina_izdanja)

  db.session.commit()

  return f"Izmjene uspijesno zavrsene.Provjerite kjnigu sa id-jem {book_id}"

@app.route("/api/books1/<int:book_id>", methods = ["DELETE"])
def obrisi(book_id):
  knjiga = Book.query.get(book_id)

  if not knjiga:
    return "Ne postoji knjiga u bazi!"
  
  db.session.delete(knjiga)
  db.session.commit()

  return jsonify({"message": "Knjiga uklonjena uspijesno iz baze!"})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)