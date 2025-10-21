#!/usr/bin/env python3
"""
Transcription Pipeline for Scam Call Dataset
Uses OpenAI Whisper for speech recognition with speaker attribution
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import whisper
import torch
import pandas as pd
from datetime import timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranscriptionPipeline:
    """Handles transcription with speaker attribution for scam call conversations"""
    
    def __init__(self, model_size: str = "base", device: str = "auto"):
        """
        Initialize transcription pipeline
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: Device to use (auto, cpu, cuda)
        """
        self.model_size = model_size
        self.device = device
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model"""
        try:
            if self.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            self.model = whisper.load_model(self.model_size, device=self.device)
            logger.info(f"Whisper model loaded: {self.model_size} on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise
    
    def transcribe_with_timestamps(self, audio_path: str, language: str = None) -> Dict:
        """
        Transcribe audio with word-level timestamps
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'hi', 'en', 'auto')
            
        Returns:
            Dict containing transcription results
        """
        try:
            # Transcribe with word timestamps
            result = self.model.transcribe(
                audio_path,
                language=language,
                word_timestamps=True,
                verbose=False
            )
            
            # Extract segments with timestamps
            segments = []
            for segment in result["segments"]:
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "words": segment.get("words", [])
                })
            
            transcription_result = {
                "audio_path": audio_path,
                "language": result.get("language", "unknown"),
                "duration": result.get("duration", 0),
                "text": result["text"],
                "segments": segments,
                "language_probability": result.get("language_probability", 0)
            }
            
            logger.info(f"Transcribed {audio_path}: {len(segments)} segments")
            return transcription_result
            
        except Exception as e:
            logger.error(f"Error transcribing {audio_path}: {str(e)}")
            return None
    
    def combine_diarization_transcription(self, diarization_path: str, transcription_path: str) -> Dict:
        """
        Combine diarization and transcription results
        
        Args:
            diarization_path: Path to diarization JSON file
            transcription_path: Path to transcription JSON file
            
        Returns:
            Combined result with speaker-attributed transcripts
        """
        try:
            # Load diarization results
            with open(diarization_path, 'r') as f:
                diarization = json.load(f)
            
            # Load transcription results
            with open(transcription_path, 'r') as f:
                transcription = json.load(f)
            
            # Combine results
            combined_segments = []
            
            for diar_seg in diarization["segments"]:
                # Find overlapping transcription segments
                overlapping_text = []
                for trans_seg in transcription["segments"]:
                    # Check for overlap
                    if (trans_seg["start"] < diar_seg["end"] and 
                        trans_seg["end"] > diar_seg["start"]):
                        
                        # Calculate overlap
                        overlap_start = max(trans_seg["start"], diar_seg["start"])
                        overlap_end = min(trans_seg["end"], diar_seg["end"])
                        overlap_duration = overlap_end - overlap_start
                        
                        if overlap_duration > 0:
                            overlapping_text.append({
                                "text": trans_seg["text"],
                                "start": overlap_start,
                                "end": overlap_end,
                                "overlap_duration": overlap_duration
                            })
                
                # Combine overlapping text
                combined_text = " ".join([seg["text"] for seg in overlapping_text])
                
                combined_segments.append({
                    "start": diar_seg["start"],
                    "end": diar_seg["end"],
                    "speaker": diar_seg["speaker"],
                    "text": combined_text.strip(),
                    "duration": diar_seg["duration"]
                })
            
            combined_result = {
                "file_id": Path(diarization_path).stem.replace("_diarization", ""),
                "duration": diarization["total_duration"],
                "num_speakers": diarization["num_speakers"],
                "speakers": diarization["speakers"],
                "language": transcription["language"],
                "segments": combined_segments
            }
            
            logger.info(f"Combined diarization and transcription for {combined_result['file_id']}")
            return combined_result
            
        except Exception as e:
            logger.error(f"Error combining results: {str(e)}")
            return None
    
    def save_transcript(self, transcript_result: Dict, output_path: str):
        """Save transcript to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transcript_result, f, indent=2, ensure_ascii=False)
        logger.info(f"Transcript saved to {output_path}")
    
    def batch_transcribe(self, input_dir: str, output_dir: str, language: str = None) -> List[Dict]:
        """
        Transcribe all audio files in directory
        
        Args:
            input_dir: Directory containing audio files
            output_dir: Directory to save transcription results
            language: Language code for transcription
            
        Returns:
            List of transcription results
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        audio_extensions = ['.wav', '.mp3', '.m4a', '.flac']
        
        for file_path in input_path.iterdir():
            if file_path.suffix.lower() in audio_extensions:
                logger.info(f"Transcribing {file_path.name}")
                
                # Perform transcription
                result = self.transcribe_with_timestamps(str(file_path), language)
                
                if result:
                    # Save individual transcript file
                    output_file = output_path / f"{file_path.stem}_transcript.json"
                    self.save_transcript(result, str(output_file))
                    results.append(result)
        
        # Save batch summary
        batch_summary = {
            "total_files": len(results),
            "successful_transcriptions": len(results),
            "language": language,
            "results": results
        }
        
        with open(output_path / "batch_transcription_summary.json", "w") as f:
            json.dump(batch_summary, f, indent=2)
        
        logger.info(f"Batch transcription completed: {len(results)} files processed")
        return results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcribe audio files with timestamps")
    parser.add_argument("--input", required=True, help="Input directory with audio files")
    parser.add_argument("--output", required=True, help="Output directory for transcription results")
    parser.add_argument("--model", default="base", help="Whisper model size")
    parser.add_argument("--language", help="Language code for transcription")
    
    args = parser.parse_args()
    
    pipeline = TranscriptionPipeline(model_size=args.model)
    pipeline.batch_transcribe(args.input, args.output, args.language)

if __name__ == "__main__":
    main()
