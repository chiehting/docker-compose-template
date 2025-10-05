"""
title: Hello User
author: Chiehting
description: This tool calculates the inverse of a string
version: 0.1.0
licence: MIT
"""

from typing import Callable, Any
import asyncio

class Tools:
    def __init__(self):
        pass

    async def hello_world(
        self,
        name: str,
        __user__: dict,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Say hello to someone.
        
        :param name: The name of the person to greet
        :return: A greeting message
        """
        
        # 發送狀態更新（可選）
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"Greeting {name}...", "done": False},
                }
            )
            
        # 模擬一些處理時間
        await asyncio.sleep(1)
        
        greeting = f"Hello, {name}! 👋 Welcome to Open WebUI Tools!"
        
        # 發送完成狀態
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status", 
                    "data": {"description": "Greeting complete!", "done": True}
                }
            )
        
        return greeting

    async def get_user_info(
        self,
        __user__: dict,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Get current user information.
        
        :return: User information as a formatted string
        """
        
        user_name = __user__.get("name", "Unknown User")
        user_email = __user__.get("email", "No email provided")
        user_role = __user__.get("role", "user")
        
        info = f"""
        📋 **User Information:**
        - **Name:** {user_name}
        - **Email:** {user_email}
        - **Role:** {user_role}
        - **ID:** {__user__.get("id", "N/A")}
        """
        
        return info.strip()

    async def calculate_sum(
        self,
        numbers: str,
        __user__: dict,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Calculate the sum of comma-separated numbers.
        
        :param numbers: Comma-separated numbers (e.g., "1,2,3,4,5")
        :return: The sum result
        """
        
        try:
            # 解析數字
            num_list = [float(x.strip()) for x in numbers.split(",")]
            
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"Calculating sum of {len(num_list)} numbers...", 
                            "done": False
                        },
                    }
                )
            
            result = sum(num_list)
            
            response = f"""
            🧮 **Calculation Result:**
            - **Numbers:** {numbers}
            - **Sum:** {result}
            - **Count:** {len(num_list)} numbers
            """
            
            return response.strip()
            
        except ValueError as e:
            return f"❌ Error: Invalid number format. Please use comma-separated numbers like '1,2,3,4,5'"
        except Exception as e:
            return f"❌ Error: {str(e)}"