"""Actually load PostgreSQL, execute a multi-source join, verify SQLite parity.

Set PG_DSN to your own local database, e.g.
postgresql+psycopg://USER@127.0.0.1:55432/postgres
This project uses a dedicated schema and replaces only its own tables.
"""
from pathlib import Path
import os,json,sqlite3,subprocess
import pandas as pd
from sqlalchemy import create_engine,text

ROOT=Path(__file__).resolve().parents[1]
def main():
    dsn=os.environ.get('PG_DSN')
    if not dsn:raise RuntimeError('Set PG_DSN; see README. Credentials are not stored in this project.')
    engine=create_engine(dsn)
    with engine.begin() as connection:
        connection.execute(text('CREATE SCHEMA IF NOT EXISTS mobile_divide_group01'))
    tables={
        'municipalities':pd.read_csv(ROOT/'data/processed/municipalities.csv'),
        'tiles':pd.read_parquet(ROOT/'data/processed/tiles_assigned.parquet'),
        'stations':pd.read_csv(ROOT/'data/processed/stations_assigned.csv'),
    }
    # Drop only this project's reproducible tables, in dependency order.
    # This makes a second notebook execution work with existing foreign keys.
    with engine.begin() as connection:
        for name in ['tiles','stations','municipalities']:
            connection.execute(text(f'DROP TABLE IF EXISTS mobile_divide_group01.{name}'))
    for name,df in tables.items():df.to_sql(name,engine,schema='mobile_divide_group01',if_exists='replace',index=False,chunksize=1000)
    query=(ROOT/'src/group_summary.sql').read_text()
    with engine.begin() as connection:
        connection.execute(text('SET search_path TO mobile_divide_group01'))
        for name,col in [('municipalities','bfs_id'),('tiles','quadkey'),('stations','record_key')]:
            connection.execute(text(f'ALTER TABLE {name} ADD PRIMARY KEY ({col})'))
        connection.execute(text('CREATE INDEX tiles_municipality_idx ON tiles(bfs_id)'))
        connection.execute(text('CREATE INDEX stations_municipality_idx ON stations(bfs_id)'))
        for name in ['tiles','stations']:
            connection.execute(text(f'ALTER TABLE {name} ADD FOREIGN KEY (bfs_id) REFERENCES municipalities(bfs_id)'))
        result=pd.read_sql_query(text(query),connection)
        version=connection.execute(text('SELECT version()')).scalar()
        # Demonstrates the infrastructure/source JOIN separately from Ookla aggregation.
        infrastructure=pd.read_sql_query(text('''SELECT m.municipality_type,
            COUNT(DISTINCT m.bfs_id) AS municipalities,
            COUNT(s.record_key) AS matched_station_records,
            SUM(s.has_5g) AS records_with_5g
            FROM municipalities m LEFT JOIN stations s ON m.bfs_id=s.bfs_id
            GROUP BY m.municipality_type ORDER BY m.municipality_type'''),connection)
    result.to_csv(ROOT/'results/postgres_query_result.csv',index=False)
    infrastructure.to_csv(ROOT/'results/postgres_infrastructure_join.csv',index=False)
    expected=pd.read_csv(ROOT/'results/sqlite_query_result.csv')
    pd.testing.assert_frame_equal(result,expected,check_dtype=False,rtol=1e-10)
    (ROOT/'results/postgres_verification.json').write_text(json.dumps({'status':'executed successfully','server':version,'schema':'mobile_divide_group01','tables':{k:len(v) for k,v in tables.items()},'join_and_aggregation':'Executed in PostgreSQL from Python','sqlite_parity':'PASS','primary_and_foreign_keys':'enforced','database_credentials':'not included'},indent=2))
    print(result.to_string(index=False));print('PostgreSQL execution and SQLite parity: PASS')

if __name__=='__main__':main()
