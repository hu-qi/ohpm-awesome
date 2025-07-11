#!/usr/bin/env python3
"""
Package Insights Generator
Generates additional insights and statistics about OpenHarmony packages
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import pandas as pd
from wordcloud import WordCloud
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PackageInsights:
    def __init__(self, packages_file='packages.json'):
        self.packages_file = packages_file
        self.packages = []
        
    def load_packages(self):
        with open(self.packages_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.packages = data['packages']
        logger.info(f"Loaded {len(self.packages)} packages")
    
    def generate_popularity_trends(self):
        """Generate popularity trends visualization"""
        popularities = [pkg.get('popularity', 0) for pkg in self.packages]
        likes = [pkg.get('likes', 0) for pkg in self.packages]
        
        plt.figure(figsize=(12, 8))
        
        # Popularity distribution
        plt.subplot(2, 2, 1)
        plt.hist(popularities, bins=50, alpha=0.7, color='skyblue')
        plt.title('Package Popularity Distribution')
        plt.xlabel('Popularity Score')
        plt.ylabel('Number of Packages')
        plt.yscale('log')
        
        # Likes distribution
        plt.subplot(2, 2, 2)
        plt.hist(likes, bins=30, alpha=0.7, color='lightgreen')
        plt.title('Package Likes Distribution')
        plt.xlabel('Likes Count')
        plt.ylabel('Number of Packages')
        plt.yscale('log')
        
        # Top organizations
        orgs = [pkg.get('org', 'unknown') for pkg in self.packages if pkg.get('org')]
        org_counts = Counter(orgs).most_common(10)
        
        plt.subplot(2, 2, 3)
        orgs_names, orgs_values = zip(*org_counts)
        plt.barh(orgs_names, orgs_values, color='coral')
        plt.title('Top Organizations by Package Count')
        plt.xlabel('Number of Packages')
        
        # License distribution
        licenses = [pkg.get('license', 'Unknown') for pkg in self.packages if pkg.get('license')]
        license_counts = Counter(licenses).most_common(8)
        
        plt.subplot(2, 2, 4)
        license_names, license_values = zip(*license_counts)
        plt.pie(license_values, labels=license_names, autopct='%1.1f%%', startangle=90)
        plt.title('License Distribution')
        
        plt.tight_layout()
        plt.savefig('package_insights.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info("Generated package_insights.png")
    
    def generate_temporal_analysis(self):
        """Analyze package publishing trends over time"""
        # Convert timestamps to dates
        publish_times = []
        for pkg in self.packages:
            timestamp = pkg.get('latestPublishTime', 0)
            if timestamp > 0:
                date = datetime.fromtimestamp(timestamp / 1000)
                publish_times.append(date)
        
        if not publish_times:
            logger.warning("No valid publish times found")
            return
        
        # Create DataFrame
        df = pd.DataFrame({'publish_date': publish_times})
        df['year_month'] = df['publish_date'].dt.to_period('M')
        
        # Monthly publishing trends
        monthly_counts = df['year_month'].value_counts().sort_index()
        
        plt.figure(figsize=(12, 6))
        monthly_counts.plot(kind='line', marker='o', color='steelblue')
        plt.title('OpenHarmony Package Publishing Trends Over Time')
        plt.xlabel('Year-Month')
        plt.ylabel('Number of Package Updates')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('publishing_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info("Generated publishing_trends.png")
    
    def generate_wordcloud(self):
        """Generate word cloud from package descriptions"""
        # Collect all descriptions
        descriptions = []
        for pkg in self.packages:
            desc = pkg.get('description', '')
            if desc and len(desc.strip()) > 0:
                descriptions.append(desc)
        
        if not descriptions:
            logger.warning("No descriptions found for word cloud")
            return
        
        # Combine all descriptions
        text = ' '.join(descriptions)
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=1200, 
            height=600, 
            background_color='white',
            max_words=100,
            colormap='viridis'
        ).generate(text)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('OpenHarmony Packages - Most Common Words', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('package_wordcloud.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info("Generated package_wordcloud.png")
    
    def generate_stats_report(self):
        """Generate comprehensive statistics report"""
        stats = {
            'total_packages': len(self.packages),
            'total_likes': sum(pkg.get('likes', 0) for pkg in self.packages),
            'avg_popularity': sum(pkg.get('popularity', 0) for pkg in self.packages) / len(self.packages),
            'unique_orgs': len(set(pkg.get('org', '') for pkg in self.packages if pkg.get('org'))),
            'unique_licenses': len(set(pkg.get('license', '') for pkg in self.packages if pkg.get('license'))),
            'packages_with_description': len([pkg for pkg in self.packages if pkg.get('description')]),
            'most_popular': max(self.packages, key=lambda p: p.get('popularity', 0)),
            'most_liked': max(self.packages, key=lambda p: p.get('likes', 0)),
            'top_orgs': Counter(pkg.get('org', 'unknown') for pkg in self.packages if pkg.get('org')).most_common(5),
            'top_licenses': Counter(pkg.get('license', 'Unknown') for pkg in self.packages if pkg.get('license')).most_common(5)
        }
        
        # Save stats to JSON
        with open('package_stats.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info("Generated package_stats.json")
        return stats

def main():
    try:
        insights = PackageInsights()
        insights.load_packages()
        
        logger.info("Generating insights...")
        insights.generate_popularity_trends()
        insights.generate_temporal_analysis()
        insights.generate_wordcloud()
        stats = insights.generate_stats_report()
        
        print("📊 Package Insights Generated:")
        print(f"  • Total Packages: {stats['total_packages']:,}")
        print(f"  • Total Likes: {stats['total_likes']:,}")
        print(f"  • Average Popularity: {stats['avg_popularity']:,.1f}")
        print(f"  • Unique Organizations: {stats['unique_orgs']}")
        print(f"  • Unique Licenses: {stats['unique_licenses']}")
        print(f"  • Most Popular: {stats['most_popular']['name']} ({stats['most_popular']['popularity']:,})")
        print(f"  • Most Liked: {stats['most_liked']['name']} ({stats['most_liked']['likes']} likes)")
        
        print("\\n📁 Generated Files:")
        print("  • package_insights.png - Popularity and distribution charts")
        print("  • publishing_trends.png - Publishing trends over time")
        print("  • package_wordcloud.png - Word cloud of descriptions")
        print("  • package_stats.json - Detailed statistics")
        
    except ImportError as e:
        print(f"⚠️  Optional dependencies missing: {e}")
        print("📦 To generate visualizations, install: pip install matplotlib seaborn pandas wordcloud")
        # Still generate basic stats without visualizations
        insights = PackageInsights()
        insights.load_packages()
        stats = insights.generate_stats_report()
        print("📊 Basic statistics generated in package_stats.json")

if __name__ == "__main__":
    main()