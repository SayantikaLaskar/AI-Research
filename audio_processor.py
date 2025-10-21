#!/usr/bin/env python3
"""
Audio Processing Pipeline for Scam Call Dataset
Handles audio normalization, format conversion, and preprocessing
"""

import os
import librosa
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize
import argparse
from pathlib import Path
import json
from typing import Dict, List, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessor:
    """Handles audio preprocessing for the scam call dataset"""
    
    def __init__(self, target_sr: int = 16000, target_format: str = "wav"):
        self.target_sr = target_sr
        self.target_format = target_format
        
    def normalize_audio(self, audio_path: str, output_path: str) -> Dict:
        """
        Normalize and convert audio to target format and sample rate
        
        Args:
            audio_path: Path to input audio file
            output_path: Path to save processed audio
            
        Returns:
            Dict with processing metadata
        """
        try:
            # Load audio with librosa
            audio, sr = librosa.load(audio_path, sr=self.target_sr)
            
            # Normalize audio
            audio_normalized = librosa.util.normalize(audio)
            
            # Save as WAV
            sf.write(output_path, audio_normalized, self.target_sr)
            
            # Get duration
            duration = len(audio_normalized) / self.target_sr
            
            metadata = {
                "original_path": audio_path,
                "processed_path": output_path,
                "duration_seconds": duration,
                "sample_rate": self.target_sr,
                "format": self.target_format,
                "channels": 1,  # Mono
                "normalized": True
            }
            
            logger.info(f"Processed {audio_path} -> {output_path} ({duration:.2f}s)")
            return metadata
            
        except Exception as e:
            logger.error(f"Error processing {audio_path}: {str(e)}")
            return None
    
    def batch_process(self, input_dir: str, output_dir: str) -> List[Dict]:
        """
        Process all audio files in a directory
        
        Args:
            input_dir: Directory containing raw audio files
            output_dir: Directory to save processed files
            
        Returns:
            List of metadata for all processed files
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        metadata_list = []
        supported_formats = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
        
        for file_path in input_path.iterdir():
            if file_path.suffix.lower() in supported_formats:
                output_file = output_path / f"{file_path.stem}.{self.target_format}"
                metadata = self.normalize_audio(str(file_path), str(output_file))
                
                if metadata:
                    metadata_list.append(metadata)
        
        # Save batch metadata
        batch_metadata = {
            "total_files": len(metadata_list),
            "processed_files": len([m for m in metadata_list if m]),
            "target_sample_rate": self.target_sr,
            "target_format": self.target_format,
            "files": metadata_list
        }
        
        with open(output_path / "batch_metadata.json", "w") as f:
            json.dump(batch_metadata, f, indent=2)
        
        logger.info(f"Batch processed {len(metadata_list)} files")
        return metadata_list

def main():
    parser = argparse.ArgumentParser(description="Process audio files for scam call dataset")
    parser.add_argument("--input", required=True, help="Input directory with raw audio")
    parser.add_argument("--output", required=True, help="Output directory for processed audio")
    parser.add_argument("--sample-rate", type=int, default=16000, help="Target sample rate")
    
    args = parser.parse_args()
    
    processor = AudioProcessor(target_sr=args.sample_rate)
    processor.batch_process(args.input, args.output)

if __name__ == "__main__":
    main()
