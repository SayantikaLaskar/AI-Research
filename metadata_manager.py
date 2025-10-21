#!/usr/bin/env python3
"""
Metadata Management for Scam Call Dataset
Handles creation and management of dataset metadata
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetadataManager:
    """Manages metadata for the scam call dataset"""
    
    def __init__(self, dataset_dir: str = "."):
        self.dataset_dir = Path(dataset_dir)
        self.metadata_file = self.dataset_dir / "metadata" / "dataset_metadata.csv"
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
    def create_metadata_entry(self, 
                            file_id: str,
                            filename: str,
                            duration_sec: float,
                            num_speakers: int,
                            speaker_roles: List[str],
                            source_type: str,
                            recording_conditions: str,
                            language: str,
                            notes: str = "") -> Dict:
        """
        Create a metadata entry for a conversation
        
        Args:
            file_id: Unique identifier for the conversation
            filename: Name of the audio file
            duration_sec: Duration in seconds
            num_speakers: Number of speakers
            speaker_roles: List of speaker roles (scammer, victim)
            source_type: public or simulated
            recording_conditions: Description of recording environment
            language: Primary language of conversation
            notes: Additional notes
            
        Returns:
            Metadata dictionary
        """
        metadata = {
            'file_id': file_id,
            'filename': filename,
            'duration_sec': duration_sec,
            'num_speakers': num_speakers,
            'speaker_roles': '|'.join(speaker_roles),
            'source_type': source_type,
            'recording_conditions': recording_conditions,
            'language': language,
            'notes': notes,
            'created_date': datetime.now().isoformat(),
            'audio_path': f"audio/processed/{filename}",
            'transcript_path': f"transcripts/{file_id}_transcript.json",
            'diarization_path': f"diarization/{file_id}_diarization.json"
        }
        
        return metadata
    
    def add_metadata_entry(self, metadata: Dict):
        """Add a metadata entry to the dataset"""
        # Load existing metadata
        if self.metadata_file.exists():
            df = pd.read_csv(self.metadata_file)
        else:
            df = pd.DataFrame()
        
        # Add new entry
        new_row = pd.DataFrame([metadata])
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Save updated metadata
        df.to_csv(self.metadata_file, index=False)
        logger.info(f"Added metadata for {metadata['file_id']}")
    
    def update_metadata_entry(self, file_id: str, updates: Dict):
        """Update an existing metadata entry"""
        if not self.metadata_file.exists():
            logger.error("No metadata file found")
            return
        
        df = pd.read_csv(self.metadata_file)
        
        # Find and update the entry
        mask = df['file_id'] == file_id
        if mask.any():
            for key, value in updates.items():
                if key in df.columns:
                    df.loc[mask, key] = value
            
            df.to_csv(self.metadata_file, index=False)
            logger.info(f"Updated metadata for {file_id}")
        else:
            logger.error(f"File ID {file_id} not found in metadata")
    
    def get_metadata_summary(self) -> Dict:
        """Get summary statistics of the dataset"""
        if not self.metadata_file.exists():
            return {"error": "No metadata file found"}
        
        df = pd.read_csv(self.metadata_file)
        
        summary = {
            'total_conversations': len(df),
            'total_duration_minutes': df['duration_sec'].sum() / 60,
            'languages': df['language'].value_counts().to_dict(),
            'source_types': df['source_type'].value_counts().to_dict(),
            'speaker_counts': df['num_speakers'].value_counts().to_dict(),
            'average_duration_seconds': df['duration_sec'].mean(),
            'min_duration_seconds': df['duration_sec'].min(),
            'max_duration_seconds': df['duration_sec'].max()
        }
        
        return summary
    
    def create_dataset_readme(self) -> str:
        """Create a comprehensive README for the dataset"""
        summary = self.get_metadata_summary()
        
        readme_content = f"""# Scam Call Dataset

## Dataset Overview

This dataset contains {summary.get('total_conversations', 0)} conversations of scam-related voice calls in Hindi, Hinglish, and English languages.

