from contextlib import contextmanager
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import pymysql
import os
from dotenv import load_dotenv
import traceback
import base58

# 加载 .env 文件中的环境变量
load_dotenv()


def is_valid_solana_address(address):
    try:
        # Base58 解码
        decoded = base58.b58decode(address)

        # 检查解码后的字节长度是否为 32
        if len(decoded) == 32:
            return True
        else:
            return False
    except ValueError:
        # 如果解码失败，则地址无效
        return False


@contextmanager
def get_db_connection():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        print("建立数据库连接")
        yield connection
    finally:
        print("关闭数据库连接")
        connection.close()


# 依赖注入方式提供数据库连接
def get_db():
    with get_db_connection() as connection:
        yield connection


connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)


app = FastAPI(
    title="TaskOn Verification API Demo",
    description="A demo API for TaskOn task verification integration",
    version="1.0.0",
)

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class VerificationResponse(BaseModel):
    result: dict = {"isValid": bool}
    error: Optional[str] = None


# DEMO_COMPLETED_TASKS = {
#     # Demo wallet addresses
#     "0xd5045deea369d64ab7efab41ad18b82eeabcdefg",
#     "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
#     # Demo social accounts
#     "taskonxyz",
#     "1084460817220641111",  # Discord ID
#     "6881505111",  # Telegram ID
#     "demo@taskon.xyz",
# }


@app.get(
    "/api/task/verification",
    response_model=VerificationResponse,
    summary="Verify Task Completion",
    description="Verify if a user has completed the task based on their wallet address or social media ID",
)
async def verify_task(
    address: str,
    # authorization: Optional[str] = Header(None),
    db=Depends(get_db),
) -> VerificationResponse:
    try:
        print("地址:", address)
        is_valid = False
        if not is_valid_solana_address(address):
            print("地址非法")
            return VerificationResponse(
                result={"isValid": is_valid}, error="invalid solana address"
            )

        # cursor = connection.cursor()
        cursor = db.cursor()

        # 执行 SQL 查询
        query = "SELECT * FROM user_info WHERE address = %s"
        cursor.execute(query, (address,))

        # 获取查询结果
        # print("===========")
        results = cursor.fetchall()
        print("result: {}".format(results))
        if results and len(results) > 0:
            is_valid = True

        return VerificationResponse(result={"isValid": is_valid}, error=None)
    except Exception as e:
        traceback.print_exc()
        return VerificationResponse(result={"isValid": False}, error=None)


@app.get("/")
async def root():
    return {"message": "Welcome to TaskOn Verification API Demo"}
