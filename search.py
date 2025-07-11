#!/usr/bin/env python3
"""
Package Search Tool
A CLI tool to search and filter OpenHarmony packages
"""

import json
import argparse
import re
from typing import List, Dict
import sys

class PackageSearch:
    def __init__(self, packages_file='packages.json'):
        self.packages_file = packages_file
        self.packages = []
        
    def load_packages(self):
        try:
            with open(self.packages_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.packages = data['packages']
        except FileNotFoundError:
            print(f"❌ Error: {self.packages_file} not found. Run crawler.py first.")
            sys.exit(1)
    
    def search(self, query: str, category: str = None, org: str = None, 
               license_filter: str = None, min_likes: int = 0, 
               min_popularity: int = 0, limit: int = 20) -> List[Dict]:
        """Search packages with various filters"""
        results = []
        query_lower = query.lower() if query else ""
        
        for pkg in self.packages:
            # Text search in name and description
            if query:
                name_match = query_lower in pkg.get('name', '').lower()
                desc_match = query_lower in pkg.get('description', '').lower()
                if not (name_match or desc_match):
                    continue
            
            # Organization filter
            if org and pkg.get('org', '').lower() != org.lower():
                continue
            
            # License filter
            if license_filter and pkg.get('license', '').lower() != license_filter.lower():
                continue
            
            # Minimum likes filter
            if pkg.get('likes', 0) < min_likes:
                continue
            
            # Minimum popularity filter
            if pkg.get('popularity', 0) < min_popularity:
                continue
            
            results.append(pkg)
        
        # Sort by popularity (descending)
        results.sort(key=lambda p: p.get('popularity', 0), reverse=True)
        
        return results[:limit]
    
    def _get_package_url(self, package_name: str) -> str:
        """Generate OpenHarmony registry URL for a package"""
        from urllib.parse import quote
        encoded_name = quote(package_name, safe='')
        return f"https://ohpm.openharmony.cn/#/cn/detail/{encoded_name}"
    
    def display_results(self, results: List[Dict], detailed: bool = False):
        """Display search results in a formatted way"""
        if not results:
            print("🔍 No packages found matching your criteria.")
            return
        
        print(f"🎯 Found {len(results)} packages:\\n")
        
        for i, pkg in enumerate(results, 1):
            name = pkg.get('name', 'Unknown')
            desc = pkg.get('description', 'No description')
            version = pkg.get('latestVersion', 'N/A')
            likes = pkg.get('likes', 0)
            popularity = pkg.get('popularity', 0)
            org = pkg.get('org', 'N/A')
            license_info = pkg.get('license', 'N/A')
            pkg_url = self._get_package_url(name)
            
            # Truncate description for list view
            if not detailed and len(desc) > 80:
                desc = desc[:77] + "..."
            
            print(f"{i:2d}. 📦 {name}")
            print(f"    🔗 {pkg_url}")
            print(f"    🏢 Org: {org} | 📄 License: {license_info} | 📦 v{version}")
            print(f"    ⭐ {likes} likes | 📈 {popularity:,} popularity")
            print(f"    📝 {desc}")
            
            if detailed:
                # Show additional details
                author = pkg.get('authorName', 'N/A')
                publisher = pkg.get('publisherName', 'N/A')
                print(f"    👤 Author: {author} | 🏗️  Publisher: {publisher}")
                
                # Format publish time
                timestamp = pkg.get('latestPublishTime', 0)
                if timestamp > 0:
                    from datetime import datetime
                    date_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M')
                    print(f"    📅 Last updated: {date_str}")
            
            print()
    
    def list_organizations(self):
        """List all organizations"""
        orgs = set()
        for pkg in self.packages:
            org = pkg.get('org')
            if org:
                orgs.add(org)
        
        print(f"🏢 Found {len(orgs)} organizations:")
        for org in sorted(orgs):
            count = sum(1 for pkg in self.packages if pkg.get('org') == org)
            print(f"  • {org} ({count} packages)")
    
    def list_licenses(self):
        """List all licenses"""
        licenses = {}
        for pkg in self.packages:
            license_info = pkg.get('license', 'Unknown')
            licenses[license_info] = licenses.get(license_info, 0) + 1
        
        print(f"📄 Found {len(licenses)} license types:")
        for license_info, count in sorted(licenses.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {license_info}: {count} packages")
    
    def show_stats(self):
        """Show package statistics"""
        total = len(self.packages)
        total_likes = sum(pkg.get('likes', 0) for pkg in self.packages)
        avg_popularity = sum(pkg.get('popularity', 0) for pkg in self.packages) / total if total > 0 else 0
        
        with_desc = sum(1 for pkg in self.packages if pkg.get('description'))
        unique_orgs = len(set(pkg.get('org') for pkg in self.packages if pkg.get('org')))
        unique_licenses = len(set(pkg.get('license') for pkg in self.packages if pkg.get('license')))
        
        print(f"📊 Package Statistics:")
        print(f"  • Total packages: {total:,}")
        print(f"  • Total likes: {total_likes:,}")
        print(f"  • Average popularity: {avg_popularity:,.1f}")
        print(f"  • Packages with description: {with_desc:,} ({with_desc/total*100:.1f}%)")
        print(f"  • Unique organizations: {unique_orgs}")
        print(f"  • Unique licenses: {unique_licenses}")
        
        # Top packages
        top_popular = max(self.packages, key=lambda p: p.get('popularity', 0))
        top_liked = max(self.packages, key=lambda p: p.get('likes', 0))
        
        print(f"\\n🏆 Top Packages:")
        print(f"  • Most popular: {top_popular['name']} ({top_popular['popularity']:,})")
        print(f"  • Most liked: {top_liked['name']} ({top_liked['likes']} likes)")

def main():
    parser = argparse.ArgumentParser(description='Search OpenHarmony packages')
    parser.add_argument('query', nargs='?', help='Search query (searches in name and description)')
    parser.add_argument('--org', help='Filter by organization')
    parser.add_argument('--license', help='Filter by license')
    parser.add_argument('--min-likes', type=int, default=0, help='Minimum number of likes')
    parser.add_argument('--min-popularity', type=int, default=0, help='Minimum popularity score')
    parser.add_argument('--limit', type=int, default=20, help='Maximum number of results')
    parser.add_argument('--detailed', action='store_true', help='Show detailed information')
    parser.add_argument('--list-orgs', action='store_true', help='List all organizations')
    parser.add_argument('--list-licenses', action='store_true', help='List all licenses')
    parser.add_argument('--stats', action='store_true', help='Show package statistics')
    
    args = parser.parse_args()
    
    search_tool = PackageSearch()
    search_tool.load_packages()
    
    if args.list_orgs:
        search_tool.list_organizations()
    elif args.list_licenses:
        search_tool.list_licenses()
    elif args.stats:
        search_tool.show_stats()
    else:
        results = search_tool.search(
            query=args.query,
            org=args.org,
            license_filter=args.license,
            min_likes=args.min_likes,
            min_popularity=args.min_popularity,
            limit=args.limit
        )
        search_tool.display_results(results, detailed=args.detailed)

if __name__ == "__main__":
    main()