### Key Statistics:
- **Total Conversations**: {summary.get('total_conversations', 0)}
- **Total Duration**: {summary.get('total_duration_minutes', 0):.1f} minutes
- **Average Duration**: {summary.get('average_duration_seconds', 0):.1f} seconds
- **Languages**: {', '.join(summary.get('languages', {}).keys())}
- **Source Types**: {', '.join(summary.get('source_types', {}).keys())}

## Dataset Structure

```
scam_dataset_project/
├── audio/
│   ├── raw/                    # Original audio files
│   └── processed/              # Normalized audio files (16kHz WAV)
├── transcripts/                # Time-aligned transcripts with speaker labels
├── diarization/               # Speaker diarization results
├── metadata/                  # Dataset metadata and statistics
└── README.md                  # This file
```

## File Formats

### Audio Files
- **Format**: WAV
- **Sample Rate**: 16 kHz
- **Channels**: Mono
- **Bit Depth**: 16-bit

### Transcript Files
Each transcript file contains:
- Time-aligned segments with speaker labels
- Speaker roles (scammer/victim)
- Text content with timestamps
- Language identification

### Diarization Files
Speaker diarization results with:
- Speaker segments with timestamps
- Speaker identification
- Segment durations

### Metadata
CSV file containing:
- `file_id`: Unique conversation identifier
- `filename`: Audio filename
- `duration_sec`: Duration in seconds
- `num_speakers`: Number of speakers
- `speaker_roles`: Speaker roles (scammer|victim)
- `source_type`: Data source (public/simulated)
- `recording_conditions`: Recording environment
- `language`: Primary language
- `notes`: Additional information

## Tools Used

### Audio Processing
- **librosa**: Audio loading and preprocessing
- **soundfile**: Audio file I/O
- **pydub**: Audio format conversion

### Speaker Diarization
- **pyannote.audio**: Speaker diarization pipeline
- **torch**: Deep learning framework

### Speech Recognition
- **OpenAI Whisper**: Automatic speech recognition
- **transformers**: Model loading and inference

### Data Processing
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations

## Usage

### Loading Audio
```python
import librosa
audio, sr = librosa.load('audio/processed/conv_001.wav', sr=16000)
```

### Loading Transcript
```python
import json
with open('transcripts/conv_001_transcript.json', 'r') as f:
    transcript = json.load(f)
```

### Loading Metadata
```python
import pandas as pd
metadata = pd.read_csv('metadata/dataset_metadata.csv')
```

## Quality Control

All transcripts have been manually reviewed for:
- Speaker attribution accuracy
- Transcription fidelity
- Role annotation correctness
- Language identification

## Ethical Considerations

- All conversations are either publicly available or simulated
- No personal information is included
- Conversations are used for research purposes only
- Proper attribution is maintained for public sources

## Citation

If you use this dataset in your research, please cite:

```
Scam Call Dataset (2024)
AI Research Intern Assignment
[Include your name and institution]
```

## License

This dataset is provided for research purposes only. Please ensure compliance with local laws and regulations when using this data.

## Contact

For questions about this dataset, please contact [your email].

---
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return readme_content
    
    def save_readme(self):
        """Save the README to file"""
        readme_content = self.create_dataset_readme()
        readme_file = self.dataset_dir / "README.md"
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        logger.info(f"README saved to {readme_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage dataset metadata")
    parser.add_argument("--create-readme", action="store_true", help="Create README.md")
    parser.add_argument("--summary", action="store_true", help="Show dataset summary")
    parser.add_argument("--dataset-dir", default=".", help="Dataset directory")
    
    args = parser.parse_args()
    
    manager = MetadataManager(args.dataset_dir)
    
    if args.summary:
        summary = manager.get_metadata_summary()
        print(json.dumps(summary, indent=2))
    
    if args.create_readme:
        manager.save_readme()

if __name__ == "__main__":
    main()
