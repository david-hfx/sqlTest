import time

import pandas as pd
from clickhouse_sqlalchemy import get_declarative_base, make_session
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import sessionmaker

start = time.time()
conf = {
    # "user": "",
    # "password": "",
    "server_host": "localhost",
    "port": "8123",
    "db": "system",
}
connection = "clickhouse://default:@{server_host}:{port}/{db}".format(**conf)
engine = create_engine(
    connection, echo=False, pool_size=100, pool_recycle=3600, pool_timeout=20
)

# Base = declarative_base(bind=engine)
metadata = MetaData(bind=engine)
metadata.reflect(schema="system", only=["asynchronous_metrics"])
Base = get_declarative_base(metadata=metadata)


class System(Base):
    __tablename__ = "asynchronous_metrics"
    __table__ = Table(__tablename__, metadata, autoload=True, autoload_with=engine)
    # metric = Column(String, primary_key=True)
    __mapper_args__ = {"primary_key": [__table__.c.metric]}


# Session = sessionmaker(bind=engine)
# session = Session()
session = make_session(engine)
# for _ in range(1000):
rs = session.query(System).filter(System.value > 0)
df = pd.read_sql(sql=rs.statement, con=session.bind)
print(time.time() - start)
