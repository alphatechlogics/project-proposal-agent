# AI Document Generation System

An intelligent system that processes business requirement documents and generates comprehensive technical documentation using AI-powered analysis.

> Live @streamlit [PPA](https://project-proposal-agent-demo1.streamlit.app/)

## Features

- Document processing support for multiple formats (PDF, DOCX, TXT)
- AI-powered analysis using Groq LLM:
  - Requirements analysis
  - Technical specifications generation
  - Architecture recommendations
- Automated project planning and task breakdown
- Detailed cost estimation including:
  - Labor costs with complexity factors
  - Infrastructure costs
  - License costs
- Interactive web interface using Streamlit
- JSON-formatted outputs for all analyses
- Downloadable consolidated reports

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file in the project root:
   ```plaintext
   GROQ_API_KEY=your_api_key
   ```

## Usage

1. Start the web interface:
   ```bash
   streamlit run app.py
   ```
2. Upload your business requirements document
3. The system will automatically:
   - Process the document
   - Analyze requirements
   - Generate technical specifications
   - Suggest architecture
   - Create project plan
   - Calculate cost estimates
4. View results in different tabs
5. Download the complete analysis report

## Project Structure

```plaintext
.
├── app.py                    # Main Streamlit application
├── document_processor.py     # Document parsing and processing
├── ai_analysis.py           # AI-powered analysis pipeline
├── project_planner.py       # Project planning logic
├── cost_estimator.py        # Cost estimation engine
├── document_generator.py     # Final document generation
├── groq_client.py           # Groq API integration
└── config.py                # Configuration management
```

## Input Document Support

Supported formats:
- PDF (.pdf)
- Microsoft Word (.docx)
- Text files (.txt)

## Output Format

The system generates a comprehensive report including:
- Analyzed requirements
- Technical specifications
- Suggested architecture
- Project timeline and tasks
- Detailed cost breakdown

### Cost Estimate Format
```json
{
    "status": "success",
    "cost_breakdown": {
        "labor_costs": {
            "amount": 0.00,
            "currency": "USD"
        },
        "infrastructure_costs": {
            "amount": 0.00,
            "currency": "USD"
        },
        "license_costs": {
            "amount": 0.00,
            "currency": "USD"
        },
        "total_cost": {
            "amount": 0.00,
            "currency": "USD"
        }
    }
}
```

## Requirements

- Python 3.8 or higher
- Groq API key
- Required Python packages (see requirements.txt)

## Error Handling

The system includes comprehensive error handling for:
- Invalid document formats
- API failures
- Processing errors
- Invalid input data

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
```

This updated README.md provides:
- Accurate project name and description
- Complete feature list
- Correct setup instructions
- Detailed project structure
- Input/Output format specifications
- Error handling information
- Clear usage instructions for the Streamlit interface
