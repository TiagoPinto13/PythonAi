# setup.py
from setuptools import setup, find_packages

setup(
    name='Python',
    version='1.0.0',
    description='Uma biblioteca Python para gerenciar interações com o OpenAI com suporte a PDFs e threads de conversação.',
    author='Tiago Pinto',
    author_email='tiago.daniel.s.pinto23@gmail.com',
    url='https://github.com/TiagoPinto13/PythonAi', 
    packages=find_packages(),
    install_requires=[
        'openai',
        'PyPDF2',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'openai-cli=PythonAi.cli_tool:main',  # Registra a ferramenta CLI
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Define a versão mínima do Python
)
