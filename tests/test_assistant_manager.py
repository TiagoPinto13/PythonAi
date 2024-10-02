import unittest
from unittest.mock import patch, MagicMock
from pythonAI_wrapper.assistant_manager import AssistantManager
from config import OPENAI_API_KEY

class TestAssistantManager(unittest.TestCase):

    def setUp(self):
        self.manager = AssistantManager()

    @patch('pythonAI_wrapper.assistant_manager.OpenAIAssistant')
    def test_create_assistant(self, mock_assistant):
        self.manager.create_assistant(OPENAI_API_KEY, "test_assistant", "gpt-3.5-turbo", "Test instructions")
        mock_assistant.assert_called_once_with(api_key=OPENAI_API_KEY, name="test_assistant", model="gpt-3.5-turbo", instructions="Test instructions")
        self.assertIn("test_assistant", self.manager.assistants)

    def test_create_duplicate_assistant(self):
        self.manager.create_assistant(OPENAI_API_KEY, "test_assistant")
        with self.assertRaises(ValueError):
            self.manager.create_assistant(OPENAI_API_KEY, "test_assistant")

    def test_get_assistant(self):
        self.manager.create_assistant(OPENAI_API_KEY, "test_assistant")
        assistant = self.manager.get_assistant("test_assistant")
        self.assertIsNotNone(assistant)

    def test_get_nonexistent_assistant(self):
        with self.assertRaises(ValueError):
            self.manager.get_assistant("nonexistent_assistant")

    def test_list_assistants_empty(self):
        self.assertEqual(self.manager.list_assistants(), ["Nenhum assistente criado."])

    def test_list_assistants(self):
        self.manager.create_assistant(OPENAI_API_KEY, "assistant1", "gpt-3.5-turbo")
        self.manager.create_assistant(OPENAI_API_KEY, "assistant2", "gpt-4")
        assistants_list = self.manager.list_assistants()
        self.assertEqual(len(assistants_list), 2)
        self.assertIn("Nome: assistant1, Modelo: gpt-3.5-turbo", assistants_list)
        self.assertIn("Nome: assistant2, Modelo: gpt-4", assistants_list)

    

    def test_remove_nonexistent_assistant(self):
        with self.assertRaises(ValueError):
            self.manager.remove_assistant("nonexistent_assistant")

if __name__ == '__main__':
    unittest.main()