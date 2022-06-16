from typing import List
import uuid
import cloudinary
from fastapi import FastAPI, File,Response, status, HTTPException, Depends, APIRouter, UploadFile, Form
from sqlalchemy.orm import Session
from .. import models, schemas, utils, email_config
from ..database import get_db
from ..config import pictures
import cloudinary.uploader
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

router = APIRouter(
    tags=['Users']
)

cloudinary.config(
    cloud_name=pictures.cloud_name,
    api_key=pictures.cloud_api_key,
    api_secret=pictures.cloud_api_secret
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):
    print(user)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    if not utils.verify(user.confirmPassword, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail =f"Your password doesn't match" )

    user.confirmPassword = user.password  

    # print(user.profileIamge.filename)
    # result =await cloudinary.uploader.upload(user.profileIamge.file)
    # url = result.get("url")
    # print(result)
    # print(url)
    print(user)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
@router.post("/upload/{id}", status_code=status.HTTP_201_CREATED)
async def upload_photo(id:int,profileImage:UploadFile=File(...),db: Session = Depends(get_db)):

    result = cloudinary.uploader.upload(profileImage.file)
    url = result.get("url")
    profileImage = url
    print(profileImage)
    found = db.query(models.User).filter(models.User.id == id)
    user = found.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with id: {id} does not exist" ) 

    x = dict(profileImage=url)
    found.update(x, synchronize_session=False)
    db.commit()
    
    return{"message":"You're okay"}



@router.get('/user/{id}', response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id == id).first()


    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with id: {id} does not exist" ) 

    return user

@router.post('/user/forgot_password')
async def forgot_password(user: schemas.ForgotPasword,db: Session = Depends(get_db)):

    found_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not found_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail =f"Invalid credentials. Please provide your E-mail.")
    
    if found_user:
        reset_code = uuid.uuid1()
        user = models.Code(user_id=found_user.id, reset_code= reset_code)
        db.add(user)
        db.commit()
        db.refresh(user)
    

    subject = "Hello "
    recipient = [found_user.email]
    message = """
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <div style="width:100%;font-family: monospace;">

        <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the button.  
        <a href="http://127.0.0.1:8000/user/forgot_password/{0:}" style="box-sizing:border-box;border-color:#1f8feb;text-decoration:none;background-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px 24px;text-transform:capitialize;display:inline-block\"target=\"_blank\">Reset your password</a>\n <p>If you did't request this,you can ignore this email.</p>
        </div>
        </body>
        </html>""".format(reset_code)

    await email_config.send_email(subject,recipient,message)
    print(reset_code)    


    return {"messgae":"we have send email to reset your password"}

@router.patch('/user/forgot_password/{reset_code}')
def reset_password(reset_code:str,password:schemas.Password,db: Session = Depends(get_db)):

    reset = db.query(models.Code).filter(models.Code.reset_code == reset_code).first()
    if reset:
        found = db.query(models.User).filter(models.User.id == reset.user_id)
        post = found.first()
        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User doesnot exist.")
        hashed_password = utils.hash(password.password)
        password.password = hashed_password
        password.confirmPassword = password.password
        password.email = post.email
        found.update(password.dict(),synchronize_session=False)
        db.commit()
    
    return{"message":"Your password has been reset"}
