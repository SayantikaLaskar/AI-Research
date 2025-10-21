#!/usr/bin/env python3
"""
Data Collection Script for Scam Call Dataset
Handles downloading and collecting audio from various sources
"""

import os
import json
import logging
import requests
import yt_dlp
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollector:
    """Handles collection of scam call audio from various sources"""
    
    def __init__(self, output_dir: str = "audio/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.collection_log = []
        
    def download_youtube_audio(self, urls: List[str], max_duration: int = 600) -> List[Dict]:
        """
        Download audio from YouTube videos
        
        Args:
            urls: List of YouTube URLs
            max_duration: Maximum duration in seconds (default 10 minutes)
            
        Returns:
            List of download metadata
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'extractaudio': True,
            'audioformat': 'wav',
            'audioquality': '0',
            'noplaylist': True,
            'max_duration': max_duration,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        
        results = []
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in urls:
                try:
                    logger.info(f"Downloading from {url}")
                    
                    # Get video info first
                    info = ydl.extract_info(url, download=False)
                    duration = info.get('duration', 0)
                    
                    if duration > max_duration:
                        logger.warning(f"Video {url} is too long ({duration}s), skipping")
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
                        'title': info.get('title', 'Unknown'),
                        'duration': duration,
                        'filename': Path(filename).name,
                        'download_time': datetime.now().isoformat(),
                        'status': 'success'
                    }
                    
                    results.append(result)
                    self.collection_log.append(result)
                    
                except Exception as e:
                    logger.error(f"Failed to download {url}: {str(e)}")
                    error_result = {
                        'source': 'youtube',
                        'url': url,
                        'status': 'failed',
                        'error': str(e),
                        'download_time': datetime.now().isoformat()
                    }
                    results.append(error_result)
                    self.collection_log.append(error_result)
        
        return results
    
    def create_simulated_scenarios(self) -> List[Dict]:
        """
        Create simulated scam call scenarios for recording
        
        Returns:
            List of scenario descriptions
        """
        scenarios = [
            {
                'scenario_id': 'bank_fraud_hindi',
                'title': 'Bank Fraud Call - Hindi',
                'description': 'Scammer pretending to be from bank fraud department',
                'language': 'hindi',
                'duration_estimate': 300,
                'script_outline': [
                    'Scammer: Bank fraud department se baat kar rahe hain...',
                    'Victim: Haan, main sun raha hun...',
                    'Scammer: Aapke account mein suspicious activity detect hui hai...',
                    'Victim: Kya hua hai?',
                    'Scammer: Aapko OTP share karna hoga verification ke liye...'
                ]
            },
            {
                'scenario_id': 'tech_support_hinglish',
                'title': 'Tech Support Scam - Hinglish',
                'description': 'Scammer pretending to be tech support',
                'language': 'hinglish',
                'duration_estimate': 400,
                'script_outline': [
                    'Scammer: Sir, main Microsoft se call kar raha hun...',
                    'Victim: Haan, kya problem hai?',
                    'Scammer: Aapke computer mein virus aa gaya hai...',
                    'Victim: Really? Kaise pata chala?',
                    'Scammer: Remote access deke main check kar sakta hun...'
                ]
            },
            {
                'scenario_id': 'lottery_scam_english',
                'title': 'Lottery Scam - English',
                'description': 'Scammer claiming victim won lottery',
                'language': 'english',
                'duration_estimate': 350,
                'script_outline': [
                    'Scammer: Congratulations! You have won $50,000 in our lottery...',
                    'Victim: Really? I never entered any lottery...',
                    'Scammer: Your number was randomly selected...',
                    'Victim: How do I claim the prize?',
                    'Scammer: You need to pay processing fees first...'
                ]
            },
            {
                'scenario_id': 'investment_scam_hindi',
                'title': 'Investment Scam - Hindi',
                'description': 'Scammer offering fake investment opportunity',
                'language': 'hindi',
                'duration_estimate': 450,
                'script_outline': [
                    'Scammer: Sir, main investment advisor hun...',
                    'Victim: Haan, kya offer hai?',
                    'Scammer: 50% return guarantee hai hamare scheme mein...',
                    'Victim: Itna high return kaise possible hai?',
                    'Scammer: Hamare clients ko regular profit mil raha hai...'
                ]
            }
        ]
        
        # Save scenarios to file
        scenarios_file = self.output_dir.parent / 'simulated_scenarios.json'
        with open(scenarios_file, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created {len(scenarios)} simulated scenarios")
        return scenarios
    
    def search_youtube_scam_calls(self, keywords: List[str], max_results: int = 10) -> List[str]:
        """
        Search YouTube for scam call videos
        
        Args:
            keywords: List of search keywords
            max_results: Maximum number of results per keyword
            
        Returns:
            List of YouTube URLs
        """
        urls = []
        
        for keyword in keywords:
            try:
                # Use yt-dlp to search
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
                    
                    if 'entries' in results:
                        for entry in results['entries']:
                            if entry:
                                urls.append(entry['webpage_url'])
                                logger.info(f"Found: {entry.get('title', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"Error searching for '{keyword}': {str(e)}")
        
        return urls
    
    def create_collection_plan(self) -> Dict:
        """Create a comprehensive data collection plan"""
        plan = {
            'collection_date': datetime.now().isoformat(),
            'target_languages': ['hindi', 'hinglish', 'english'],
            'target_duration_minutes': 120,  # 2 hours total
            'sources': {
                'youtube': {
                    'search_keywords': [
                        'scam call hindi',
                        'fraud call recording',
                        'phone scam india',
                        'bank fraud call',
                        'tech support scam',
                        'lottery scam call',
                        'investment scam hindi',
                        'scam call recording english'
                    ],
                    'max_duration_per_video': 600,  # 10 minutes
                    'estimated_videos': 20
                },
                'simulated': {
                    'scenarios': 4,
                    'languages': ['hindi', 'hinglish', 'english'],
                    'estimated_duration_per_scenario': 400  # seconds
                }
            },
            'quality_requirements': {
                'min_duration_seconds': 60,
                'max_duration_seconds': 600,
                'required_speakers': 2,
                'audio_quality': 'clear'
            }
        }
        
        # Save collection plan
        plan_file = self.output_dir.parent / 'collection_plan.json'
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        return plan
    
    def save_collection_log(self):
        """Save collection log to file"""
        log_file = self.output_dir.parent / 'collection_log.json'
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.collection_log, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Collection log saved to {log_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Collect scam call audio data")
    parser.add_argument("--output", default="audio/raw", help="Output directory for audio files")
    parser.add_argument("--search-youtube", action="store_true", help="Search and download from YouTube")
    parser.add_argument("--create-scenarios", action="store_true", help="Create simulated scenarios")
    parser.add_argument("--max-duration", type=int, default=600, help="Maximum duration per video (seconds)")
    
    args = parser.parse_args()
    
    collector = DataCollector(args.output)
    
    if args.create_scenarios:
        collector.create_simulated_scenarios()
    
    if args.search_youtube:
        # Search keywords for scam calls
        keywords = [
            'scam call hindi',
            'fraud call recording',
            'phone scam india',
            'bank fraud call',
            'tech support scam'
        ]
        
        urls = collector.search_youtube_scam_calls(keywords, max_results=5)
        
        if urls:
            collector.download_youtube_audio(urls, max_duration=args.max_duration)
            collector.save_collection_log()
    
    # Create collection plan
    collector.create_collection_plan()

if __name__ == "__main__":
    main()
