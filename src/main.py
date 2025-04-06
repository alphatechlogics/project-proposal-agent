import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agents.document_agent import DocumentAgent
from src.processors.document_processor import DocumentProcessor
from src.config.settings import settings
from src.utils.logger import logger

def main():
    """Main entry point for the document automation system."""
    try:
        # Initialize components
        agent = DocumentAgent()
        processor = DocumentProcessor()
        
        # Process input files
        for input_file in settings.INPUT_DIR.glob("*.docx"):
            logger.info(f"Processing file: {input_file}")
            
            # Read requirements
            requirements = processor.process_input_file(input_file)
            if not requirements:
                logger.error(f"Failed to process {input_file}")
                continue
            
            try:
                # Generate documents
                logger.info("Generating project plan...")
                project_plan = agent.generate_project_plan(requirements)
                
                logger.info("Generating cost estimates...")
                estimates = agent.generate_estimates(requirements)
                
                # Save outputs
                output_base = settings.OUTPUT_DIR / input_file.stem
                processor.write_docx(
                    project_plan["content"],
                    output_base.with_name(f"{input_file.stem}_project_plan.docx")
                )
                processor.write_excel(
                    estimates["content"],
                    output_base.with_name(f"{input_file.stem}_estimates.xlsx")
                )
                
                logger.success(f"Successfully processed {input_file}")
            except Exception as e:
                logger.error(f"Error processing {input_file}: {str(e)}")
                continue
        
        logger.info("Document processing completed")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()