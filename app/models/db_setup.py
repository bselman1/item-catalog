from . import Base, Category, CategoryItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists

class DbSetup():
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.db_engine = create_engine(connection_string)
        self.sessionmaker = sessionmaker(bind=self.db_engine)
    
    def create_session(self) -> sessionmaker:
        return self.sessionmaker()

    def initialize_database(self) -> None:
        '''
        Checks to see if the database is already created. If not, a new database
        is created and initalized with some default values.
        '''
        if database_exists(self.connection_string):
            return
        
        ## Create database and initialize with default values
        Base.metadata.create_all(self.db_engine)
        session = self.create_session()

        # Default categories
        football = Category(name = 'Football')
        football.category_items = [
            CategoryItem(name='Football', description='Throw the most excellent spirals.'),
            CategoryItem(name='Helmet', description='Protect that noggin with our best helmet yet.')
        ]
        session.add(football)

        soccer = Category(name = 'Soccer')
        soccer.category_items = [
            CategoryItem(name='Soccer ball', description='Use the same ball that was seen at the World Cup with this limited edition item.'),
            CategoryItem(name='Cleats', description='The best kicks bar none.')
        ]
        session.add(soccer)

        running = Category(name = 'Running')
        running.category_items = [
            CategoryItem(name='Lightning bolt shoes', description='Run faster than Usain Bolt with these special edition kicks.'),
            CategoryItem(name='Water bottle', description='Keeps your water cold for 24 hours!')
        ]
        session.add(running)

        session.commit()
        session.close()




