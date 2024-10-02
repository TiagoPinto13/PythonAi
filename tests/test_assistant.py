import unittest
import tempfile

from unittest.mock import patch, MagicMock
import os
from pythonAI_wrapper.assistant import OpenAIAssistant

class TestOpenAIAssistant(unittest.TestCase):

    def setUp(self):
        self.api_key = "api_key_test"
        self.name = "test_assistant"
        self.model = "gpt-4"
        self.instructions = "Test instructions"
        self.assistant = OpenAIAssistant(self.api_key, "Test Assistant")

    @patch('pythonAI_wrapper.assistant.OpenAI')
    def test_init(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        assistant = OpenAIAssistant(self.api_key, self.name, self.model, self.instructions)

        mock_openai.assert_called_once_with(api_key=self.api_key)
        self.assertEqual(assistant.name, self.name)
        self.assertEqual(assistant.model, self.model)
        self.assertEqual(assistant.instructions, self.instructions)
        self.assertEqual(assistant.client, mock_client)
        mock_client.beta.assistants.create.assert_called_once_with(
            name=self.name,
            instructions=self.instructions,
            model=self.model
        )

    def test_add_context_file(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(b"Test PDF content")

        try:
            self.assistant.add_context_file(temp_file_path)
        finally:
            os.unlink(temp_file_path)

    def test_set_model(self):
        new_model = "gpt-3.5-turbo"
        self.assistant.set_model(new_model)
        self.assertEqual(self.assistant.model, new_model)

    @patch('os.path.exists')
    @patch('openai.OpenAI')
    def test_add_context_file(self, mock_openai, mock_exists):
        mock_exists.return_value = True
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        
        thread_id = "test_thread_id"
        
        self.assistant.add_context_file("test.pdf", thread_id)
        
        self.assertIn("test.pdf", self.assistant.context_files)
        mock_client.files.create.assert_called_once()
        mock_client.beta.assistants.files.create.assert_called_once()

            

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('pythonAI_wrapper.assistant.OpenAIAssistant.add_context_file')
    def test_add_context_folder(self, mock_add_file, mock_listdir, mock_isdir):
        mock_isdir.return_value = True
        mock_listdir.return_value = ["file1.pdf", "file2.txt", "file3.pdf"]

        # Simular thread_id
        thread_id = "test_thread_id"
        
        self.assistant.add_context_folder("/test/folder", thread_id)

        self.assertEqual(mock_add_file.call_count, 2)
        mock_add_file.assert_any_call("/test/folder/file1.pdf", thread_id)
        mock_add_file.assert_any_call("/test/folder/file3.pdf", thread_id)


    def test_start_thread(self):
        self.assistant.start_thread("thread1")
        self.assertIn("thread1", self.assistant.threads)
        
        with self.assertRaises(ValueError):
            self.assistant.start_thread("thread1")

    
    def test_get_thread_history(self):
        self.assistant.start_thread("thread1")
        self.assistant.threads["thread1"] = [{"prompt": "Test", "response": "Response"}]
        
        history = self.assistant.get_thread_history("thread1")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["prompt"], "Test")
        self.assertEqual(history[0]["response"], "Response")
        
        with self.assertRaises(ValueError):
            self.assistant.get_thread_history("non_existent_thread")

    def test_get_name(self):
        self.assertEqual(self.assistant.get_name(), "Test Assistant")

    

if __name__ == '__main__':
    unittest.main()