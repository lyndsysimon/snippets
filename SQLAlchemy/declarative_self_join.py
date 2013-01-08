# A quick example showing how to create a self-join column in a model, using
# SQLAlchemy's declarative syntax.
#
# This is especially helpful for versioning - old versions of a record may
# be kept in the table, and the most recent version may be accessed by
# filtering on the self-join column.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import column_property, scoped_session, sessionmaker
from sqlalchemy.sql.expression import case


Base = declarative_base()


class Widget(Base):
    __tablename__ = 'widgets'
    id = Column(Integer, primary_key=True)
    name = Column(String(129))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Widget(id=%s;name="%s")>' % (self.id, self.name)

subq = select(
    [func.max(Widget.id).label('maxid'), Widget.name]
).group_by(Widget.name).alias()

Widget.cur = column_property(
    select([
        case([(subq.c.maxid == Widget.id, True)], else_=False)
    ]).where(subq.c.name == Widget.name)
)

engine = create_engine('sqlite://')

Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Session.add(Widget('foo'))
Session.add(Widget('foo'))
Session.add(Widget('bar'))
Session.commit()


# Print all three Widgets
print repr(Session.query(Widget).all())

# Print only the most recent Widget with each name
print repr(Session.query(Widget).filter_by(cur=True).all())
