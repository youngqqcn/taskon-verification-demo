from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import pymysql
import os
from dotenv import load_dotenv
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
    address: str, authorization: Optional[str] = Header(None)
) -> VerificationResponse:
    print("地址:", address)
    is_valid = False
    if not is_valid_solana_address(address):
        return VerificationResponse(
            result={"isValid": is_valid}, error="invalid solana address"
        )

    cursor = connection.cursor()

    # 执行 SQL 查询
    query = "SELECT * FROM user_info WHERE address = %s"
    cursor.execute(query, (address,))

    # 获取查询结果
    # print("===========")
    results = cursor.fetchall()
    if results and len(results) > 0:
        is_valid = True

    return VerificationResponse(result={"isValid": is_valid}, error=None)


@app.get("/")
async def root():
    return {"message": "Welcome to TaskOn Verification API Demo"}