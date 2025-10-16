from typing import Union
from uuid import UUID

from src.shared.domain.models import State
from src.shared.domain.entities import Message

class StateService:
    @classmethod
    def update_chat_history(
        cls,
        state: State,
        input: str,
        response: str
    ) -> State:
        human_message = Message(
            type="human",
            content=input
        )

        ai_message = Message(
            type="ai",
            content=response
        )

        state['chat_history'].extend([human_message, ai_message])

        return state
        
    @classmethod
    def get_new_state(
        cls, 
        call_id: Union[UUID, str],
        input: str = None
    ) -> State:
        return State(
            call_id=str(call_id),
            input=input,
            chat_history=[],
            summary="",
            investment_data={},
            client_data={},
            appointment_data={},
            response=None
        )

    @classmethod
    def refresh_turn(
        cls,
        state: State,
        input: str
    ) -> State:
        state["input"] = input
        state["response"] = ""

        return state