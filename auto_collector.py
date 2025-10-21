#!/usr/bin/env python3
"""
Automatic Data Collection for Scam Call Dataset
Collects audio from multiple sources with minimal manual intervention
"""

import os
import json
import logging
import requests
import yt_dlp
from pathlib import Path
from typing import Dict, List, Optional
import time
import random
from datetime import datetime
import subprocess
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoDataCollector:
    """Automatic data collection from multiple sources"""
    
    def __init__(self, output_dir: str = "audio/raw", max_files_per_source: int = 5):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_files_per_source = max_files_per_source
        self.collection_log = []
        
        # Search configurations for different languages
        self.search_configs = {
            'hindi': {
                'keywords': [
                    'scam call hindi',
                    'bank fraud call india',
                    'OTP fraud call hindi',
                    'phone scam hindi',
                    'fraud call recording hindi'
                ],
                'filters': ['call', 'scam', 'fraud', 'hindi']
            },
            'hinglish': {
                'keywords': [
                    'scam call hinglish',
                    'fraud call india',
                    'tech support scam',
                    'phone scam hinglish',
                    'bank fraud hinglish'
                ],
                'filters': ['call', 'scam', 'fraud', 'hinglish']
            },
            'english': {
                'keywords': [
                    'scam call english',
                    'tech support scam call',
                    'IRS scam call',
                    'lottery scam call',
                    'investment scam call'
                ],
                'filters': ['call', 'scam', 'fraud', 'english']
            }
        }
    
    def search_youtube_automatically(self) -> Dict[str, List[str]]:
        """Automatically search YouTube for scam call videos by language"""
        logger.info("Starting automatic YouTube search...")
        
        all_urls = {}
        
        for language, config in self.search_configs.items():
            logger.info(f"Searching for {language} scam calls...")
            urls = []
            
            for keyword in config['keywords']:
                try:
                    # Search YouTube
                    search_urls = self._search_youtube_keyword(keyword, max_results=3)
                    urls.extend(search_urls)
                    
                    # Add delay to avoid rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error searching for '{keyword}': {str(e)}")
            
            # Remove duplicates and limit results
            urls = list(set(urls))[:self.max_files_per_source]
            all_urls[language] = urls
            
            logger.info(f"Found {len(urls)} URLs for {language}")
        
        return all_urls
    
    def _search_youtube_keyword(self, keyword: str, max_results: int = 5) -> List[str]:
        """Search YouTube for a specific keyword"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'default_search': 'ytsearch',
                'max_results': max_results
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch{max_results}:{keyword}"
                results = ydl.extract_info(search_query, download=False)
                
                urls = []
                if 'entries' in results:
                    for entry in results['entries']:
                        if entry and 'webpage_url' in entry:
                            # Filter by duration (1-10 minutes)
                            duration = entry.get('duration', 0)
                            if 60 <= duration <= 600:  # 1-10 minutes
                                urls.append(entry['webpage_url'])
                                logger.info(f"Found: {entry.get('title', 'Unknown')} ({duration}s)")
                
                return urls
                
        except Exception as e:
            logger.error(f"Error searching YouTube for '{keyword}': {str(e)}")
            return []
    
    def download_audio_batch(self, urls_by_language: Dict[str, List[str]]) -> Dict[str, List[Dict]]:
        """Download audio files in batches by language"""
        logger.info("Starting batch audio download...")
        
        download_results = {}
        
        for language, urls in urls_by_language.items():
            if not urls:
                continue
                
            logger.info(f"Downloading {len(urls)} files for {language}...")
            
            # Create language-specific subdirectory
            lang_dir = self.output_dir / language
            lang_dir.mkdir(exist_ok=True)
            
            results = self._download_language_batch(urls, str(lang_dir), language)
            download_results[language] = results
            
            # Add delay between languages
            time.sleep(3)
        
        return download_results
    
    def _download_language_batch(self, urls: List[str], output_dir: str, language: str) -> List[Dict]:
        """Download audio files for a specific language"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'extractaudio': True,
            'audioformat': 'wav',
            'audioquality': '0',
            'noplaylist': True,
            'max_duration': 600,  # 10 minutes max
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        
        results = []
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for i, url in enumerate(urls):
                try:
                    logger.info(f"Downloading {i+1}/{len(urls)} for {language}: {url}")
                    
                    # Get video info first
                    info = ydl.extract_info(url, download=False)
                    duration = info.get('duration', 0)
                    title = info.get('title', 'Unknown')
                    
                    # Skip if too long or too short
                    if duration > 600 or duration < 60:
                        logger.warning(f"Skipping {title} - duration {duration}s")
                        continue
                    
                    # Download audio
                    ydl.download([url])
                    
                    # Get filename
                    filename = ydl.prepare_filename(info)
                    if not filename.endswith('.wav'):
                        filename += '.wav'
                    
                    result = {
                        'source': 'youtube',
                        'url': url,
                        'title': title,
                        'duration': duration,
                        'filename': Path(filename).name,
                        'language': language,
                        'download_time': datetime.now().isoformat(),
                        'status': 'success'
                    }
                    
                    results.append(result)
                    self.collection_log.append(result)
                    
                    # Add delay between downloads
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Failed to download {url}: {str(e)}")
                    error_result = {
                        'source': 'youtube',
                        'url': url,
                        'language': language,
                        'status': 'failed',
                        'error': str(e),
                        'download_time': datetime.now().isoformat()
                    }
                    results.append(error_result)
                    self.collection_log.append(error_result)
        
        return results
    
    def create_simulated_audio_scripts(self) -> List[Dict]:
        """Create scripts for simulated audio recording"""
        logger.info("Creating simulated audio recording scripts...")
        
        scripts = []
        
        # Load sample conversations
        with open("sample_conversations.json", "r", encoding="utf-8") as f:
            conversations = json.load(f)
        
        for conv in conversations["conversations"]:
            script_info = {
                'id': conv['id'],
                'title': conv['title'],
                'language': conv['language'],
                'duration_estimate': conv['duration_estimate'],
                'scenario': conv['scenario'],
                'script': conv['script'],
                'recording_instructions': {
                    'audio_quality': 'Record in quiet environment with good microphone',
                    'speakers': 'Use different voices for scammer and victim',
                    'pacing': 'Natural conversation pace, include pauses',
                    'emotions': 'Scammer: persuasive, urgent. Victim: cautious, suspicious',
                    'file_format': 'Save as WAV, 16kHz if possible'
                }
            }
            scripts.append(script_info)
        
        # Save scripts
        scripts_file = self.output_dir / "recording_scripts.json"
        with open(scripts_file, "w", encoding="utf-8") as f:
            json.dump(scripts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created {len(scripts)} recording scripts")
        return scripts
    
    def generate_audio_synthesis_commands(self) -> List[str]:
        """Generate commands for text-to-speech synthesis"""
        logger.info("Generating TTS synthesis commands...")
        
        commands = []
        
        # Load sample conversations
        with open("sample_conversations.json", "r", encoding="utf-8") as f:
            conversations = json.load(f)
        
        for conv in conversations["conversations"]:
            lang_dir = self.output_dir / "synthetic" / conv['language']
            lang_dir.mkdir(parents=True, exist_ok=True)
            
            # Create separate files for each speaker
            scammer_text = []
            victim_text = []
            
            for line in conv['script']:
                if line['speaker'] == 'scammer':
                    scammer_text.append(line['text'])
                else:
                    victim_text.append(line['text'])
            
            # Generate TTS commands (example using gTTS)
            scammer_file = lang_dir / f"{conv['id']}_scammer.txt"
            victim_file = lang_dir / f"{conv['id']}_victim.txt"
            
            with open(scammer_file, "w", encoding="utf-8") as f:
                f.write(" ".join(scammer_text))
            
            with open(victim_file, "w", encoding="utf-8") as f:
                f.write(" ".join(victim_text))
            
            # TTS commands
            commands.extend([
                f"# {conv['title']} - {conv['language']}",
                f"gtts-cli -f {scammer_file} -l {self._get_tts_language(conv['language'])} -o {lang_dir}/{conv['id']}_scammer.mp3",
                f"gtts-cli -f {victim_file} -l {self._get_tts_language(conv['language'])} -o {lang_dir}/{conv['id']}_victim.mp3",
                f"# Combine with ffmpeg: ffmpeg -i {lang_dir}/{conv['id']}_scammer.mp3 -i {lang_dir}/{conv['id']}_victim.mp3 -filter_complex '[0:0][1:0]concat=n=2:v=0:a=1[out]' -map '[out]' {lang_dir}/{conv['id']}_combined.wav",
                ""
            ])
        
        # Save commands
        commands_file = self.output_dir / "tts_commands.sh"
        with open(commands_file, "w", encoding="utf-8") as f:
            f.write("\n".join(commands))
        
        logger.info(f"Generated TTS commands in {commands_file}")
        return commands
    
    def _get_tts_language(self, language: str) -> str:
        """Get TTS language code"""
        mapping = {
            'hindi': 'hi',
            'hinglish': 'hi',  # Use Hindi for Hinglish
            'english': 'en'
        }
        return mapping.get(language, 'en')
    
    def run_full_auto_collection(self) -> Dict:
        """Run complete automatic data collection"""
        logger.info("=== Starting Full Automatic Data Collection ===")
        
        results = {
            'start_time': datetime.now().isoformat(),
            'youtube_search': {},
            'download_results': {},
            'scripts_created': [],
            'tts_commands': []
        }
        
        try:
            # Step 1: Search YouTube automatically
            logger.info("Step 1: Searching YouTube...")
            urls_by_language = self.search_youtube_automatically()
            results['youtube_search'] = urls_by_language
            
            # Step 2: Download audio files
            logger.info("Step 2: Downloading audio files...")
            download_results = self.download_audio_batch(urls_by_language)
            results['download_results'] = download_results
            
            # Step 3: Create simulated scripts
            logger.info("Step 3: Creating simulated recording scripts...")
            scripts = self.create_simulated_audio_scripts()
            results['scripts_created'] = scripts
            
            # Step 4: Generate TTS commands
            logger.info("Step 4: Generating TTS synthesis commands...")
            tts_commands = self.generate_audio_synthesis_commands()
            results['tts_commands'] = tts_commands
            
            # Step 5: Save collection log
            self.save_collection_log()
            
            results['end_time'] = datetime.now().isoformat()
            results['status'] = 'success'
            
            logger.info("=== Automatic Data Collection Completed ===")
            
        except Exception as e:
            logger.error(f"Collection failed: {str(e)}")
            results['error'] = str(e)
            results['status'] = 'failed'
        
        return results
    
    def save_collection_log(self):
        """Save collection log to file"""
        log_file = self.output_dir.parent / "collection_log.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.collection_log, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Collection log saved to {log_file}")
    
    def show_collection_summary(self, results: Dict):
        """Show summary of collection results"""
        logger.info("\n=== Collection Summary ===")
        
        total_downloaded = 0
        for language, downloads in results.get('download_results', {}).items():
            successful = len([d for d in downloads if d.get('status') == 'success'])
            total_downloaded += successful
            logger.info(f"{language}: {successful} files downloaded")
        
        logger.info(f"Total files collected: {total_downloaded}")
        logger.info(f"Scripts created: {len(results.get('scripts_created', []))}")
        logger.info(f"TTS commands generated: {len(results.get('tts_commands', []))}")
        
        logger.info("\nNext steps:")
        logger.info("1. Review downloaded files in audio/raw/")
        logger.info("2. Record simulated conversations using scripts")
        logger.info("3. Run: python main_pipeline.py")

def main():
    """Main function for automatic data collection"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automatic scam call data collection")
    parser.add_argument("--output", default="audio/raw", help="Output directory")
    parser.add_argument("--max-files", type=int, default=5, help="Max files per language")
    parser.add_argument("--youtube-only", action="store_true", help="Only search YouTube")
    parser.add_argument("--scripts-only", action="store_true", help="Only create scripts")
    
    args = parser.parse_args()
    
    collector = AutoDataCollector(args.output, args.max_files)
    
    if args.scripts_only:
        # Only create scripts
        scripts = collector.create_simulated_audio_scripts()
        tts_commands = collector.generate_audio_synthesis_commands()
        collector.save_collection_log()
        logger.info("Scripts and TTS commands created")
        
    elif args.youtube_only:
        # Only search and download from YouTube
        urls_by_language = collector.search_youtube_automatically()
        download_results = collector.download_audio_batch(urls_by_language)
        collector.save_collection_log()
        collector.show_collection_summary({'download_results': download_results})
        
    else:
        # Full automatic collection
        results = collector.run_full_auto_collection()
        collector.show_collection_summary(results)

if __name__ == "__main__":
    main()
