import asyncio
from typing import Dict, List, Optional, Union
import google.generativeai as genai
from google.generativeai.types import ContentDict
from tenacity import retry, stop_after_attempt, wait_random_exponential

from app.config import LLMSettings, config
from app.logger import logger
from app.schema import Message, ROLE_VALUES


class GeminiAdapter:
    """Adapter to make Gemini API compatible with OpenManus LLM interface."""
    
    def __init__(self, llm_config: LLMSettings):
        self.model_name = llm_config.model
        self.api_key = llm_config.api_key
        self.max_tokens = llm_config.max_tokens
        self.temperature = llm_config.temperature
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        # Generation config
        self.generation_config = genai.types.GenerationConfig(
            max_output_tokens=self.max_tokens,
            temperature=self.temperature,
        )

    def _convert_messages_to_gemini_format(self, messages: List[dict]) -> List[ContentDict]:
        """Convert OpenAI-style messages to Gemini format."""
        gemini_messages = []
        
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            # Map OpenAI roles to Gemini roles
            if role == "system":
                # Gemini doesn't have system role, prepend to user message
                gemini_messages.append({
                    "role": "user",
                    "parts": [f"System: {content}"]
                })
            elif role == "user":
                gemini_messages.append({
                    "role": "user", 
                    "parts": [content]
                })
            elif role == "assistant":
                gemini_messages.append({
                    "role": "model",
                    "parts": [content]
                })
        
        return gemini_messages

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
    )
    async def generate_content(
        self, 
        messages: List[dict], 
        stream: bool = True
    ) -> str:
        """Generate content using Gemini API."""
        try:
            # Convert messages to Gemini format
            gemini_messages = self._convert_messages_to_gemini_format(messages)
            
            # For single message, use generate_content
            if len(gemini_messages) == 1:
                prompt = gemini_messages[0]["parts"][0]
                
                if stream:
                    # Streaming response
                    response = await asyncio.to_thread(
                        self.model.generate_content,
                        prompt,
                        generation_config=self.generation_config,
                        stream=True
                    )
                    
                    collected_text = []
                    for chunk in response:
                        if chunk.text:
                            collected_text.append(chunk.text)
                            print(chunk.text, end="", flush=True)
                    
                    print()  # Newline after streaming
                    return "".join(collected_text)
                else:
                    # Non-streaming response
                    response = await asyncio.to_thread(
                        self.model.generate_content,
                        prompt,
                        generation_config=self.generation_config
                    )
                    return response.text
            
            else:
                # Multi-turn conversation
                chat = self.model.start_chat(history=gemini_messages[:-1])
                last_message = gemini_messages[-1]["parts"][0]
                
                if stream:
                    response = await asyncio.to_thread(
                        chat.send_message,
                        last_message,
                        generation_config=self.generation_config,
                        stream=True
                    )
                    
                    collected_text = []
                    for chunk in response:
                        if chunk.text:
                            collected_text.append(chunk.text)
                            print(chunk.text, end="", flush=True)
                    
                    print()  # Newline after streaming
                    return "".join(collected_text)
                else:
                    response = await asyncio.to_thread(
                        chat.send_message,
                        last_message,
                        generation_config=self.generation_config
                    )
                    return response.text
                    
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    @staticmethod
    def format_messages(messages: List[Union[dict, Message]]) -> List[dict]:
        """Format messages for Gemini by converting them to standard dict format."""
        formatted_messages = []

        for message in messages:
            if isinstance(message, dict):
                if "role" not in message:
                    raise ValueError("Message dict must contain 'role' field")
                formatted_messages.append(message)
            elif isinstance(message, Message):
                formatted_messages.append(message.to_dict())
            else:
                raise TypeError(f"Unsupported message type: {type(message)}")

        # Validate all messages have required fields
        for msg in formatted_messages:
            if msg["role"] not in ROLE_VALUES:
                raise ValueError(f"Invalid role: {msg['role']}")
            if "content" not in msg and "tool_calls" not in msg:
                raise ValueError(
                    "Message must contain either 'content' or 'tool_calls'"
                )

        return formatted_messages

    async def ask(
        self,
        messages: List[Union[dict, Message]],
        system_msgs: Optional[List[Union[dict, Message]]] = None,
        stream: bool = True,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Ask Gemini and get response (compatible with OpenManus LLM interface).
        """
        try:
            # Update temperature if provided
            if temperature is not None:
                self.generation_config.temperature = temperature

            # Format system and user messages
            if system_msgs:
                system_msgs = self.format_messages(system_msgs)
                messages = system_msgs + self.format_messages(messages)
            else:
                messages = self.format_messages(messages)

            response = await self.generate_content(messages, stream=stream)
            
            if not response or not response.strip():
                raise ValueError("Empty response from Gemini API")
                
            return response.strip()

        except Exception as e:
            logger.error(f"Error in Gemini ask: {e}")
            raise

    async def ask_tool(self, *args, **kwargs):
        """
        Tool calling not yet implemented for Gemini.
        Falls back to regular ask method.
        """
        logger.warning("Tool calling not yet implemented for Gemini. Using regular ask method.")
        return await self.ask(*args, **kwargs)