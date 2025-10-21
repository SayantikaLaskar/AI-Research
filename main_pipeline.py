#!/usr/bin/env python3
"""
Main Processing Pipeline for Scam Call Dataset
Orchestrates the complete data processing workflow
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import argparse
from datetime import datetime

# Import our custom modules
from audio_processor import AudioProcessor
from diarization_pipeline import DiarizationPipeline
from transcription_pipeline import TranscriptionPipeline
from metadata_manager import MetadataManager
from data_collector import DataCollector

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScamDatasetPipeline:
    """Main pipeline for processing scam call dataset"""
    
    def __init__(self, project_dir: str = ".", hf_token: str = None):
        self.project_dir = Path(project_dir)
        self.hf_token = hf_token
        
        # Initialize components
        self.audio_processor = AudioProcessor()
        self.diarization_pipeline = DiarizationPipeline(hf_token=hf_token)
        self.transcription_pipeline = TranscriptionPipeline()
        self.metadata_manager = MetadataManager(str(self.project_dir))
        self.data_collector = DataCollector(str(self.project_dir / "audio" / "raw"))
        
        # Pipeline state
        self.processing_log = []
        
    def collect_data(self, search_youtube: bool = True, create_scenarios: bool = True):
        """Collect data from various sources"""
        logger.info("Starting data collection phase...")
        
        if create_scenarios:
            logger.info("Creating simulated scenarios...")
            scenarios = self.data_collector.create_simulated_scenarios()
            self.processing_log.append({
                'phase': 'data_collection',
                'action': 'create_scenarios',
                'count': len(scenarios),
                'timestamp': datetime.now().isoformat()
            })
        
        if search_youtube:
            logger.info("Searching YouTube for scam call videos...")
            keywords = [
                'scam call hindi',
                'fraud call recording',
                'phone scam india',
                'bank fraud call',
                'tech support scam'
            ]
            
            urls = self.data_collector.search_youtube_scam_calls(keywords, max_results=3)
            
            if urls:
                logger.info(f"Found {len(urls)} videos, downloading...")
                results = self.data_collector.download_youtube_audio(urls, max_duration=600)
                self.processing_log.append({
                    'phase': 'data_collection',
                    'action': 'download_youtube',
                    'count': len(results),
                    'timestamp': datetime.now().isoformat()
                })
        
        self.data_collector.save_collection_log()
        logger.info("Data collection phase completed")
    
    def process_audio(self):
        """Process raw audio files"""
        logger.info("Starting audio processing phase...")
        
        raw_dir = self.project_dir / "audio" / "raw"
        processed_dir = self.project_dir / "audio" / "processed"
        
        if not raw_dir.exists() or not any(raw_dir.iterdir()):
            logger.warning("No raw audio files found. Run data collection first.")
            return
        
        # Process audio files
        metadata_list = self.audio_processor.batch_process(str(raw_dir), str(processed_dir))
        
        self.processing_log.append({
            'phase': 'audio_processing',
            'action': 'normalize_audio',
            'count': len(metadata_list),
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Processed {len(metadata_list)} audio files")
    
    def perform_diarization(self):
        """Perform speaker diarization on processed audio"""
        logger.info("Starting speaker diarization phase...")
        
        processed_dir = self.project_dir / "audio" / "processed"
        diarization_dir = self.project_dir / "diarization"
        
        if not processed_dir.exists() or not any(processed_dir.iterdir()):
            logger.warning("No processed audio files found. Run audio processing first.")
            return
        
        # Perform diarization
        results = self.diarization_pipeline.batch_diarize(
            str(processed_dir), 
            str(diarization_dir)
        )
        
        self.processing_log.append({
            'phase': 'diarization',
            'action': 'speaker_diarization',
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Diarized {len(results)} audio files")
    
    def perform_transcription(self, language: str = None):
        """Perform transcription on processed audio"""
        logger.info("Starting transcription phase...")
        
        processed_dir = self.project_dir / "audio" / "processed"
        transcript_dir = self.project_dir / "transcripts"
        
        if not processed_dir.exists() or not any(processed_dir.iterdir()):
            logger.warning("No processed audio files found. Run audio processing first.")
            return
        
        # Perform transcription
        results = self.transcription_pipeline.batch_transcribe(
            str(processed_dir), 
            str(transcript_dir),
            language=language
        )
        
        self.processing_log.append({
            'phase': 'transcription',
            'action': 'speech_recognition',
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Transcribed {len(results)} audio files")
    
    def combine_results(self):
        """Combine diarization and transcription results"""
        logger.info("Starting result combination phase...")
        
        diarization_dir = self.project_dir / "diarization"
        transcript_dir = self.project_dir / "transcripts"
        combined_dir = self.project_dir / "transcripts" / "combined"
        combined_dir.mkdir(exist_ok=True)
        
        combined_count = 0
        
        # Find matching diarization and transcription files
        for diar_file in diarization_dir.glob("*_diarization.json"):
            file_id = diar_file.stem.replace("_diarization", "")
            trans_file = transcript_dir / f"{file_id}_transcript.json"
            
            if trans_file.exists():
                # Combine results
                combined_result = self.transcription_pipeline.combine_diarization_transcription(
                    str(diar_file), str(trans_file)
                )
                
                if combined_result:
                    # Save combined result
                    output_file = combined_dir / f"{file_id}_combined.json"
                    self.transcription_pipeline.save_transcript(combined_result, str(output_file))
                    combined_count += 1
        
        self.processing_log.append({
            'phase': 'combination',
            'action': 'combine_results',
            'count': combined_count,
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Combined {combined_count} diarization and transcription results")
    
    def annotate_speaker_roles(self):
        """Manually annotate speaker roles (scammer/victim)"""
        logger.info("Starting speaker role annotation phase...")
        
        combined_dir = self.project_dir / "transcripts" / "combined"
        
        if not combined_dir.exists():
            logger.warning("No combined results found. Run combination phase first.")
            return
        
        annotation_guide = {
            'instructions': [
                'Review each conversation transcript',
                'Identify which speaker is the scammer and which is the victim',
                'Update the speaker roles in the JSON files',
                'Common scammer tactics:',
                '  - Asking for personal information',
                '  - Requesting money or payment',
                '  - Creating urgency or fear',
                '  - Pretending to be from official organizations',
                '  - Asking for OTP or passwords'
            ],
            'files_to_annotate': []
        }
        
        for file_path in combined_dir.glob("*_combined.json"):
            annotation_guide['files_to_annotate'].append(str(file_path))
        
        # Save annotation guide
        guide_file = self.project_dir / "annotation_guide.json"
        with open(guide_file, 'w', encoding='utf-8') as f:
            json.dump(annotation_guide, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created annotation guide for {len(annotation_guide['files_to_annotate'])} files")
        logger.info("Manual annotation required - please review and update speaker roles")
    
    def create_metadata(self):
        """Create comprehensive metadata for the dataset"""
        logger.info("Starting metadata creation phase...")
        
        # This would typically be done after manual annotation
        # For now, create placeholder metadata entries
        
        processed_dir = self.project_dir / "audio" / "processed"
        combined_dir = self.project_dir / "transcripts" / "combined"
        
        metadata_entries = []
        
        for audio_file in processed_dir.glob("*.wav"):
            file_id = audio_file.stem
            combined_file = combined_dir / f"{file_id}_combined.json"
            
            if combined_file.exists():
                # Load combined results to get metadata
                with open(combined_file, 'r', encoding='utf-8') as f:
                    combined_data = json.load(f)
                
                # Create metadata entry
                metadata = self.metadata_manager.create_metadata_entry(
                    file_id=file_id,
                    filename=audio_file.name,
                    duration_sec=combined_data.get('duration', 0),
                    num_speakers=combined_data.get('num_speakers', 2),
                    speaker_roles=['scammer', 'victim'],  # Placeholder - needs manual annotation
                    source_type='public',  # Placeholder - needs verification
                    recording_conditions='Unknown',  # Placeholder
                    language=combined_data.get('language', 'unknown'),
                    notes='Generated by automated pipeline - requires manual review'
                )
                
                metadata_entries.append(metadata)
        
        # Add metadata entries
        for metadata in metadata_entries:
            self.metadata_manager.add_metadata_entry(metadata)
        
        logger.info(f"Created metadata for {len(metadata_entries)} conversations")
    
    def generate_final_report(self):
        """Generate final dataset report"""
        logger.info("Generating final dataset report...")
        
        # Get metadata summary
        summary = self.metadata_manager.get_metadata_summary()
        
        # Create final report
        report = {
            'dataset_info': {
                'creation_date': datetime.now().isoformat(),
                'total_conversations': summary.get('total_conversations', 0),
                'total_duration_minutes': summary.get('total_duration_minutes', 0),
                'languages': summary.get('languages', {}),
                'source_types': summary.get('source_types', {})
            },
            'processing_log': self.processing_log,
            'quality_metrics': {
                'average_duration_seconds': summary.get('average_duration_seconds', 0),
                'min_duration_seconds': summary.get('min_duration_seconds', 0),
                'max_duration_seconds': summary.get('max_duration_seconds', 0)
            }
        }
        
        # Save report
        report_file = self.project_dir / "dataset_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Create README
        self.metadata_manager.save_readme()
        
        logger.info(f"Final report saved to {report_file}")
        logger.info("Dataset processing completed!")
    
    def run_full_pipeline(self, search_youtube: bool = True, create_scenarios: bool = True):
        """Run the complete processing pipeline"""
        logger.info("Starting full dataset processing pipeline...")
        
        try:
            # Phase 1: Data Collection
            self.collect_data(search_youtube, create_scenarios)
            
            # Phase 2: Audio Processing
            self.process_audio()
            
            # Phase 3: Speaker Diarization
            self.perform_diarization()
            
            # Phase 4: Transcription
            self.perform_transcription()
            
            # Phase 5: Combine Results
            self.combine_results()
            
            # Phase 6: Manual Annotation (guidance only)
            self.annotate_speaker_roles()
            
            # Phase 7: Create Metadata
            self.create_metadata()
            
            # Phase 8: Generate Report
            self.generate_final_report()
            
            logger.info("Full pipeline completed successfully!")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Process scam call dataset")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    parser.add_argument("--hf-token", help="Hugging Face token for model access")
    parser.add_argument("--skip-collection", action="store_true", help="Skip data collection phase")
    parser.add_argument("--skip-youtube", action="store_true", help="Skip YouTube data collection")
    parser.add_argument("--skip-scenarios", action="store_true", help="Skip scenario creation")
    parser.add_argument("--language", help="Language for transcription (hi, en, auto)")
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = ScamDatasetPipeline(args.project_dir, args.hf_token)
    
    if args.skip_collection:
        # Run processing phases only
        pipeline.process_audio()
        pipeline.perform_diarization()
        pipeline.perform_transcription(args.language)
        pipeline.combine_results()
        pipeline.annotate_speaker_roles()
        pipeline.create_metadata()
        pipeline.generate_final_report()
    else:
        # Run full pipeline
        pipeline.run_full_pipeline(
            search_youtube=not args.skip_youtube,
            create_scenarios=not args.skip_scenarios
        )

if __name__ == "__main__":
    main()
