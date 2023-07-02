import requests
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, BOOLEAN
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Step 1: Data Fetching
print("Data Fetching from API..........")
api_url = "https://api.stackexchange.com/2.3/tags"
params = {
    "order": "desc",
    "sort": "popular",
    "site": "stackoverflow",
    "pagesize": 100
}

response = requests.get(api_url, params=params)
print("Data Fetching Completed from API..........")

data = response.json()["items"]

# Step 2: Data Storage (SQLite)
DB_FILE = os.path.join(str(os.getcwd()),"tags.db")

# Create the SQLAlchemy engine
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)

# Create the SQLAlchemy base model
Base = declarative_base()

# Define the Tag model
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    has_synonyms = Column(BOOLEAN)
    is_moderator_only = Column(BOOLEAN)
    is_required = Column(BOOLEAN)
    count = Column(Integer)
    name = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

# Create the database tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
print('--------------------SESSION CREATED--------------------')


# Insert the fetched data into the table
for tag in data:
    has_synonyms = tag["has_synonyms"]
    is_moderator_only = tag["is_moderator_only"]
    is_required = tag["is_required"]
    count = tag["count"]
    name = tag["name"]
    year = int(str(datetime.now()).split(' ')[0].split('-')[0])
    month = int(str(datetime.now()).split(' ')[0].split('-')[1])

    new_tag = Tag(has_synonyms=has_synonyms,is_moderator_only=is_moderator_only,is_required=is_required,count=count,name=name,year=year,month=month)
    session.add(new_tag)

# Commit the changes to the database
session.commit()


# Step 3: Answering Business Query
# Query the database for the top trending tags this month
print("----------BUSINESS QUERY START----------")
this_month = datetime.now().month
this_year = datetime.now().year


top_tags = session.query(Tag).filter(
    Tag.month == this_month,
    Tag.year == this_year
).order_by(Tag.count.desc()).limit(10)

for tag in top_tags:
    print(tag.name)

print("----------BUSINESS QUERY END----------")
session.close()
print('--------------------SESSION CLOSED--------------------')
'''
# Step 4: BI Integration
# I have connected Power BI Desktop tools to the SQLite database and analyze the data as per requirements.
# I have attached the screenshots and step to follow in the separate document 'IntegratingSQLiteWithPowerBI', which I am attaching it into the Github link.
# This assessment, I found it most interesting and surely test the skills for Data Engineer :) :)
'''