#!/usr/bin/env python3
"""
Speaker Diarization Pipeline for Scam Call Dataset
Uses pyannote.audio for speaker diarization
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import torch
from pyannote.audio import Pipeline
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiarizationPipeline:
    """Handles speaker diarization for scam call conversations"""
    
    def __init__(self, hf_token: str = None):
        """
        Initialize diarization pipeline
        
        Args:
            hf_token: Hugging Face token for accessing pyannote models
        """
        self.hf_token = hf_token
        self.pipeline = None
        self._load_pipeline()
    
    def _load_pipeline(self):
        """Load the pyannote diarization pipeline"""
        try:
            # Use the pre-trained model from Hugging Face
            self.pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.hf_token
            )
            logger.info("Diarization pipeline loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load diarization pipeline: {str(e)}")
            raise
    
    def diarize_audio(self, audio_path: str) -> Dict:
        """
        Perform speaker diarization on audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dict containing diarization results
        """
        try:
            # Run diarization
            diarization = self.pipeline(audio_path)
            
            # Convert to list of segments
            segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                segments.append({
                    "start": turn.start,
                    "end": turn.end,
                    "speaker": speaker,
                    "duration": turn.end - turn.start
                })
            
            # Get unique speakers
            speakers = list(set([seg["speaker"] for seg in segments]))
            
            result = {
                "audio_path": audio_path,
                "num_speakers": len(speakers),
                "speakers": speakers,
                "segments": segments,
                "total_duration": max([seg["end"] for seg in segments]) if segments else 0
            }
            
            logger.info(f"Diarized {audio_path}: {len(speakers)} speakers, {len(segments)} segments")
            return result
            
        except Exception as e:
            logger.error(f"Error diarizing {audio_path}: {str(e)}")
            return None
    
    def save_diarization(self, diarization_result: Dict, output_path: str):
        """Save diarization results to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(diarization_result, f, indent=2)
        logger.info(f"Diarization saved to {output_path}")
    
    def batch_diarize(self, input_dir: str, output_dir: str) -> List[Dict]:
        """
        Perform diarization on all audio files in directory
        
        Args:
            input_dir: Directory containing audio files
            output_dir: Directory to save diarization results
            
        Returns:
            List of diarization results
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        audio_extensions = ['.wav', '.mp3', '.m4a', '.flac']
        
        for file_path in input_path.iterdir():
            if file_path.suffix.lower() in audio_extensions:
                logger.info(f"Processing {file_path.name}")
                
                # Perform diarization
                result = self.diarize_audio(str(file_path))
                
                if result:
                    # Save individual diarization file
                    output_file = output_path / f"{file_path.stem}_diarization.json"
                    self.save_diarization(result, str(output_file))
                    results.append(result)
        
        # Save batch summary
        batch_summary = {
            "total_files": len(results),
            "successful_diarizations": len(results),
            "results": results
        }
        
        with open(output_path / "batch_diarization_summary.json", "w") as f:
            json.dump(batch_summary, f, indent=2)
        
        logger.info(f"Batch diarization completed: {len(results)} files processed")
        return results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Perform speaker diarization on audio files")
    parser.add_argument("--input", required=True, help="Input directory with audio files")
    parser.add_argument("--output", required=True, help="Output directory for diarization results")
    parser.add_argument("--hf-token", help="Hugging Face token for model access")
    
    args = parser.parse_args()
    
    pipeline = DiarizationPipeline(hf_token=args.hf_token)
    pipeline.batch_diarize(args.input, args.output)

if __name__ == "__main__":
    main()
