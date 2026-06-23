#this file contains all the API's which is useful for our Task Management System
from datetime import datetime,timedelta,timezone
from database import Base,engine,SessionLocal
from sqlalchemy.orm import Session
import models
from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel,Field
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM=os.getenv('ALGORITHM')
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
oauth2scheme=OAuth2PasswordBearer(tokenUrl="login")
from passlib.context import CryptContext
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
from jose import jwt,JWTError
#let me create all the tables in the database 
Base.metadata.create_all(engine)
#let me create Fastapi app
app=FastAPI()
#welcome page
@app.get('/',tags=['Welcome'])
def home():
    return 'Welcome to Task Management System'
#dependency function
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
#hasing password
def hashPassword(password):
    return pwd_context.hash(password)
#verify password
def verifyPassword(password,hashpassword):
    return pwd_context.verify(password,hashpassword)
#create token
def create_token(data:dict):
    to_encode=data.copy()
    exp=datetime.utcnow()+timedelta(minutes=30)
    to_encode.update({'exp':exp})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
#verify token
def verify_token(token:str):
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
         raise HTTPException(status_code=401,detail='Invalid Token or Token Expired')
#---AUTH API's---------
class registerUser(BaseModel):
    name:str
    email:str
    password:str
    role:str='member'
#-------Create Team---------
class createTeam(BaseModel):
    name:str
#-----Add users to Team-----------
class addUserTeam(BaseModel):
    user_id:int
    team_id:int
#------------Create Task----------------
class createTask(BaseModel):
    title:str
    description:str
    status:str='TODO'
    priority:str
    team_id:int
    created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
#--------------Assign  Task------------
class assignTask(BaseModel):
    task_id:int
    assigned_to:int
    team_id:int
#----------------update status-------
class updateStatus(BaseModel):
    status:str
#---------------Add Comment---------------
class addComment(BaseModel):
    task_id:int
    user_id:int
    comment_text:str
    created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
#---------1.register ----------------
@app.post("/register",tags=['Register'])
def register(add:registerUser,db:Session=Depends(get_db)):
    exist=db.query(models.User).filter(models.User.email==add.email).first()#if mail matches then user already exists
    if not exist:
        user=models.User(name=add.name,email=add.email,password=hashPassword(add.password),role=add.role.lower())
        #add to user to session
        db.add(user)
        #comitting user to database
        db.commit()
        db.refresh(user)
        return {
            'message':'Registered Successfully',
            'user':{
                "user_id":user.id,
                "user_name":user.name,
                "user_email":user.email,
                "user_role":user.role
            }
        }
    raise HTTPException(status_code=400,detail='Email Already Exist')
