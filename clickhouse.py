import time

import pandas as pd
from clickhouse_sqlalchemy import get_declarative_base, make_session, types
from sqlalchemy import Column, create_engine

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

start = time.time()
Base = get_declarative_base()


class System(Base):
    __tablename__ = "asynchronous_metrics"

    metric = Column(types.String, primary_key=True)
    value = Column(types.Float(64))
    #
    # def __init__(self, metric=None, value=None):
    #     self.data = (metric, value)
    #
    # def __repr__(self):
    #     return "{}, {}".format(self.metric, self.value)


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

session = make_session(engine)
# session = Session()
# for _ in range(1000):
rs = session.query(System).filter(System.value > 0)
df = pd.read_sql(sql=rs.statement, con=session.bind)
print(time.time() - start)
