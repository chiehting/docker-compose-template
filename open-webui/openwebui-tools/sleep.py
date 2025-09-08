from datetime import datetime
import time
from typing import Awaitable, Callable
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        pass

    class UserValves(BaseModel):
        pass

    def __init__(self):
        self.valves = self.Valves()
        self.user_valves = self.UserValves()

    async def test_function(self, prompt: str, __user__: dict, __event_emitter__=None) -> str:
        """
        This is a demo

        :param prompt: this is a test parameter
        """
        try:
            await __event_emitter__({
                "type": "status",
                "data": {"description": "Message that shows up in the chat", "done": False}
            })

            # Do some other logic here

            await __event_emitter__({
                "type": "status",
                "data": {"description": "Completed a task message", "done": True, "hidden": False}
            })

            return "Success"
        except Exception as e:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"An error occured: {e}", "done": True}
            })
            return f"Tell the user: {e}"
