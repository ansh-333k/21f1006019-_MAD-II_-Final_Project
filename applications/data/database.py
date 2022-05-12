from main import db
#from sqlalchemy import create_engine

#engine = create_engine('sqlite:////home/ansh/flashcard/database/database.sqlite3', convert_unicode=True)
#db_session = db.scoped_session(db.sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = db.declarative_base()
Base.query = db.session.query_property()

#def init_db():
#    import applications.data.models
#    Base.metadata.create_all(bind=engine)