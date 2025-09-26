from collections import deque
from typing import Deque, Dict, List

class ConversationMemory:
    """
    Memoria simple en cola: guarda los últimos N turnos (usuario/modelo).
    """

    def __init__(self, max_messages: int = 12):
        self._messages: Deque[Dict[str, str]] = deque(maxlen=max_messages)

    def add_user(self, content: str):
        """Agregar mensaje del usuario"""
        self._messages.append({"role": "user", "content": content})

    def add_model(self, content: str):
        """Agregar respuesta del modelo"""
        self._messages.append({"role": "model", "content": content})

    def get(self) -> List[Dict[str, str]]:
        """Devolver historial completo"""
        return list(self._messages)

    def clear(self):
        """Limpiar memoria"""
        self._messages.clear()
