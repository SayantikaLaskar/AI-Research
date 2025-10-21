#!/usr/bin/env python3
"""
Setup script for Scam Call Dataset project
Installs dependencies and initializes the project
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_requirements():
    """Install required Python packages"""
    logger.info("Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    logger.info("Setting up project directories...")
    
    directories = [
        "audio/raw",
        "audio/processed", 
        "transcripts",
        "diarization",
        "metadata"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    return True

def create_sample_data():
    """Create sample data for testing"""
    logger.info("Creating sample data...")
    
    # Create sample metadata
    sample_metadata = {
        "file_id": "sample_001",
        "filename": "sample_conversation.wav",
        "duration_sec": 120.5,
        "num_speakers": 2,
        "speaker_roles": "scammer|victim",
        "source_type": "simulated",
        "recording_conditions": "Studio recording",
        "language": "hindi",
        "notes": "Sample conversation for testing pipeline"
    }
    
    # Save sample metadata
    metadata_file = Path("metadata") / "sample_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(sample_metadata, f, indent=2, ensure_ascii=False)
    
    # Create sample transcript
    sample_transcript = {
        "file_id": "sample_001",
        "duration": 120.5,
        "num_speakers": 2,
        "speakers": ["SPEAKER_1", "SPEAKER_2"],
        "language": "hindi",
        "segments": [
            {
                "start": 0.0,
                "end": 5.2,
                "speaker": "SPEAKER_1",
                "text": "Hello, main bank se call kar raha hun",
                "duration": 5.2
            },
            {
                "start": 5.3,
                "end": 12.1,
                "speaker": "SPEAKER_2", 
                "text": "Haan, main sun raha hun",
                "duration": 6.8
            }
        ]
    }
    
    transcript_file = Path("transcripts") / "sample_001_combined.json"
    with open(transcript_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(sample_transcript, f, indent=2, ensure_ascii=False)
    
    logger.info("Sample data created")
    return True

def create_gitignore():
    """Create .gitignore file"""
    logger.info("Creating .gitignore file...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Audio files (too large for git)
audio/raw/*.wav
audio/raw/*.mp3
audio/raw/*.m4a
audio/processed/*.wav
audio/processed/*.mp3

# Model files
*.pth
*.pt
*.bin

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    logger.info(".gitignore created")
    return True

def main():
    """Main setup function"""
    logger.info("Setting up Scam Call Dataset project...")
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Run setup steps
    steps = [
        ("Setting up directories", setup_directories),
        ("Installing dependencies", install_requirements),
        ("Creating sample data", create_sample_data),
        ("Creating .gitignore", create_gitignore)
    ]
    
    for step_name, step_func in steps:
        logger.info(f"Step: {step_name}")
        if not step_func():
            logger.error(f"Failed: {step_name}")
            return False
    
    logger.info("Setup completed successfully!")
    logger.info("\nNext steps:")
    logger.info("1. Run 'python main_pipeline.py --help' to see available options")
    logger.info("2. Run 'python main_pipeline.py' to start the full pipeline")
    logger.info("3. Or run individual components as needed")
    
    return True

if __name__ == "__main__":
    main()
