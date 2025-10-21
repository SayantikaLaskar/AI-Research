#!/usr/bin/env python3
"""
Working Auto Collector - No Heavy Dependencies
Works with Python 3.14 and minimal packages
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
import subprocess
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkingAutoCollector:
    """Auto collector that works without heavy dependencies"""
    
    def __init__(self, output_dir: str = "audio/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_sample_audio_files(self):
        """Create sample audio files for testing"""
        logger.info("Creating sample audio files...")
        
        # Create sample audio files (empty for now, but with proper structure)
        sample_files = [
            "hindi_bank_fraud_001.wav",
            "hindi_investment_001.wav", 
            "hinglish_tech_support_001.wav",
            "hinglish_bank_fraud_001.wav",
            "english_lottery_001.wav",
            "english_tech_support_001.wav"
        ]
        
        for filename in sample_files:
            filepath = self.output_dir / filename
            # Create empty file as placeholder
            with open(filepath, 'w') as f:
                f.write("# Placeholder audio file\n")
            logger.info(f"Created placeholder: {filename}")
        
        return sample_files
    
    def create_sample_transcripts(self):
        """Create sample transcript files"""
        logger.info("Creating sample transcript files...")
        
        transcript_dir = Path("transcripts")
        transcript_dir.mkdir(exist_ok=True)
        
        # Load sample conversations
        with open("sample_conversations.json", "r", encoding="utf-8") as f:
            conversations = json.load(f)
        
        for conv in conversations["conversations"]:
            # Create transcript structure
            transcript = {
                "file_id": conv["id"],
                "duration": conv["duration_estimate"],
                "num_speakers": 2,
                "speakers": ["SPEAKER_1", "SPEAKER_2"],
                "language": conv["language"],
                "segments": []
            }
            
            # Convert script to segments
            for i, line in enumerate(conv["script"]):
                start_time = line["start_time"]
                end_time = line["end_time"]
                speaker = "SPEAKER_1" if line["speaker"] == "scammer" else "SPEAKER_2"
                
                segment = {
                    "start": start_time,
                    "end": end_time,
                    "speaker": speaker,
                    "text": line["text"],
                    "duration": end_time - start_time,
                    "role": line["speaker"]  # Add role information
                }
                transcript["segments"].append(segment)
            
            # Save transcript
            transcript_file = transcript_dir / f"{conv['id']}_combined.json"
            with open(transcript_file, "w", encoding="utf-8") as f:
                json.dump(transcript, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Created transcript: {transcript_file.name}")
    
    def create_sample_metadata(self):
        """Create sample metadata"""
        logger.info("Creating sample metadata...")
        
        metadata_dir = Path("metadata")
        metadata_dir.mkdir(exist_ok=True)
        
        # Load sample conversations
        with open("sample_conversations.json", "r", encoding="utf-8") as f:
            conversations = json.load(f)
        
        metadata_entries = []
        
        for conv in conversations["conversations"]:
            entry = {
                "file_id": conv["id"],
                "filename": f"{conv['id']}.wav",
                "duration_sec": conv["duration_estimate"],
                "num_speakers": 2,
                "speaker_roles": "scammer|victim",
                "source_type": "simulated",
                "recording_conditions": "Sample conversation for demonstration",
                "language": conv["language"],
                "notes": "Generated sample for testing pipeline",
                "created_date": datetime.now().isoformat(),
                "audio_path": f"audio/processed/{conv['id']}.wav",
                "transcript_path": f"transcripts/{conv['id']}_combined.json",
                "diarization_path": f"diarization/{conv['id']}_diarization.json"
            }
            metadata_entries.append(entry)
        
        # Save metadata CSV
        import pandas as pd
        df = pd.DataFrame(metadata_entries)
        metadata_file = metadata_dir / "dataset_metadata.csv"
        df.to_csv(metadata_file, index=False)
        
        logger.info(f"Created metadata: {metadata_file}")
    
    def create_sample_diarization(self):
        """Create sample diarization files"""
        logger.info("Creating sample diarization files...")
        
        diarization_dir = Path("diarization")
        diarization_dir.mkdir(exist_ok=True)
        
        # Load sample conversations
        with open("sample_conversations.json", "r", encoding="utf-8") as f:
            conversations = json.load(f)
        
        for conv in conversations["conversations"]:
            # Create diarization structure
            diarization = {
                "audio_path": f"audio/processed/{conv['id']}.wav",
                "num_speakers": 2,
                "speakers": ["SPEAKER_1", "SPEAKER_2"],
                "total_duration": conv["duration_estimate"],
                "segments": []
            }
            
            # Create segments based on script
            for i, line in enumerate(conv["script"]):
                start_time = line["start_time"]
                end_time = line["end_time"]
                speaker = "SPEAKER_1" if line["speaker"] == "scammer" else "SPEAKER_2"
                
                segment = {
                    "start": start_time,
                    "end": end_time,
                    "speaker": speaker,
                    "duration": end_time - start_time
                }
                diarization["segments"].append(segment)
            
            # Save diarization
            diarization_file = diarization_dir / f"{conv['id']}_diarization.json"
            with open(diarization_file, "w", encoding="utf-8") as f:
                json.dump(diarization, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Created diarization: {diarization_file.name}")
    
    def create_sample_processed_audio(self):
        """Create sample processed audio files"""
        logger.info("Creating sample processed audio files...")
        
        processed_dir = Path("audio/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Load sample conversations
        with open("sample_conversations.json", "r", encoding="utf-8") as f:
            conversations = json.load(f)
        
        for conv in conversations["conversations"]:
            # Create placeholder processed audio file
            processed_file = processed_dir / f"{conv['id']}.wav"
            with open(processed_file, 'w') as f:
                f.write("# Processed audio file placeholder\n")
            logger.info(f"Created processed audio: {processed_file.name}")
    
    def run_complete_sample_creation(self):
        """Create complete sample dataset"""
        logger.info("=== Creating Complete Sample Dataset ===")
        
        try:
            # Create all sample files
            self.create_sample_audio_files()
            self.create_sample_processed_audio()
            self.create_sample_diarization()
            self.create_sample_transcripts()
            self.create_sample_metadata()
            
            logger.info("=== Sample Dataset Creation Completed ===")
            logger.info("✅ All sample files created successfully!")
            
            # Show summary
            self.show_dataset_summary()
            
        except Exception as e:
            logger.error(f"Sample creation failed: {str(e)}")
            return False
        
        return True
    
    def show_dataset_summary(self):
        """Show summary of created dataset"""
        logger.info("\n=== Dataset Summary ===")
        
        # Count files
        audio_files = len(list(Path("audio/raw").glob("*.wav")))
        processed_files = len(list(Path("audio/processed").glob("*.wav")))
        transcript_files = len(list(Path("transcripts").glob("*.json")))
        diarization_files = len(list(Path("diarization").glob("*.json")))
        
        logger.info(f"📁 Audio files (raw): {audio_files}")
        logger.info(f"📁 Audio files (processed): {processed_files}")
        logger.info(f"📁 Transcript files: {transcript_files}")
        logger.info(f"📁 Diarization files: {diarization_files}")
        
        # Show languages
        with open("sample_conversations.json", "r", encoding="utf-8") as f:
            conversations = json.load(f)
        
        languages = [conv["language"] for conv in conversations["conversations"]]
        logger.info(f"🌍 Languages: {', '.join(set(languages))}")
        
        logger.info("\n📋 Next steps:")
        logger.info("1. Replace placeholder audio files with real recordings")
        logger.info("2. Run: python main_pipeline.py for full processing")
        logger.info("3. Review and validate all files")
        logger.info("4. Package for submission")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Working auto collector")
    parser.add_argument("--output", default="audio/raw", help="Output directory")
    
    args = parser.parse_args()
    
    collector = WorkingAutoCollector(args.output)
    success = collector.run_complete_sample_creation()
    
    if success:
        logger.info("🎉 Sample dataset created successfully!")
    else:
        logger.error("❌ Sample dataset creation failed!")

if __name__ == "__main__":
    main()
