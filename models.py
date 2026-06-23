#this file contains all the models that will be useful for task management
from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Text,DateTime
from sqlalchemy.orm import relationship
#---let's create first table 
#----1.User Table
class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)#this is the id of the user which is unique
    name=Column(String,nullable=False)#this is the name of the user which is not null
    email=Column(String,unique=True)#this is the email of the user which is unique
    password=Column(String,nullable=False)#this is the password of the user
    role=Column(String,nullable=False,default='member')#this is the role of the user
    task_rel=relationship('Task',back_populates='user_rel')
    team_rel=relationship('Team',back_populates='user_rel')
#------2.Teams Table
class Team(Base):
    __tablename__='team'
    id=Column(Integer,primary_key=True)#this is the id of the team which is unique
    name=Column(String,nullable=False)#this is the name of the team which is not null
    created_by=Column(Integer,ForeignKey('user.id'))#this is created by the user which refers to user id in user table
    task_rel=relationship('Task',back_populates='team_rel')
    user_rel=relationship('User',back_populates='team_rel')
#-----3.Team Members Table
class TeamMember(Base):
    __tablename__='team_member'
    id=Column(Integer,primary_key=True)#this is the id of the team members
    user_id=Column(Integer,ForeignKey('user.id'))#this is the user id which refers to user id in the user table
    team_id=Column(Integer,ForeignKey('team.id'))#this is the tema id which refers to team id in the team table
#---------4.Tasks Table
class Task(Base):
    __tablename__='task'
    id =Column(Integer,primary_key=True)#id of the task
    title=Column(String)#title of the task
    description=Column(Text)#description about the task
    status=Column(String)#(TODO / IN_PROGRESS / DONE)#status of the task
    priority=Column(String) #(LOW / MEDIUM / HIGH)  #priority of the task
    assigned_to=Column(Integer,ForeignKey('user.id'))#task assigned to which use
    team_id=Column(Integer,ForeignKey('team.id'))#task assigned to which team
    created_at=Column(DateTime)#created on
    user_rel=relationship('User',back_populates='task_rel')
    team_rel=relationship('Team',back_populates='task_rel')
    com_rel=relationship('Comment',back_populates='task_rel')
#-----------5.Comments Table-------
class Comment(Base):
    __tablename__='comments'
    id=Column(Integer,primary_key=True)
    task_id=Column(Integer,ForeignKey('task.id'))
    user_id=Column(Integer,ForeignKey('user.id'))
    comment_text=Column(Text)
    created_at=Column(DateTime)
    task_rel=relationship('Task',back_populates='com_rel')