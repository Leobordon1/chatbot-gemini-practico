from typing import Optional
from config import settings
from roles import RolePreset, ROLE_SYSTEM_PROMPTS
from prompts import build_system_prompt, collapse_history
from memory import ConversationMemory
from llm_client import GeminiClient

class ChatService:
    """
    Servicio principal del chat: maneja rol, memoria y conexión a Gemini.
    """

    def __init__(self, role: RolePreset = RolePreset.ASISTENTE):
        self.role = role
        self.memory = ConversationMemory(max_messages=settings.max_history_messages)
        self.client = GeminiClient(api_key=settings.api_key, model_name=settings.model)

    def set_role(self, role: RolePreset):
        """Cambiar rol del chatbot"""
        self.role = role

    def ask(self, prompt: str) -> str:
        """
        Enviar prompt al modelo, manejar historial y actualizar memoria.
        """
        # Construir contexto de sistema según rol
        system_prompt = build_system_prompt(ROLE_SYSTEM_PROMPTS[self.role])
        
        # Historial (colapsado/sumarizado si hace falta)
        history = collapse_history(self.memory.get())
        
        # Generar respuesta
        response_text = self.client.generate(
            system_prompt=system_prompt,
            history=history,
            user_message=prompt,
            max_retries=settings.max_retries,
            timeout_seconds=settings.timeout_seconds
        )
        
        # Actualizar memoria
        self.memory.add_user(prompt)
        self.memory.add_model(response_text)
        
        return response_text

    def reset(self):
        """Limpiar toda la memoria de la conversación"""
        self.memory.clear()