#---------2.Login------------------------
@app.post('/login',tags=['Login'])
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==form_data.username).first()
    if not user:
        raise HTTPException(status_code=400,detail='User Not Found')
    if not verifyPassword(form_data.password,user.password):
        raise HTTPException(status_code=401,detail='Invalid Credentials')
    token=create_token({'sub':str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user.name
    }
#--------3.0 get profile----
#to get current user
def get_current_user(token:str=Depends(oauth2scheme)):
    payload=verify_token(token)
    return int(payload.get('sub'))
#------3.1 profile API----------
@app.get('/profile',tags=['Get Profile'])
def get_profile(user=Depends(get_current_user),db:Session=Depends(get_db)):
    userdetails=db.query(models.User).filter(models.User.id==user).first()
    if userdetails:
        return{
        'id':userdetails.id,
        'name':userdetails.name,
        'email':userdetails.email
                }
    raise HTTPException(status_code=404,detail='user not found')
#-------Teams API's-------------
#------------4.create Team--------------
@app.post('/teams',tags=['Create Team'])
def teams(add:createTeam,db:Session=Depends(get_db)):
    team=models.Team(name=add.name)
    #add to session
    db.add(team)
    #commit to database
    db.commit()
    db.refresh(team)
    return{
        "message":'Team created Successfully',
        "team_id":team.id
    }
#---------5.Add users to Team Members----------
@app.post('/team/addTeamMembers',tags=['Add Users To Team Members'])
def addTeamMembers(add:addUserTeam,db:Session=Depends(get_db)):
    user_exist=db.query(models.User).filter(models.User.id==add.user_id).first()
    team_exist=db.query(models.Team).filter(models.Team.id==add.team_id).first()
    #if user not exist
    if not user_exist:
        raise HTTPException(status_code=404,detail='User Not Found')
    #if team not exist
    if not team_exist:
        raise HTTPException(status_code=404,detail='Team Not Found')
    team_add=models.TeamMember(user_id=add.user_id,team_id=add.team_id)
    #add to session
    db.add(team_add)
    #commit to db
    db.commit()
    #refresh
    db.refresh(team_add)
    return{
        'message':'Users Added to Team Successfully'
    }
#----------6.Get Team Members-----------
@app.get('/team/users',tags=['Get Team Members'])
def users_from_team(db:Session=Depends(get_db)):
    teamMembers=db.query(models.TeamMember).all()
    if not teamMembers:
        raise HTTPException(status_code=404,detail='Team Members Not Found')
    return{
        'Team_Members':
        [
            {'Team_Member_id':TeamMember.id,
            'User_id':TeamMember.user_id,
            'team_id':TeamMember.team_id
            }
            for TeamMember in teamMembers
        ] 
    }
#------TASK API's-----------------
#----------------7.Create Task---------------------
@app.post('/task',tags=['Create Task'])
def create_task(add:createTask, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user).first()
    if user.role not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    task=models.Task(title=add.title,
                     description=add.description,
                     status=add.status,
                     priority=add.priority,
                     team_id=add.team_id,
                     created_at=add.created_at)
    db.add(task)
    db.commit()
    db.refresh(task)
    return{
        'message':'Task Created Successfully'
    }
#--------------8.Assign Task-----------------
@app.patch('/task/assign',tags=['Assign Task'])
def assign_task(add:assignTask,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == add.assigned_to).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task = db.query(models.Task).filter(models.Task.id == add.task_id).first()
    team = db.query(models.Team).filter(models.Team.id == add.team_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    task.assigned_to = add.assigned_to
    task.team_id = add.team_id
    db.commit()
    db.refresh(task)
    return{
        'message':'Task Assigned Successfully'
    }
#------------9.Update Status------------
@app.put('/task/statusupdate/{id}',tags=['Update Status'])
def updateStatus(id:int, add:updateStatus,db:Session=Depends(get_db)):
    task=db.query(models.Task).filter(models.Task.id==id).first()
    if not task:
        raise HTTPException(status_code=404,detail='Task Not Found')
    task.status = add.status
    db.commit()
    db.refresh(task)
    return{
        'message':'Task Updated Sucessfully',
        'task_id':task.id
    }
#-----------10. DELETE TASK-----------------
@app.delete('/task/delete/{id}',tags=['Delete Task'])
def delete(id:int,db:Session=Depends(get_db)):
    task=db.query(models.Task).filter(models.Task.id==id).first()
    if not task:
        raise HTTPException(status_code=404,detail='Task Not Found')
    db.delete(task)
    db.commit()
    return{
        'message':'Deleted Successfully'
    }
#---------11.Get All Tasks(Admin)------------
@app.get('/admin/tasks',tags=['Get All Tasks (Admin)'])
def get_all_tasks_Admin(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user).first()
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='Not allowed')
    tasks=db.query(models.Task).all()
    return{
        'Tasks':[
            {
                'Task_id':task.id,
                'Task_title':task.title,
                'Task_description':task.description,
                'Task_status':task.status,
                'Task_Priority':task.priority,
                'Task_Assigned_To':task.assigned_to,
                'Team_id':task.team_id,
                'Task_created_at':task.created_at
            }for task in tasks
        ]
    }
#-----------12.Get My Tasks------------
@app.get('/task/mytasks',tags=['Get My Tasks'])
def mytasks(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==current_user).first()
    tasks=db.query(models.Task).filter(models.Task.assigned_to==current_user).all()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not tasks:
        raise HTTPException(status_code=404,detail='Tasks Not Yet Assigned')
    if user.role == "admin":
        return {
            'user':'Admin',
            'Tasks':db.query(models.Task).all()
        }
    return {
        'user_id':current_user,
        'tasks': tasks
    }
#-----------13. Get Team Tasks---------------
@app.get('/team/task/{id}',tags=['Get Teams Tasks'])
def team_tasks(id:int,db:Session=Depends(get_db)):
    teams_tasks=db.query(models.Task).filter(models.Task.team_id==id).all()
    if not teams_tasks:
        raise HTTPException(status_code=404,detail='No tasks found')
    return{
            'team_id':id,
            'tasks':
            [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status,
                    "priority": t.priority
                }
                for t in teams_tasks
            ]
            }
#-----------14.Filter By Status----------------
@app.get('/filter/{status}',tags=['Filter By Status'])
def status_filter(status:str,db:Session=Depends(get_db)):
    tasks=db.query(models.Task).filter(models.Task.status==status).all()
    return {
    "Tasks": [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority
        }
        for t in tasks
            ]
        }
#------------Comment API's--------
#-------------15.Add Comment---------------
@app.post('/add/comment',tags=['Add Comment'])
def comment(add:addComment,db:Session=Depends(get_db)):
    task_exist=db.query(models.Task).filter(models.Task.id==add.task_id).first()
    user_exist=db.query(models.User).filter(models.User.id==add.user_id).first()
    if not task_exist:
        raise HTTPException(status_code=404,detail='Task Not Exist')
    if not user_exist:
        raise HTTPException(status_code=404,detail='User Not Exist')
    task = db.query(models.Task).filter(models.Task.id == add.task_id).first()
    if task.team_id is None:
        raise HTTPException(status_code=400, detail="Task not assigned to any team")
    if task.assigned_to != add.user_id:
        raise HTTPException(status_code=403, detail="Only assigned user can comment")
    comment=models.Comment(task_id=add.task_id,user_id=add.user_id,comment_text=add.comment_text,created_at=add.created_at)
    #add to session
    db.add(comment)
    #commit to db
    db.commit()
    #refresh
    db.refresh(comment)
    return{
        'message':'Comment Added Successfully'
    }
#-------------16.Get comments of a task-------------
@app.get('/comment/task/{id}',tags=['Comments Of a Task'])
def comments_task(id:int,db:Session=Depends(get_db)):
    comment=db.query(models.Comment).filter(models.Comment.task_id==id).first()
    if not comment:
        raise HTTPException(status_code=404,detail='Comments Not Found')
    return {
    "message": "Comment Fetched Successfully",
    "comment": {
        "id": comment.id,
        "task_id": comment.task_id,
        "user_id": comment.user_id,
        "comment_text": comment.comment_text,
        "created_at": comment.created_at
    }
            }