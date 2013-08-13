from datetime import datetime, date

from sqlalchemy import Table
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, Date, DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
# association tables for many to many relationships
principal_application_table = Table('pri_app', Base.metadata,
                Column('principal', Integer, ForeignKey('principal.id')),
                Column('application', Integer, ForeignKey('application.id')))
litigation_application_table = Table('lit_app', Base.metadata,
                Column('litigation', Integer, ForeignKey('litigation.id')),
                Column('application', Integer, ForeignKey('application.id')))
opposition_application_table = Table('opp_app', Base.metadata,
                Column('opposition', Integer, ForeignKey('opposition.id')),
                Column('application', Integer, ForeignKey('application.id')))

class ValidationError(Exception):
    pass

class User(Base):
    """User class is not exactly defined yet.

    Not sure whether i will implement it
    
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    
    def __init__(self, name, surname, password=None):
        self.name = name
        self.surname = surname
        self. password = password
        
    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.surname)


class Principal(Base):
    """An active principal of the law firm.
    
    He can be assigned to a number of cases.
    Many principals can be assigned to a specific case.
    
    """
    __tablename__ = 'principal'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    afm= Column(String)
    
    def __init__(self, name, surname, afm):
        """Initialization method for Principal class.
        
        afm: VAT(ΑΦΜ, Αριθμος Φορολογικού Μητρώου)

        """
        self.name = name
        self.surname = surname
        self.afm = afm        
        
    def __repr__(self):
        """Representation method for Principal."""
        return "<Principal('%s', '%s')>" % (self.name, self.surname)


class Litigation(Base):
    """Litigation object assigned to an application.

    Litigation should be connected to either a NPerson or an Entity.
    Associating the litigation to an application, should always occur 
    after the litigation is connected.

    """
    __tablename__ = 'litigation'

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime)
    time_modified = Column(DateTime, nullable=True)
    # foreign keys
    nperson_id = Column(Integer, ForeignKey('nperson.id'), nullable=True)
    entity_id = Column(Integer, ForeignKey('entity.id'), nullable=True)
    
    # relationships
    nperson = relationship("NPerson", backref="litigations")
    entity = relationship("Entity", backref="litigations")

    def __init__(self):
        self.time_created = datetime.now()

    def __repr__(self):
        return "<Litigation('%s')>" % (self.time_created)    

    def is_a_person(self):
        """ Return True if Litigation is connected to a NPerson, False otherwise."""
        if self.nperson == None:
            return False
        else:
            return True

    def is_an_entity(self):
        """ Return True if Litigation is connected to an Entity, False otherwise."""
        if self.entity == None:
            return False
        else:
            return True

    def isConnected(self):
        """Return True if Litigation is connected, or False if not."""
        return self.is_an_entity() or self.is_a_person()

    def connect_to_Entity(self, entity):
        """ Connect to entity  if litigation is not already connected."""
        try:
            if not self.isConnected():
                self.entity = entity
                return True
            else:
                raise ValidationError
        except ValidationError as err:
            print(err, "litigation is already connected")
        except AttributeError as err:
            print(err)
        return False

    def connect_to_NPerson(self, nperson):
        """ Connect to nperson if litigation is not already connected."""
        try:
            if not self.isConnected():
                self.nperson = nperson
                return True
            else:
                raise ValidationError
        except ValidationError as err:
            print(err, "litigation is already connected")
        except AttributeError as err:
            print(err)
        return False

    def disconnect_me(self):
        """ Disconnect litigation from any connections to nperson or entity."""
        if self.is_a_person():
            del(self.nperson)
            return True
        elif self.is_an_entity():
            del(self.entity)
            return True
        return False
        
    def assign_to_application(self, application):
        """Assign litigation to an application.

        Since this method checks if the litigation is connected before assigning it to
        a specific application, it should be used instead of direct assignment.
        
        """
        
        try:
            # check if connected
            if self.isConnected():
                self.applications.append(application)
                return True
            else:
                raise ValidationError
        # handle possible errors
        except AttributeError as err:
            print(err, ": Argument must be an Application instance")
            return False
        except ValidationError as err:
            print(err, ": This instance is not connected")
            return False
             

class Opposition(Base):
    __tablename__ = 'opposition'

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime)
    time_modified = Column(DateTime, nullable=True)
    nperson_id = Column(Integer, ForeignKey('nperson.id'), nullable=True)
    entity_id = Column(Integer, ForeignKey('entity.id'), nullable=True)

    # relationships
    nperson= relationship("NPerson", backref="oppositions")    
    entity = relationship("Entity", backref="oppositions")    
            
    def __init__(self):
        """Initialization method for Opposition."""
        self.time_created = datetime.now()

    def __repr__(self):
        """Representation method for Opposition."""
        return "<Opposition('%s')>" % (self.time_created)    

    def is_a_person(self):
        """ Check whether this Opposition instance is connected to an NPerson."""
        if self.nperson is None:
            return False
        else:
            return True

    def is_an_entity(self):
        """ Check whether this Opposition instance is connected to an Entity."""
        if self.entity is None:
            return False
        else:
            return True

    def isConnected(self):
        """ Check wheter this Opposition is connected.

        It can either be connected to an Entity or a Nperson Instance.

        """
        return self.is_an_entity() or self.is_a_person()

    def connect_to_Entity(self, entity):
        """ Connect to entity if opposition is not already connected."""
        try:
            if not self.isConnected():
                self.entity = entity
                return True
            else:
                raise ValidationError
        except ValidationError as err:
            print(err, "opposition is already connected")
            return False
        except AttributeError as err:
            print(err)
            return False

    def connect_to_NPerson(self, nperson):
        """ Connect to nperson if opposition is not already connected."""
        try:
            if not self.isConnected():
                self.nperson = nperson
                return True
            else:
                raise ValidationError
        except ValidationError as err:
            print(err, "opposition is already connected")
            return False
        except AttributeError as err:
            print(err)
            return False

    def disconnect_me(self):
        """ Disconnect opposition from any connections to nperson or entity."""
        if self.is_a_person():
            del(self.nperson)
            return True
        elif self.is_an_entity():
            del(self.entity)
            return True
        return False

    def assign_to_application(self, application):
        """Assign Opposition to an Application.

        Since this method checks if the Opposition is connected before assigning it to
        a specific Application, it should be used instead of direct assignment.
        
        """
        
        try:
            # check if connected
            if self.isConnected():
                self.applications.append(application)
                return True
            else:
                raise ValidationError
        # handle possible errors
        except AttributeError as err:
            print(err, ": Argument must be an Application instance")
            return False
        except ValidationError as err:
            print(err, ": This instance is not connected")
            return False


class Application(Base):
    """ The application class represents an open case handled by the law firm.

    It is connected to the Principal, Litigation and Opposition classes by many to many 
    relationships. date_of_trial is of crucial importance as it is used to deduce the 
    various deadlines. The other factor is remedy which is not yet implemented.

    """
    __tablename__ = 'application'
    
    id = Column(Integer, primary_key=True)
    date_of_trial = Column(Date)
    principals = relationship("Principal",
                              secondary=principal_application_table,
                              backref="applications")
    litigations = relationship("Litigation",
                               secondary=litigation_application_table,
                               backref="applications")
    oppositions = relationship("Opposition",
                               secondary=opposition_application_table,
                               backref="applications")    
    
    def __init__(self, date_of_trial):
        if isinstance(date_of_trial, date):
            self.date_of_trial = date_of_trial
        else:
            raise TypeError("Argument is not of datetime.date type")

    def __repr__(self):
        return "<Application('%s')>" % (self.date_of_trial)

    
class NPerson(Base):
    """ A NPerson is a natural person that can be a part of an opposition or a litigation in an active application.

    It is connected to a NPerson or an Opposition class by a one to one relationship.
    It also has a Contact Info relationship.

    """
    __tablename__ = 'nperson'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    father_name = Column(String)
    mother_name = Column(String, nullable=True)
    # Identification number, adt: Aριθμος Δελτιου Tαυτοτητας
    adt = Column(String, nullable=True)
    # VAT, afm: Αριθμος Φορολογικου Μητρώου
    afm = Column(String)
    # foreign keys
    contact_info_id = Column(Integer, ForeignKey('contact_info.id'), nullable=True)
    # relationships
    contact_info = relationship("ContactInfo", backref=backref("nperson", uselist=False))
    
    def __init__(self, name, surname, father_name, afm, mother_name=None, adt=None):
        """ Initialization method for NPerson class."""
        self.name = name
        self.surname = surname
        self.father_name = father_name
        self.afm = afm
        self.mother_name = mother_name
        self.adt = adt

    def __repr__(self):
        """ Representation method for NPerson class."""
        return "<NPerson('%s', '%s', '%s')>" % (self.name, self.name, self.afm)
  

class Entity(Base):
    """ An Entity is a natural person that can be a part of an opposition or a litigation in an active application.

    It is connected to a NPerson or an Opposition class by a one to one relationship.
    It also has a Contact Info relationship.
    
    """
    __tablename__ = 'entity'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brandname = Column(String, nullable=True)
    base = Column(String)
    # VAT, afm: Αριθμος Φορολογικου Μητρώου
    afm = Column(String)
    additional_info = Column(String, nullable=True)
    # foreign keys
    contact_info_id = Column(Integer, ForeignKey('contact_info.id'), nullable=True)
    # relationships
    contact_info = relationship("ContactInfo", backref=backref("entity", uselist=False))

 
    def __init__(self, name, afm, base, brandname=None, additional_info=None):
        """ Initialization method for Entity class."""
        self.name = name
        self.afm = afm
        self.base = base
        self.brandname = brandname
        self.additional_info = additional_info
        
    def __repr__(self):
        """ Representation method for Entity class."""
        return "<Entity('%s', '%s', '%s')>" % (self.name, self.base, self.afm)
    

class ContactInfo(Base):
    """ Contact info used by the NPerson and Entity class."""
    __tablename__ = 'contact_info'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    city = Column(String)
    mobile = Column(String)
    email = Column(String)
    # post office
    po = Column(String, nullable=True)
    secondary_address = Column(String, nullable=True)
    home_phone = Column(String, nullable=True)
    work_phone = Column(String, nullable=True)


    def __init__(self, address, city, mobile, email, 
                 po=None, secondary_address=None, home_phone=None, work_phone=None):
        """ Initialization method for ContactInfo class."""
        self.address = address
        self.mobile = mobile
        self.email = email
        self.secondary_address = secondary_address
        self.home_phone = home_phone
        self.work_phone = work_phone

    def __repr__(self):
        """Representation method for ContactInfo class."""
        return "<ContactInfo('%s', '%s')>" % (self.address, self.mobile)


if __name__ == '__main__':
    # define models for interactive use
    # npersons
    john = NPerson("john", "snow", "alex", "98329133")
    alex = NPerson("alex", "mao", "vasili", "91283210")
    bill = NPerson("bill", "hicks", "george", "9210839")
    # entities
    ibm = Entity("IBM", "Virginia", "28173922")
    gp = Entity("Greenpeace", "Athens", "28738122")
    wwf = Entity("WWF", "Amsterdam", "921398127")
    # applications
    application1 = Application(date(2014, 2, 26))
    application2 = Application(date(2013, 12, 13))
    # litigations 
    lit1 = Litigation()
    lit2 = Litigation()
    # oppositions 
    opp1 = Opposition()
    opp2 = Opposition()
    


