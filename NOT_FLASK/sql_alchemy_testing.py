from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# To connect to in-memory SQLite DB we use:
engine = create_engine('sqlite:///:memory:', echo=True)

# We create the base class using the declarative_base()
Base = declarative_base()

# Declaring the class User
class User(Base):
    # Indicate the tablename
    __tablename__ = 'users'

    # Indicate the columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    # Indicate the row we get on "print {instance}"
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                      self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    
    # Create the Relationship to Users:
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

# Create the back-relation to Address
User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

# Creating Tables
Base.metadata.create_all(engine)

# Starting a new session
Session = sessionmaker(bind=engine)
session = Session()

# Add a single user
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)

# Add multiple users
session.add_all([User(name='wendy', fullname='Wendy Williams', password='foobar'), User(name='mary', fullname='Mary Contrary', password='xxg527'),User(name='fred', fullname='Fred Flinstone', password='blah')])

# Apply the session changes to DB
session.commit()

# To revert the session changes we can use the session.rollback()

# Some query examples:

for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)

query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
query.all()

for user in session.query(User).filter(text("id<224")).order_by(text("id")).all():
    print(user.name)

# Related objects examples:
jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
jack.addresses = [Address(email_address='jack@google.com'),Address(email_address='j25@yahoo.com')]

session.add(jack)
session.commit()


