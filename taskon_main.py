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
import requests

# 加载 .env 文件中的环境变量
load_dotenv()

assert os.getenv("TASK_TOKEN").strip() != "", "请设置.env中的TASK_TOKEN"

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
        connection.close()
        print("关闭数据库连接")


# 依赖注入方式提供数据库连接
def get_db():
    with get_db_connection() as connection:
        yield connection


app = FastAPI(
    title="TaskOn Verification API Demo",
    description="A demo API for TaskOn task verification integration",
    version="1.0.0",
)

# Add CORS middleware configuration
# app.add_middleware(
#     CORSMiddleware,
#     # allow_origins=["*"],  # Allows all origins
#     allow_credentials=False,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )


class VerificationResponse(BaseModel):
    result: dict = {"isValid": bool}
    error: Optional[str] = None

class SubmitResponse(BaseModel):
    msg: str
    code: int
    data: Optional[dict] = None

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
    print("地址:", address)
    addr = address.strip().lower()
    try:
        is_valid = False
        if len(address) < 40 or len(address) > 50:
            print("地址非法")
            return VerificationResponse(
                result={"isValid": is_valid}, error="invalid solana address"
            )

        # cursor = connection.cursor()
        cursor = db.cursor()

        # 执行 SQL 查询,  因为 TaskOn传来的都是小写，因此必须要大小写不敏感， 使用 ci
        query = "SELECT * FROM user_info WHERE LOWER(address) = %s"
        cursor.execute(query, (addr,))

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


@app.get(
    "/api/task/verification2",
    response_model=SubmitResponse,
    summary="submit digitask uid",
    description="xx",
)
async def finish_digitask(
    address: str,
    userid: str,
    # authorization: Optional[str] = Header(None),
    db=Depends(get_db),
) -> SubmitResponse:
    print("address = ", address)
    print("userid = ", userid)

    try:

        try:
            i = int(userid.strip())
        except:
            return SubmitResponse(msg="invalid uid", code=1002)

        if not is_valid_solana_address(address):
            return SubmitResponse(msg="invalid solana address", code=1001)

        # cursor = connection.cursor()
        cursor = db.cursor()

        # 执行 SQL 查询,  因为 TaskOn传来的都是小写，因此必须要大小写不敏感， 使用 ci
        query = "SELECT * FROM user_info WHERE LOWER(address) = %s AND age=0"
        cursor.execute(query, (address,))

        # 获取查询结果
        # print("===========")
        results = cursor.fetchall()
        print("result: {}".format(results))
        if results and len(results) > 0:
            resp = requests.post(
                "https://api.digitasks.cc/earn/super/check-ref",
                json={"uid": int(userid.strip())},
                headers={"Authorization": os.getenv("TASK_TOKEN").strip()},
            )
            print("响应resp: ", resp.text)
            if resp and '"code":200,' in resp.text:
                print("响应成功")
                cursor = db.cursor()
                cursor.execute("UPDATE user_info SET age=1 WHERE LOWER(address) = %s", (address,))
                db.commit()
            return SubmitResponse(msg="ok", code=0)

        print("未找到地址，或者，重复调用")
        return SubmitResponse(msg="", code=0)
    except Exception as e:
        traceback.print_exc()
        return SubmitResponse(msg="error", code=1005)



@app.get("/")
async def root():
    return {}
