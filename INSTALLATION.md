# Installation Guide

This guide will help you set up the Scam Call Dataset project on your system.

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space minimum
- **GPU**: Optional but recommended for faster processing

### Required Software
- **FFmpeg**: For audio processing
- **Git**: For version control
- **CUDA**: Optional, for GPU acceleration

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd scam_dataset_project
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Or install individually
pip install librosa soundfile pydub
pip install pyannote.audio torch torchaudio
pip install openai-whisper transformers
pip install pandas numpy scipy
pip install yt-dlp requests
```

### 4. Install System Dependencies

#### Windows
```bash
# Install FFmpeg using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

#### macOS
```bash
# Install FFmpeg using Homebrew
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
# Install FFmpeg
sudo apt update
sudo apt install ffmpeg

# Install additional dependencies
sudo apt install libsndfile1-dev
```

### 5. Setup Hugging Face Token

For speaker diarization, you need a Hugging Face token:

1. Go to https://huggingface.co/settings/tokens
2. Create a new token
3. Set environment variable:

```bash
# Windows
set HUGGINGFACE_TOKEN=your_token_here

# macOS/Linux
export HUGGINGFACE_TOKEN=your_token_here
```

### 6. Run Setup Script

```bash
python setup.py
```

## Verification

### Test Installation

```bash
# Test audio processing
python audio_processor.py --help

# Test diarization
python diarization_pipeline.py --help

# Test transcription
python transcription_pipeline.py --help

# Test main pipeline
python main_pipeline.py --help
```

### Check Dependencies

```python
# Test imports
import librosa
import soundfile
import torch
import whisper
from pyannote.audio import Pipeline

print("All dependencies installed successfully!")
```

## Troubleshooting

### Common Issues

#### 1. CUDA Out of Memory
```bash
# Use CPU instead
python main_pipeline.py --device cpu
```

#### 2. FFmpeg Not Found
```bash
# Add FFmpeg to PATH
# Windows: Add FFmpeg bin directory to system PATH
# macOS/Linux: Ensure FFmpeg is in /usr/local/bin or add to PATH
```

#### 3. Pyannote Authentication Error
```bash
# Set Hugging Face token
export HUGGINGFACE_TOKEN=your_token_here

# Or pass token directly
python diarization_pipeline.py --hf-token your_token_here
```

#### 4. Audio Format Issues
```bash
# Install additional audio codecs
pip install ffmpeg-python

# Or use pydub for format conversion
from pydub import AudioSegment
```

### Performance Optimization

#### GPU Acceleration
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Use GPU for processing
python main_pipeline.py --device cuda
```

#### Memory Management
```bash
# Process files in smaller batches
python main_pipeline.py --batch-size 4

# Use smaller models
python transcription_pipeline.py --model tiny
```

## Quick Start

### 1. Basic Setup
```bash
python setup.py
```

### 2. Run Full Pipeline
```bash
python main_pipeline.py
```

### 3. Process Existing Files
```bash
python main_pipeline.py --skip-collection
```

### 4. Individual Components
```bash
# Audio processing
python audio_processor.py --input audio/raw --output audio/processed

# Speaker diarization
python diarization_pipeline.py --input audio/processed --output diarization

# Transcription
python transcription_pipeline.py --input audio/processed --output transcripts
```

## Configuration

### Environment Variables
```bash
# Hugging Face token
export HUGGINGFACE_TOKEN=your_token_here

# CUDA device
export CUDA_VISIBLE_DEVICES=0

# Audio processing
export AUDIO_SAMPLE_RATE=16000
export AUDIO_FORMAT=wav
```

### Configuration Files
Create `config.json`:
```json
{
  "audio": {
    "sample_rate": 16000,
    "format": "wav",
    "channels": 1
  },
  "diarization": {
    "model": "pyannote/speaker-diarization-3.1",
    "min_speakers": 2,
    "max_speakers": 4
  },
  "transcription": {
    "model": "base",
    "language": "auto",
    "device": "auto"
  }
}
```

## Next Steps

1. **Data Collection**: Run the data collection pipeline
2. **Audio Processing**: Process and normalize audio files
3. **Diarization**: Perform speaker diarization
4. **Transcription**: Generate transcripts
5. **Annotation**: Manually annotate speaker roles
6. **Metadata**: Create comprehensive metadata
7. **Quality Control**: Review and validate results

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review error logs
3. Test individual components
4. Contact support with detailed error information

## System Requirements Summary

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.9+ |
| RAM | 8GB | 16GB+ |
| Storage | 10GB | 50GB+ |
| GPU | Optional | CUDA-compatible |
| CPU | 4 cores | 8+ cores |
