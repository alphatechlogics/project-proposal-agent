# Document Automation System

A Python-based system for automating document processing using LLMs.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   make install
   ```
4. Copy `.env.example` to `.env` and configure your environment variables:
   ```bash
   cp .env.example .env
   ```

## Usage

1. Place your input documents in the `input` directory
2. Run the processor:
   ```bash
   python -m src.main
   ```
3. Find processed output in the `output` directory

## Development

- Run tests: `make test`
- Format code: `make format`
- Check code: `make lint`
- Clean build files: `make clean`

## License

MIT
