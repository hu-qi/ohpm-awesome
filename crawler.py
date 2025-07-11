#!/usr/bin/env python3
"""
OpenHarmony Package Crawler
A high-performance crawler to fetch all OpenHarmony packages from OHPM registry
"""

import asyncio
import aiohttp
import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Package:
    name: str
    description: str
    org: str
    packageType: str
    latestVersion: str
    latestPublishTime: int
    license: str
    authorName: str
    publisherId: str
    publisherName: str
    authorPicUrl: str
    likes: int
    points: int
    popularity: int

class OHPMCrawler:
    def __init__(self, base_url: str = "https://ohpm.openharmony.cn/ohpmweb/registry/oh-package/openapi/v1/search"):
        self.base_url = base_url
        self.session = None
        self.packages: List[Package] = []
        
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=20)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Referer': 'https://ohpm.openharmony.cn/'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, page_num: int, page_size: int = 50) -> Dict[str, Any]:
        """Fetch a single page of packages"""
        params = {
            'condition': '',
            'pageNum': page_num,
            'pageSize': page_size,
            'sortedType': 'popularity',
            'isHomePage': 'false'
        }
        
        try:
            async with self.session.get(self.base_url, params=params) as response:
                text = await response.text()
                logger.info(f"Response status: {response.status}, content length: {len(text)}")
                
                if response.status != 200:
                    logger.error(f"HTTP {response.status} for page {page_num}: {text[:500]}")
                    return {}
                
                try:
                    data = json.loads(text)
                    logger.info(f"Response structure: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                    if isinstance(data, dict) and 'body' in data:
                        body = data['body']
                        if isinstance(body, dict) and 'rows' in body:
                            logger.info(f"Body rows field type: {type(body['rows'])}, length: {len(body.get('rows', []))}")
                            if len(body.get('rows', [])) > 0:
                                logger.info(f"First package keys: {list(body['rows'][0].keys()) if body['rows'] else 'No packages'}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}, response: {text[:500]}")
                    return {}
                
                logger.info(f"Fetched page {page_num}/{data.get('body', {}).get('pages', '?')} - {len(data.get('body', {}).get('rows', []))} packages")
                return data
        except Exception as e:
            logger.error(f"Error fetching page {page_num}: {e}")
            return {}
    
    async def fetch_all_packages(self) -> List[Package]:
        """Fetch all packages using concurrent requests"""
        # First, get the total number of pages
        first_page = await self.fetch_page(1)
        if not first_page or 'body' not in first_page:
            logger.error("Failed to get initial page data")
            return []
        
        # Extract actual data from body
        body_data = first_page['body']
        if not body_data or 'pages' not in body_data:
            logger.error("Invalid body structure in response")
            return []
        
        total_pages = body_data['pages']
        total_packages = body_data['total']
        logger.info(f"Total packages: {total_packages}, Total pages: {total_pages}")
        
        # Process first page
        self._process_page_data(body_data)
        
        # Create tasks for remaining pages
        tasks = []
        for page_num in range(2, total_pages + 1):
            task = asyncio.create_task(self.fetch_page(page_num))
            tasks.append(task)
        
        # Execute all requests concurrently
        logger.info(f"Fetching {len(tasks)} remaining pages concurrently...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Task failed: {result}")
            elif result and 'body' in result:
                self._process_page_data(result['body'])
        
        logger.info(f"Successfully crawled {len(self.packages)} packages")
        return self.packages
    
    def _process_page_data(self, page_data: Dict[str, Any]):
        """Process page data and extract packages"""
        if not page_data or 'rows' not in page_data:
            return
        
        for pkg_data in page_data['rows']:
            try:
                package = Package(
                    name=pkg_data.get('name', ''),
                    description=pkg_data.get('description', ''),
                    org=pkg_data.get('org', ''),
                    packageType=pkg_data.get('packageType', ''),
                    latestVersion=pkg_data.get('latestVersion', ''),
                    latestPublishTime=pkg_data.get('latestPublishTime', 0),
                    license=pkg_data.get('license', ''),
                    authorName=pkg_data.get('authorName', ''),
                    publisherId=pkg_data.get('publisherId', ''),
                    publisherName=pkg_data.get('publisherName', ''),
                    authorPicUrl=pkg_data.get('authorPicUrl', ''),
                    likes=pkg_data.get('likes', 0),
                    points=pkg_data.get('points', 0),
                    popularity=pkg_data.get('popularity', 0)
                )
                self.packages.append(package)
            except Exception as e:
                logger.warning(f"Error processing package data: {e}")
    
    def save_to_json(self, filename: str = 'packages.json'):
        """Save packages to JSON file"""
        packages_dict = [asdict(pkg) for pkg in self.packages]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'crawled_at': datetime.now().isoformat(),
                'total_packages': len(self.packages),
                'packages': packages_dict
            }, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(self.packages)} packages to {filename}")

async def main():
    """Main crawler function"""
    start_time = time.time()
    
    async with OHPMCrawler() as crawler:
        packages = await crawler.fetch_all_packages()
        crawler.save_to_json()
    
    end_time = time.time()
    logger.info(f"Crawling completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())