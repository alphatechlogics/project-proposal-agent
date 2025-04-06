# Document Automation System

An AI-powered system for automating document generation from client requirements using Groq models.

## Features

- Automated document processing
- AI-powered content generation using Groq models
- Project plan generation
- Cost estimation automation
- Document format conversion (DOCX and XLSX)
- Comprehensive logging
- Error handling and recovery

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/document-automation.git
cd document-automation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Groq API key and other settings
```

## Usage

### Command Line Interface

1. Place your client documents in the `data/input/` directory

2. Run the automation:
```bash
document-automation
```

The system will:
- Process all .docx files in the input directory
- Generate project plans and cost estimates
- Save the generated documents in the `data/output/` directory

### Python API

```python
from src.agents.document_agent import DocumentAgent
from src.processors.document_processor import DocumentProcessor

# Initialize components
agent = DocumentAgent()
processor = DocumentProcessor()

# Process a document
requirements = processor.process_input_file("path/to/document.docx")
project_plan = agent.generate_project_plan(requirements)
estimates = agent.generate_estimates(requirements)
```

## Project Structure

```
.
├── src/
│   ├── agents/         # AI agent implementations
│   ├── processors/     # Document processing modules
│   ├── utils/         # Utility functions
│   └── config/        # Configuration files
├── tests/             # Test files
├── docs/              # Project documentation
├── data/
│   ├── input/         # Input documents
│   └── output/        # Generated documents
├── logs/              # Application logs
└── setup.py          # Package installation
```

## Configuration

The system can be configured through environment variables in the `.env` file:

- `GROQ_API_KEY`: Your Groq API key
- `GROQ_MODEL`: The Groq model to use (default: "mixtral-8x7b-32768")
- `LOG_LEVEL`: Logging level (default: "INFO")
- `TEMPERATURE`: AI model temperature (default: 0.7)
- `MAX_TOKENS`: Maximum tokens for AI responses (default: 2000)

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
isort .
```

4. Type checking:
```bash
mypy .
```

## License

MIT License - see LICENSE file for details
