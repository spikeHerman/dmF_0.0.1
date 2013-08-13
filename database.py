from sqlalchemy import create_engine

from sqlalchemy.engine.url import URL

class DatabaseConnector():
    """ Database Connector.

    In the works.

    """
    def __init__(self, drivername="postgresql+pypostgresql", username="mitsos",
                 password="tatoum1983", host="localhost", 
                 port="5432",database="spikes"):
        """ Initialization method for DatabaseConnector.
        
        Not sure how I will finally implement this.

        """
        self.url = URL(drivername=drivername, username=username, password=password,
                  host=host, port=port, database=database)
        self.engine = create_engine(self.url)
