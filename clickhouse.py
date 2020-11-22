import pandas as pd
from clickhouse_sqlalchemy import make_session
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class System(Base):
    __tablename__ = "asynchronous_metrics"

    metric = Column(String, primary_key=True)
    value = Column(Float(64))
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
    connection, echo=True, pool_size=100, pool_recycle=3600, pool_timeout=20
)


def get_session(db_engine):
    return make_session(db_engine)


def execute(sql):
    session = get_session(engine)
    cursor = session.execute(sql)
    try:
        # fields = cursor.keys()
        # return [dict(zip(fields, item)) for item in cursor.fetchall()]
        return pd.DataFrame(cursor.fetchall(), columns=cursor.keys())
    finally:
        cursor.close()
        session.close()


if __name__ == "__main__":

    # base_sql = "select * from system.asynchronous_metrics"
    # df = execute(base_sql)
    # print(df)
    # # get_data()
    # print(Base.metadata.create_all(engine))
    Session = sessionmaker(bind=engine)
    session = Session()
    rs = session.query(System).filter(System.value > 0)
    # print(rs)
    # df = pd.DataFrame([(d.metric, d.value) for d in rs], columns=["metric", "value"])
    df = pd.read_sql(sql=rs.statement, con=session.bind)
    print(df)
    # for i in rs:
    #     print(i.__dict__)
    # Base.metadata.create_all(engine)
    # print(System.__table__)
