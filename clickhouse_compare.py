import time

import pandas as pd
from clickhouse_sqlalchemy import make_session
from sqlalchemy import MetaData, create_engine

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

metadata = MetaData(bind=engine)
metadata.reflect(schema="system", only=["asynchronous_metrics"])
System = metadata.tables["asynchronous_metrics"]
# Session = sessionmaker(bind=engine)
# session = Session()
session = make_session(engine)
# for _ in range(1000):
rs = session.query(System).filter(System.c.value > 0)
df = pd.read_sql(sql=rs.statement, con=session.bind)
print(time.time() - start)
