# Scam Call Dataset Project

A comprehensive dataset of scam-related voice call conversations in Hindi, Hinglish, and English languages, complete with speaker diarization and time-aligned transcripts.

## Project Overview

This project creates a dataset for AI research on scam call detection and analysis. The dataset includes:

- **Audio recordings** in multiple languages (Hindi, Hinglish, English)
- **Speaker diarization** to identify who spoke when
- **Time-aligned transcripts** with speaker attribution
- **Role annotation** (scammer vs victim)
- **Comprehensive metadata** for each conversation

## Dataset Structure

```
scam_dataset_project/
├── audio/
│   ├── raw/                    # Original audio files
│   └── processed/              # Normalized audio files (16kHz WAV)
├── transcripts/                # Time-aligned transcripts with speaker labels
├── diarization/               # Speaker diarization results
├── metadata/                  # Dataset metadata and statistics
├── requirements.txt           # Python dependencies
├── setup.py                   # Project setup script
├── main_pipeline.py          # Main processing pipeline
├── audio_processor.py        # Audio preprocessing
├── diarization_pipeline.py   # Speaker diarization
├── transcription_pipeline.py # Speech recognition
├── metadata_manager.py       # Metadata management
├── data_collector.py         # Data collection utilities
└── README.md                 # This file
```

## Quick Start

### 1. Setup

```bash
# Install dependencies and setup project
python setup.py

# Or manually install dependencies
pip install -r requirements.txt
```

### 2. Run the Pipeline

```bash
# Run full pipeline (data collection + processing)
python main_pipeline.py

# Skip data collection and process existing files
python main_pipeline.py --skip-collection

# Skip YouTube data collection
python main_pipeline.py --skip-youtube

# Specify language for transcription
python main_pipeline.py --language hi
```

### 3. Individual Components

```bash
# Audio processing only
python audio_processor.py --input audio/raw --output audio/processed

# Speaker diarization only
python diarization_pipeline.py --input audio/processed --output diarization

# Transcription only
python transcription_pipeline.py --input audio/processed --output transcripts

# Create metadata
python metadata_manager.py --create-readme
```

## Data Collection

### Sources

1. **YouTube Videos**: Scam call recordings from public sources
2. **Simulated Conversations**: Scripted scenarios for controlled data
3. **Public Datasets**: Existing research datasets (if available)

### Search Keywords

- Hindi: "scam call hindi", "fraud call recording", "phone scam india"
- English: "scam call english", "fraud call center", "phone scam recording"
- Hinglish: "scam call hinglish", "fraud call india"

## Processing Pipeline

### Phase 1: Data Collection
- Search and download from YouTube
- Create simulated scenarios
- Collect from public datasets

### Phase 2: Audio Processing
- Normalize audio to 16kHz WAV
- Remove noise and enhance quality
- Standardize format across all files

### Phase 3: Speaker Diarization
- Identify speaker segments using pyannote.audio
- Assign speaker labels (SPEAKER_1, SPEAKER_2, etc.)
- Generate time-aligned speaker boundaries

### Phase 4: Speech Recognition
- Transcribe audio using OpenAI Whisper
- Generate word-level timestamps
- Support multiple languages (Hindi, English, Hinglish)

### Phase 5: Result Combination
- Merge diarization and transcription results
- Create speaker-attributed transcripts
- Align speaker segments with text content

### Phase 6: Role Annotation
- Manually annotate speaker roles (scammer/victim)
- Review and validate transcriptions
- Ensure accuracy and completeness

### Phase 7: Metadata Creation
- Generate comprehensive metadata CSV
- Include file information, durations, languages
- Create dataset statistics and summaries

## File Formats

### Audio Files
- **Format**: WAV
- **Sample Rate**: 16 kHz
- **Channels**: Mono
- **Bit Depth**: 16-bit

### Transcript Files (JSON)
```json
{
  "file_id": "conv_001",
  "duration": 210.3,
  "num_speakers": 2,
  "speakers": ["SPEAKER_1", "SPEAKER_2"],
  "language": "hindi",
  "segments": [
    {
      "start": 0.12,
      "end": 3.30,
      "speaker": "SPEAKER_1",
      "text": "Hello?",
      "duration": 3.18
    },
    {
      "start": 3.31,
      "end": 10.10,
      "speaker": "SPEAKER_2",
      "text": "Ye bank fraud department se baat kar rahe hain...",
      "duration": 6.79
    }
  ]
}
```

### Metadata CSV
```csv
file_id,filename,duration_sec,num_speakers,speaker_roles,source_type,recording_conditions,language,notes
conv_001,sample.wav,210.3,2,scammer|victim,public,Studio,hi,Sample conversation
```

## Tools and Technologies

### Audio Processing
- **librosa**: Audio loading and preprocessing
- **soundfile**: Audio file I/O
- **pydub**: Audio format conversion

### Speaker Diarization
- **pyannote.audio**: State-of-the-art diarization
- **torch**: Deep learning framework
- **Hugging Face**: Model hosting and access

### Speech Recognition
- **OpenAI Whisper**: Multilingual ASR
- **transformers**: Model loading and inference
- **torch**: GPU acceleration

### Data Processing
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **json**: Data serialization

## Quality Control

### Automatic Checks
- Audio quality validation
- Speaker diarization accuracy
- Transcription confidence scores
- Language detection accuracy

### Manual Review
- Speaker role annotation
- Transcript accuracy verification
- Language identification validation
- Overall conversation quality

## Ethical Considerations

- **Privacy**: No personal information included
- **Consent**: All data from public sources or simulated
- **Anonymization**: Speaker identities protected
- **Research Use**: Dataset for academic research only

## Usage Examples

### Loading Audio
```python
import librosa
audio, sr = librosa.load('audio/processed/conv_001.wav', sr=16000)
```

### Loading Transcript
```python
import json
with open('transcripts/conv_001_combined.json', 'r', encoding='utf-8') as f:
    transcript = json.load(f)
    
for segment in transcript['segments']:
    print(f"{segment['start']:.2f}s - {segment['end']:.2f}s: {segment['speaker']}")
    print(f"Text: {segment['text']}")
```

### Loading Metadata
```python
import pandas as pd
metadata = pd.read_csv('metadata/dataset_metadata.csv')
print(metadata.head())
```

## Troubleshooting

### Common Issues

1. **Hugging Face Token**: Required for pyannote.audio
   ```bash
   export HUGGINGFACE_TOKEN="your_token_here"
   ```

2. **CUDA Out of Memory**: Use CPU for processing
   ```bash
   python main_pipeline.py --device cpu
   ```

3. **Audio Format Issues**: Ensure FFmpeg is installed
   ```bash
   # Windows
   choco install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Ubuntu
   sudo apt install ffmpeg
   ```

### Performance Tips

- Use GPU for faster processing
- Process files in batches
- Monitor disk space for large datasets
- Use appropriate model sizes for your hardware

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for research purposes only. Please ensure compliance with local laws and regulations.

## Contact

For questions or issues, please contact [your email].

---

**Note**: This is a research dataset. Ensure proper attribution and ethical use of the data.
