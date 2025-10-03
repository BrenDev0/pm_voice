import os
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from typing import List, Dict, Any
from src.workflow.services.embedding.embedding_service import EmbeddingService
from src.workflow.state import State

class PromptService:
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service


    async def custom_prompt_template(
        self,  
        system_message: str, 
        with_input: bool = False,
        input_text: str = None,
        with_chat_history: bool = False,
        chat_history: List[Dict[str, Any]] = None,
        with_context: bool = False, 
        context_collection: str = None,
        context_top_k: int = 4
    ):
        messages = [
            SystemMessagePromptTemplate.from_template(system_message),
            SystemMessage(content=f"You will always answer in {os.getenv("AGENT_LANGUAGE")}")
        ]

        if with_chat_history and chat_history:
            messages = self.add_chat_history(chat_history=chat_history, messages=messages)

        if with_context and context_collection is not None and with_input:
            messages = await self.add_context(
                input=input_text, 
                messages=messages, 
                collection_name=context_collection,
                top_k=context_top_k
            )

        if with_input:
            messages.append(HumanMessage(content=input_text))

        prompt = ChatPromptTemplate.from_messages(messages)

        return prompt


    async def add_context(
        self, 
        input: str, 
        messages: List[Dict[str, Any]], 
        collection_name: str,
        top_k: int = 4
    ) -> List[Any]:
        context = await self.embedding_service.search_for_context(
            query=input,
            collection_name=collection_name,
            top_k=top_k
        )
 
        if context:
            messages.append(SystemMessage(content=f"""
                You have access to the following relevant context retrieved from documents.
                Use this information to inform your response. Do not make up facts outside of this context.

                Relevant context:
                {context}
            """))

        return messages

    @staticmethod
    def add_chat_history(chat_history: List[Dict[str, Any]], messages: List[Any]) -> List[Any]:

        if chat_history:
            for msg in chat_history:
                if msg["message_type"] == "human":
                    messages.append(HumanMessage(content=msg["text"]))
                elif msg["message_type"] == "ai":
                    messages.append(AIMessage(content=msg["text"]))

        return messages
    
    
    
    