from pydantic import BaseModel, Field


# Dữ liệu client gửi khi đăng ký
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6)
    fullname: str = Field(min_length=1, max_length=100)


# Dữ liệu client gửi khi đăng nhập
class UserLogin(BaseModel):
    username: str
    password: str


# Dữ liệu trả về cho client
class UserResponse(BaseModel):
    id: str
    username: str
    fullname: str