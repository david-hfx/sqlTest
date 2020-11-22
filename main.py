import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    r"sqlite:///C:\Users\david\AppData\Roaming\DBeaverData\workspace6\.metadata\sample"
    r"-database-sqlite-1\Chinook.db"
)

if __name__ == "__main__":
    table_names = engine.table_names()
    print(table_names)

    with engine.connect() as conn:
        sql = "select * from EmpView where trim(ReportsTo)!=''"
        # rs = conn.execute(sql)
        # df = pd.DataFrame(rs.fetchall(), columns=rs.keys())
        df = pd.read_sql(sql, engine)
        print(df)
