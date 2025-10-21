#!/usr/bin/env python3
"""
Simple Automatic Data Collection (No External Dependencies)
Creates scripts and guides for manual data collection
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleAutoCollector:
    """Simple automatic data collection without external dependencies"""
    
    def __init__(self, output_dir: str = "audio/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_recording_guide(self):
        """Create a comprehensive recording guide"""
        logger.info("Creating recording guide...")
        
        guide = {
            "title": "Scam Call Dataset Recording Guide",
            "created": datetime.now().isoformat(),
            "languages": ["Hindi", "Hinglish", "English"],
            "target_duration": "2-8 minutes per conversation",
            "audio_quality": {
                "format": "WAV",
                "sample_rate": "16 kHz",
                "channels": "Mono",
                "bit_depth": "16-bit"
            },
            "recording_environment": {
                "location": "Quiet room with minimal background noise",
                "microphone": "Good quality microphone or phone",
                "distance": "6-12 inches from microphone",
                "speakers": "Use different voices for scammer and victim"
            },
            "scenarios": self._get_recording_scenarios(),
            "recording_tips": [
                "Speak naturally with appropriate emotions",
                "Scammer: persuasive, urgent, sometimes aggressive",
                "Victim: cautious, suspicious, sometimes confused",
                "Include natural pauses and interruptions",
                "Maintain consistent voice for each speaker",
                "Record in quiet environment",
                "Test audio quality before recording"
            ]
        }
        
        # Save guide
        guide_file = self.output_dir / "recording_guide.json"
        with open(guide_file, "w", encoding="utf-8") as f:
            json.dump(guide, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Recording guide saved to {guide_file}")
        return guide
    
    def _get_recording_scenarios(self):
        """Get recording scenarios from sample conversations"""
        with open("sample_conversations.json", "r", encoding="utf-8") as f:
            conversations = json.load(f)
        
        scenarios = []
        for conv in conversations["conversations"]:
            scenario = {
                "id": conv["id"],
                "title": conv["title"],
                "language": conv["language"],
                "duration_estimate": conv["duration_estimate"],
                "description": conv["scenario"],
                "script": conv["script"],
                "recording_notes": {
                    "scammer_voice": "Persuasive, urgent, sometimes aggressive",
                    "victim_voice": "Cautious, suspicious, sometimes confused",
                    "pacing": "Natural conversation pace with pauses",
                    "emotions": "Realistic emotional responses"
                }
            }
            scenarios.append(scenario)
        
        return scenarios
    
    def create_youtube_search_guide(self):
        """Create a guide for finding YouTube scam call videos"""
        logger.info("Creating YouTube search guide...")
        
        search_guide = {
            "title": "YouTube Scam Call Search Guide",
            "created": datetime.now().isoformat(),
            "search_keywords": {
                "hindi": [
                    "scam call hindi",
                    "bank fraud call india",
                    "OTP fraud call hindi",
                    "phone scam hindi",
                    "fraud call recording hindi",
                    "scam call recording india"
                ],
                "hinglish": [
                    "scam call hinglish",
                    "fraud call india",
                    "tech support scam",
                    "phone scam hinglish",
                    "bank fraud hinglish",
                    "scam call recording hinglish"
                ],
                "english": [
                    "scam call english",
                    "tech support scam call",
                    "IRS scam call",
                    "lottery scam call",
                    "investment scam call",
                    "phone scam recording english"
                ]
            },
            "video_criteria": {
                "duration": "1-10 minutes (preferably 2-8 minutes)",
                "audio_quality": "Clear audio, minimal background noise",
                "speakers": "2 speakers (scammer and victim)",
                "content": "Actual scam call conversations",
                "language": "Match target language (Hindi/Hinglish/English)"
            },
            "download_instructions": {
                "tool": "yt-dlp (recommended) or youtube-dl",
                "command": "yt-dlp -f 'bestaudio[ext=m4a]/bestaudio' --extract-audio --audio-format wav 'URL'",
                "output_format": "WAV, 16kHz, mono",
                "max_duration": "600 seconds (10 minutes)"
            },
            "manual_download_steps": [
                "1. Search YouTube using keywords above",
                "2. Find videos with scam call conversations",
                "3. Check video duration (1-10 minutes)",
                "4. Listen to audio quality",
                "5. Download using yt-dlp or similar tool",
                "6. Convert to WAV format, 16kHz, mono",
                "7. Save to audio/raw/ directory"
            ]
        }
        
        # Save search guide
        search_file = self.output_dir / "youtube_search_guide.json"
        with open(search_file, "w", encoding="utf-8") as f:
            json.dump(search_guide, f, indent=2, ensure_ascii=False)
        
        logger.info(f"YouTube search guide saved to {search_file}")
        return search_guide
    
    def create_tts_guide(self):
        """Create a guide for text-to-speech synthesis"""
        logger.info("Creating TTS guide...")
        
        tts_guide = {
            "title": "Text-to-Speech Synthesis Guide",
            "created": datetime.now().isoformat(),
            "tools": {
                "gtts": {
                    "name": "Google Text-to-Speech",
                    "install": "pip install gtts",
                    "usage": "gtts-cli -f input.txt -l hi -o output.mp3"
                },
                "espeak": {
                    "name": "eSpeak",
                    "install": "apt-get install espeak (Linux) or brew install espeak (macOS)",
                    "usage": "espeak -f input.txt -w output.wav"
                },
                "festival": {
                    "name": "Festival",
                    "install": "apt-get install festival (Linux)",
                    "usage": "festival --tts input.txt > output.wav"
                }
            },
            "language_codes": {
                "hindi": "hi",
                "english": "en",
                "hinglish": "hi"  # Use Hindi for Hinglish
            },
            "workflow": [
                "1. Extract text from sample_conversations.json",
                "2. Split into scammer and victim parts",
                "3. Generate separate audio for each speaker",
                "4. Combine audio files with proper timing",
                "5. Save as WAV format, 16kHz, mono"
            ],
            "example_commands": [
                "# Extract text for Hindi bank fraud scenario",
                "echo 'Namaste, main SBI bank ke fraud department se baat kar raha hun.' > scammer.txt",
                "echo 'Haan, main Rajesh Kumar hun. Kya problem hai?' > victim.txt",
                "",
                "# Generate TTS audio",
                "gtts-cli -f scammer.txt -l hi -o scammer.mp3",
                "gtts-cli -f victim.txt -l hi -o victim.mp3",
                "",
                "# Combine with ffmpeg",
                "ffmpeg -i scammer.mp3 -i victim.mp3 -filter_complex '[0:0][1:0]concat=n=2:v=0:a=1[out]' -map '[out]' combined.wav"
            ]
        }
        
        # Save TTS guide
        tts_file = self.output_dir / "tts_guide.json"
        with open(tts_file, "w", encoding="utf-8") as f:
            json.dump(tts_guide, f, indent=2, ensure_ascii=False)
        
        logger.info(f"TTS guide saved to {tts_file}")
        return tts_guide
    
    def create_data_collection_plan(self):
        """Create a comprehensive data collection plan"""
        logger.info("Creating data collection plan...")
        
        plan = {
            "title": "Scam Call Dataset Collection Plan",
            "created": datetime.now().isoformat(),
            "target": {
                "total_conversations": 20,
                "languages": {
                    "hindi": 7,
                    "hinglish": 7,
                    "english": 6
                },
                "total_duration_minutes": 120,
                "average_duration_minutes": 6
            },
            "collection_methods": {
                "youtube_downloads": {
                    "description": "Download existing scam call videos from YouTube",
                    "target_files": 10,
                    "advantages": ["Real conversations", "Natural speech patterns", "Authentic scenarios"],
                    "disadvantages": ["Copyright issues", "Variable quality", "May need permission"]
                },
                "simulated_recordings": {
                    "description": "Record scripted conversations with actors",
                    "target_files": 8,
                    "advantages": ["Controlled quality", "Clear consent", "Consistent format"],
                    "disadvantages": ["May sound scripted", "Requires actors", "Time-consuming"]
                },
                "tts_synthesis": {
                    "description": "Generate audio using text-to-speech",
                    "target_files": 2,
                    "advantages": ["Fast generation", "Consistent quality", "Easy to modify"],
                    "disadvantages": ["May sound robotic", "Limited emotional range", "Less natural"]
                }
            },
            "quality_requirements": {
                "audio_quality": "Clear, minimal background noise",
                "speaker_separation": "Distinct voices for scammer and victim",
                "language_accuracy": "Proper pronunciation and accent",
                "content_authenticity": "Realistic scam scenarios",
                "duration": "2-8 minutes per conversation"
            },
            "next_steps": [
                "1. Review recording guides and scenarios",
                "2. Choose collection method(s) based on resources",
                "3. Start with 3-5 files per language for testing",
                "4. Record/download audio files",
                "5. Process audio using main_pipeline.py",
                "6. Manually annotate speaker roles",
                "7. Validate and finalize dataset"
            ]
        }
        
        # Save plan
        plan_file = self.output_dir / "data_collection_plan.json"
        with open(plan_file, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data collection plan saved to {plan_file}")
        return plan
    
    def run_simple_collection(self):
        """Run simple data collection (creates guides and scripts)"""
        logger.info("=== Starting Simple Data Collection ===")
        
        results = {
            "start_time": datetime.now().isoformat(),
            "guides_created": [],
            "status": "success"
        }
        
        try:
            # Create all guides
            recording_guide = self.create_recording_guide()
            results["guides_created"].append("recording_guide.json")
            
            youtube_guide = self.create_youtube_search_guide()
            results["guides_created"].append("youtube_search_guide.json")
            
            tts_guide = self.create_tts_guide()
            results["guides_created"].append("tts_guide.json")
            
            collection_plan = self.create_data_collection_plan()
            results["guides_created"].append("data_collection_plan.json")
            
            results["end_time"] = datetime.now().isoformat()
            
            logger.info("=== Simple Data Collection Completed ===")
            logger.info(f"Created {len(results['guides_created'])} guides")
            
        except Exception as e:
            logger.error(f"Collection failed: {str(e)}")
            results["error"] = str(e)
            results["status"] = "failed"
        
        return results
    
    def show_collection_summary(self, results):
        """Show summary of collection results"""
        logger.info("\n=== Collection Summary ===")
        
        if results["status"] == "success":
            logger.info("✅ All guides created successfully!")
            logger.info(f"📁 Guides saved in: {self.output_dir}")
            logger.info(f"📋 Created guides: {', '.join(results['guides_created'])}")
            
            logger.info("\n📖 Next steps:")
            logger.info("1. Review the guides in audio/raw/ directory")
            logger.info("2. Choose your data collection method:")
            logger.info("   - YouTube downloads (see youtube_search_guide.json)")
            logger.info("   - Manual recording (see recording_guide.json)")
            logger.info("   - TTS synthesis (see tts_guide.json)")
            logger.info("3. Follow the data_collection_plan.json")
            logger.info("4. Run: python main_pipeline.py to process collected data")
            
        else:
            logger.error("❌ Collection failed")
            logger.error(f"Error: {results.get('error', 'Unknown error')}")

def main():
    """Main function for simple data collection"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple automatic data collection")
    parser.add_argument("--output", default="audio/raw", help="Output directory")
    
    args = parser.parse_args()
    
    collector = SimpleAutoCollector(args.output)
    results = collector.run_simple_collection()
    collector.show_collection_summary(results)

if __name__ == "__main__":
    main()
