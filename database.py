#this file contains the database connections and engine connections and session creations
#---to create engine
from sqlalchemy import create_engine
#---to create a base class for all tables and sessions 
from sqlalchemy.orm import sessionmaker,declarative_base
#--to load the environmental variables
import os
from dotenv import load_dotenv
load_dotenv()#this will fetch all environmental variables
#----Base class for all tables
Base=declarative_base()
#fetching DB_URL
DATABASE_URL=os.getenv('DATABASE_URL')
#---engine creation
engine=create_engine(DATABASE_URL)
#----Session maker
SessionLocal=sessionmaker(bind=engine)