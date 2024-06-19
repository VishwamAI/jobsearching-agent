from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    resume = Column(String, nullable=True)
    applications = relationship('Application', back_populates='candidate')
    watchlist = relationship('Watchlist', back_populates='candidate')

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
    applications = relationship('Application', back_populates='job')
    watchlist = relationship('Watchlist', back_populates='job')

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    application_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    candidate = relationship('Candidate', back_populates='applications')
    job = relationship('Job', back_populates='applications')

class Watchlist(Base):
    __tablename__ = 'watchlist'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    added_date = Column(DateTime, nullable=False)
    candidate = relationship('Candidate', back_populates='watchlist')
    job = relationship('Job', back_populates='watchlist')

class InterviewSchedule(Base):
    __tablename__ = 'interview_schedule'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    interview_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    candidate = relationship('Candidate')
    job = relationship('Job')

def create_database():
    engine = create_engine('sqlite:///../data/jobsearching_agent.db')
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_database()
    print("Database schema created successfully.")
