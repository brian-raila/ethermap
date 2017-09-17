from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

db = create_engine('sqlite:///.db/deebee.db')
meta = MetaData()

coinbase = Table('coinbase', meta,
	Column('wallet_id', String, primary_key=True),
	Column('json_keystore', String, nullable=False),
	Column('password_hash', String, nullable=False),
	Column('wallet_pseudo', String, nullable=False),
	Column('public_address', String, nullable=False)
	)

maps = Table('wallet_maps', meta,
	Column('map_id', String, primary_key=True),
	Column('map_pseudo', String, nullable=False),
	Column('public_address', String, nullable=False),
	Column('map_hash', String, nullable=False)
	)


meta.create_all(db)
session = sessionmaker()
session.configure(bind=db)