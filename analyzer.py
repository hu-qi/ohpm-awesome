#!/usr/bin/env python3
"""
Package Analyzer and Categorizer
Analyzes OpenHarmony packages and creates intelligent categorization
"""

import json
import re
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CategoryInfo:
    name: str
    emoji: str
    description: str
    keywords: Set[str]
    packages: List[Dict] = None

    def __post_init__(self):
        if self.packages is None:
            self.packages = []

class PackageAnalyzer:
    def __init__(self, packages_file: str = 'packages.json'):
        self.packages_file = packages_file
        self.packages = []
        self.categories = self._define_categories()
        self.uncategorized = []
        
    def _define_categories(self) -> Dict[str, CategoryInfo]:
        """Define intelligent categories with keywords"""
        return {
            'testing': CategoryInfo(
                name='🧪 Testing & Quality Assurance',
                emoji='🧪',
                description='Testing frameworks, unit testing, automation testing, and quality assurance tools',
                keywords={'test', 'testing', 'unit', 'automation', 'qa', 'quality', 'mock', 'assertion', 'hypium', 'spec', 'suite'}
            ),
            'ui_components': CategoryInfo(
                name='🎨 UI Components & Design',
                emoji='🎨', 
                description='UI components, design systems, layout tools, and visual elements',
                keywords={'ui', 'component', 'design', 'layout', 'button', 'dialog', 'picker', 'navigation', 'tab', 'grid', 'list', 'card', 'menu', 'banner', 'toast', 'loading', 'refresh', 'swipe', 'slider', 'input', 'form', 'calendar', 'chart', 'graph', 'visual', 'theme', 'style', 'animation', 'transition', 'gesture'}
            ),
            'utilities': CategoryInfo(
                name='🛠️ Utilities & Tools',
                emoji='🛠️',
                description='Utility libraries, helper functions, and development tools',
                keywords={'util', 'tool', 'helper', 'library', 'common', 'encrypt', 'decrypt', 'hash', 'string', 'date', 'time', 'regex', 'validation', 'format', 'convert', 'parse', 'math', 'algorithm', 'collection', 'array', 'object', 'json', 'xml', 'csv', 'log', 'debug', 'performance', 'cache', 'storage', 'file', 'io'}
            ),
            'networking': CategoryInfo(
                name='🌐 Networking & APIs',
                emoji='🌐',
                description='HTTP clients, API wrappers, networking libraries, and communication tools',
                keywords={'http', 'api', 'request', 'axios', 'fetch', 'network', 'rest', 'graphql', 'websocket', 'rpc', 'grpc', 'client', 'server', 'protocol', 'communication', 'socket', 'tcp', 'udp', 'url', 'endpoint', 'oauth', 'auth', 'jwt'}
            ),
            'data_persistence': CategoryInfo(
                name='💾 Data & Storage',
                emoji='💾',
                description='Database libraries, data persistence, storage solutions, and data management',
                keywords={'database', 'db', 'storage', 'persistence', 'sqlite', 'sql', 'orm', 'model', 'schema', 'migration', 'backup', 'sync', 'crud', 'query', 'transaction', 'cache', 'memory', 'local', 'cloud', 'preference', 'setting', 'config'}
            ),
            'media': CategoryInfo(
                name='🎵 Media & Multimedia',
                emoji='🎵',
                description='Audio, video, image processing, camera, and multimedia handling',
                keywords={'media', 'audio', 'video', 'image', 'photo', 'camera', 'player', 'recorder', 'music', 'sound', 'voice', 'multimedia', 'codec', 'format', 'stream', 'play', 'capture', 'edit', 'filter', 'effect', 'compress', 'decode', 'encode'}
            ),
            'location_maps': CategoryInfo(
                name='📍 Location & Maps',
                emoji='📍',
                description='GPS, location services, maps, navigation, and geolocation features',
                keywords={'location', 'gps', 'map', 'navigation', 'geo', 'latitude', 'longitude', 'position', 'coordinate', 'route', 'direction', 'distance', 'address', 'place', 'marker', 'pin'}
            ),
            'sensors_hardware': CategoryInfo(
                name='📱 Sensors & Hardware',
                emoji='📱',
                description='Device sensors, hardware interfaces, and system capabilities',
                keywords={'sensor', 'hardware', 'accelerometer', 'gyroscope', 'compass', 'barometer', 'fingerprint', 'biometric', 'nfc', 'bluetooth', 'wifi', 'cellular', 'battery', 'vibration', 'light', 'proximity', 'temperature', 'pressure', 'device', 'system', 'capability'}
            ),
            'security': CategoryInfo(
                name='🔒 Security & Encryption',
                emoji='🔒',
                description='Security libraries, encryption, authentication, and privacy tools',
                keywords={'security', 'encrypt', 'decrypt', 'cipher', 'crypto', 'hash', 'hmac', 'sha', 'md5', 'aes', 'rsa', 'ssl', 'tls', 'certificate', 'key', 'auth', 'authentication', 'authorization', 'oauth', 'jwt', 'token', 'password', 'biometric', 'privacy', 'secure'}
            ),
            'navigation_routing': CategoryInfo(
                name='🧭 Navigation & Routing', 
                emoji='🧭',
                description='App navigation, routing, page transitions, and navigation patterns',
                keywords={'navigation', 'router', 'route', 'nav', 'page', 'screen', 'transition', 'stack', 'tab', 'drawer', 'bottom', 'sidebar', 'breadcrumb', 'history', 'back', 'forward', 'deep', 'link'}
            ),
            'state_management': CategoryInfo(
                name='🔄 State Management',
                emoji='🔄',
                description='State management solutions, data flow, and application state handling',
                keywords={'state', 'store', 'redux', 'flux', 'observable', 'reactive', 'model', 'data', 'flow', 'context', 'provider', 'inject', 'dependency', 'service', 'singleton', 'manager'}
            ),
            'internationalization': CategoryInfo(
                name='🌍 Internationalization & Localization',
                emoji='🌍',
                description='i18n, l10n, multi-language support, and localization tools',
                keywords={'i18n', 'l10n', 'international', 'localization', 'locale', 'language', 'translation', 'translate', 'multilingual', 'region', 'country', 'currency', 'timezone', 'format', 'culture'}
            ),
            'animation': CategoryInfo(
                name='✨ Animation & Effects',
                emoji='✨',
                description='Animation libraries, visual effects, transitions, and motion design',
                keywords={'animation', 'animate', 'transition', 'effect', 'motion', 'tween', 'spring', 'easing', 'interpolation', 'keyframe', 'timeline', 'transform', 'scale', 'rotate', 'fade', 'slide', 'bounce', 'elastic', 'cubic', 'bezier'}
            ),
            'game_graphics': CategoryInfo(
                name='🎮 Gaming & Graphics',
                emoji='🎮',
                description='Game development, 3D graphics, rendering, and interactive experiences',
                keywords={'game', 'gaming', '3d', '2d', 'graphics', 'render', 'canvas', 'webgl', 'opengl', 'shader', 'texture', 'mesh', 'scene', 'physics', 'collision', 'engine', 'sprite', 'particle', 'lighting', 'material'}
            ),
            'social_sharing': CategoryInfo(
                name='📤 Social & Sharing',
                emoji='📤',
                description='Social media integration, sharing capabilities, and social features',
                keywords={'social', 'share', 'sharing', 'wechat', 'weibo', 'qq', 'facebook', 'twitter', 'instagram', 'linkedin', 'whatsapp', 'telegram', 'discord', 'chat', 'message', 'comment', 'like', 'follow', 'friend'}
            ),
            'ecommerce_payment': CategoryInfo(
                name='💰 E-commerce & Payment',
                emoji='💰',
                description='Payment processing, e-commerce features, and financial integrations',
                keywords={'payment', 'pay', 'alipay', 'wechatpay', 'bank', 'card', 'wallet', 'money', 'currency', 'price', 'order', 'cart', 'shop', 'store', 'product', 'checkout', 'invoice', 'receipt', 'transaction', 'finance', 'billing'}
            ),
            'ar_vr': CategoryInfo(
                name='🥽 AR/VR & Immersive',
                emoji='🥽',
                description='Augmented reality, virtual reality, and immersive technologies',
                keywords={'ar', 'vr', 'augmented', 'virtual', 'reality', 'immersive', '360', 'panorama', 'spatial', 'tracking', 'marker', 'recognition', 'overlay', 'hologram', 'mixed'}
            ),
            'ai_ml': CategoryInfo(
                name='🤖 AI & Machine Learning',
                emoji='🤖',
                description='Artificial intelligence, machine learning, and smart features',
                keywords={'ai', 'ml', 'machine', 'learning', 'neural', 'network', 'deep', 'model', 'prediction', 'classification', 'recognition', 'detection', 'ocr', 'nlp', 'computer', 'vision', 'tensorflow', 'pytorch', 'opencv', 'intelligent', 'smart', 'algorithm'}
            ),
            'iot': CategoryInfo(
                name='🏠 IoT & Smart Devices',
                emoji='🏠',
                description='Internet of Things, smart home, and connected device integration',
                keywords={'iot', 'smart', 'home', 'device', 'connected', 'sensor', 'automation', 'control', 'monitor', 'remote', 'wireless', 'protocol', 'gateway', 'hub', 'cloud', 'edge', 'mesh', 'zigbee', 'mqtt'}
            ),
            'productivity': CategoryInfo(
                name='📊 Productivity & Business',
                emoji='📊',
                description='Productivity tools, business applications, and enterprise solutions',
                keywords={'productivity', 'business', 'enterprise', 'office', 'document', 'pdf', 'excel', 'word', 'presentation', 'calendar', 'schedule', 'task', 'project', 'workflow', 'crm', 'erp', 'report', 'analytics', 'dashboard', 'chart', 'graph', 'statistics'}
            ),
            'education': CategoryInfo(
                name='📚 Education & Learning',
                emoji='📚',
                description='Educational apps, learning platforms, and academic tools',
                keywords={'education', 'learning', 'study', 'course', 'lesson', 'tutorial', 'quiz', 'exam', 'test', 'grade', 'student', 'teacher', 'school', 'university', 'academic', 'knowledge', 'skill', 'training', 'certification'}
            ),
            'health_fitness': CategoryInfo(
                name='💪 Health & Fitness',
                emoji='💪',
                description='Health monitoring, fitness tracking, and wellness applications',
                keywords={'health', 'fitness', 'medical', 'wellness', 'exercise', 'workout', 'sport', 'heart', 'rate', 'step', 'calorie', 'sleep', 'weight', 'bmi', 'nutrition', 'diet', 'medicine', 'hospital', 'doctor', 'patient', 'therapy'}
            ),
            'communication': CategoryInfo(
                name='💬 Communication & Messaging',
                emoji='💬',
                description='Chat, messaging, voice/video calls, and communication tools',
                keywords={'chat', 'message', 'messaging', 'communication', 'call', 'voice', 'video', 'conference', 'meeting', 'talk', 'conversation', 'notification', 'push', 'email', 'sms', 'im', 'instant'}
            )
        }
    
    def load_packages(self):
        """Load packages from JSON file"""
        with open(self.packages_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.packages = data['packages']
        logger.info(f"Loaded {len(self.packages)} packages")
    
    def _extract_text_features(self, package: Dict) -> str:
        """Extract searchable text from package"""
        text_parts = []
        
        # Add name (cleaned)
        name = package.get('name', '').lower()
        # Remove org prefix like @ohos/, @yunkss/, etc.
        clean_name = re.sub(r'^@[^/]+/', '', name)
        text_parts.append(clean_name)
        
        # Add description
        description = package.get('description', '').lower()
        text_parts.append(description)
        
        # Add keywords if available
        keywords = package.get('keywords', [])
        if isinstance(keywords, list):
            text_parts.extend([k.lower() for k in keywords])
        elif isinstance(keywords, str) and keywords:
            text_parts.append(keywords.lower())
        
        return ' '.join(text_parts)
    
    def categorize_packages(self):
        """Categorize packages based on their content"""
        categorized_count = 0
        
        for package in self.packages:
            text_features = self._extract_text_features(package)
            best_category = None
            best_score = 0
            
            # Score each category based on keyword matches
            for category_id, category in self.categories.items():
                score = 0
                for keyword in category.keywords:
                    # Exact word match gets higher score
                    if re.search(r'\b' + re.escape(keyword) + r'\b', text_features):
                        score += 2
                    # Partial match gets lower score
                    elif keyword in text_features:
                        score += 1
                
                if score > best_score:
                    best_score = score
                    best_category = category_id
            
            # Require minimum score to categorize
            if best_score >= 1:
                self.categories[best_category].packages.append(package)
                categorized_count += 1
            else:
                self.uncategorized.append(package)
        
        logger.info(f"Categorized {categorized_count} packages, {len(self.uncategorized)} uncategorized")
    
    def analyze_popular_packages(self, limit: int = 10) -> List[Dict]:
        """Get most popular packages by popularity score"""
        return sorted(self.packages, key=lambda p: p.get('popularity', 0), reverse=True)[:limit]
    
    def analyze_recent_packages(self, limit: int = 10) -> List[Dict]:
        """Get most recently updated packages"""
        return sorted(self.packages, key=lambda p: p.get('latestPublishTime', 0), reverse=True)[:limit]
    
    def get_category_stats(self) -> Dict:
        """Get statistics for each category"""
        stats = {}
        for category_id, category in self.categories.items():
            if category.packages:
                stats[category_id] = {
                    'name': category.name,
                    'count': len(category.packages),
                    'avg_popularity': sum(p.get('popularity', 0) for p in category.packages) / len(category.packages),
                    'top_package': max(category.packages, key=lambda p: p.get('popularity', 0))
                }
        
        # Sort by package count
        return dict(sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True))
    
    def _get_package_url(self, package_name: str) -> str:
        """Generate OpenHarmony registry URL for a package"""
        from urllib.parse import quote
        encoded_name = quote(package_name, safe='')
        return f"https://ohpm.openharmony.cn/#/cn/detail/{encoded_name}"
    
    def generate_readme_content(self) -> str:
        """Generate README.md content"""
        from datetime import datetime
        stats = self.get_category_stats()
        popular_packages = self.analyze_popular_packages(15)
        recent_packages = self.analyze_recent_packages(10)
        timestamp = recent_packages[0]['latestPublishTime'] if recent_packages else datetime.timestamp(datetime.now())
        date_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y%m%d') if timestamp > 0 else 'Unknown'
        
        readme = f"""# 🎯 Awesome OpenHarmony Packages

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/hu-qi/ohpm-awesome?style=flat-square)](https://github.com/hu-qi/ohpm-awesome)
[![Last Update](https://img.shields.io/badge/last%20update-{date_str}-brightgreen?style=flat-square)](https://github.com/hu-qi/ohpm-awesome)

> A curated list of awesome OpenHarmony packages, libraries, and tools for HarmonyOS development.

## 📊 Overview

- **Total Packages**: {len(self.packages):,}
- **Categories**: {len([c for c in stats.values() if c['count'] > 0])}
- **Last Updated**: Auto-updated daily

## 🔥 Most Popular Packages

"""
        
        for i, pkg in enumerate(popular_packages, 1):
            pkg_name = pkg['name']
            pkg_url = self._get_package_url(pkg_name)
            readme += f"{i}. **[{pkg_name}]({pkg_url})** - {pkg.get('description', 'No description')[:100]}{'...' if len(pkg.get('description', '')) > 100 else ''} "
            readme += f"(⭐ {pkg.get('likes', 0)} likes, 📈 {pkg.get('popularity', 0):,} popularity)\n"
        
        readme += f"\n## 🆕 Recently Updated\n\n"
        
        for i, pkg in enumerate(recent_packages, 1):
            from datetime import datetime
            pkg_name = pkg['name']
            pkg_url = self._get_package_url(pkg_name)
            timestamp = pkg.get('latestPublishTime', 0)
            date_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d') if timestamp > 0 else 'Unknown'
            readme += f"{i}. **[{pkg_name}]({pkg_url})** v{pkg.get('latestVersion', 'N/A')} - {pkg.get('description', 'No description')[:80]}{'...' if len(pkg.get('description', '')) > 80 else ''} "
            readme += f"(📅 {date_str})\n"
        
        readme += "\n## 📚 Categories\n\n"
        
        # Generate category sections
        for category_id, category in self.categories.items():
            if not category.packages:
                continue
                
            stat = stats.get(category_id, {})
            readme += f"### {category.name}\n\n"
            readme += f"{category.description}\n\n"
            readme += f"**{len(category.packages)} packages** • "
            readme += f"Avg popularity: {stat.get('avg_popularity', 0):,.0f}\n\n"
            
            # Sort packages by popularity within category
            sorted_packages = sorted(category.packages, key=lambda p: p.get('popularity', 0), reverse=True)
            
            for pkg in sorted_packages:
                pkg_name = pkg['name']
                pkg_url = self._get_package_url(pkg_name)
                readme += f"- **[{pkg_name}]({pkg_url})** - {pkg.get('description', 'No description')}"
                
                # Add metadata
                metadata = []
                if pkg.get('license'):
                    metadata.append(f"📄 {pkg['license']}")
                if pkg.get('likes', 0) > 0:
                    metadata.append(f"⭐ {pkg['likes']} likes")
                if pkg.get('latestVersion'):
                    metadata.append(f"📦 v{pkg['latestVersion']}")
                
                if metadata:
                    readme += f" ({' • '.join(metadata)})"
                readme += "\n"
            
            readme += "\n"
        
        # Add uncategorized if any
        if self.uncategorized:
            readme += f"### 📦 Other Packages\n\n"
            readme += f"Packages that don't fit into specific categories.\n\n"
            readme += f"**{len(self.uncategorized)} packages**\n\n"
            
            sorted_uncategorized = sorted(self.uncategorized, key=lambda p: p.get('popularity', 0), reverse=True)
            for pkg in sorted_uncategorized[:20]:  # Show top 20 uncategorized
                pkg_name = pkg['name']
                pkg_url = self._get_package_url(pkg_name)
                readme += f"- **[{pkg_name}]({pkg_url})** - {pkg.get('description', 'No description')[:100]}{'...' if len(pkg.get('description', '')) > 100 else ''}\n"
            
            if len(self.uncategorized) > 20:
                readme += f"\n*...and {len(self.uncategorized) - 20} more packages*\n"
            readme += "\n"
        
        readme += f"""## 🤝 Contributing

Found an awesome OpenHarmony package that's missing? Contributions are welcome!

1. Fork this repository
2. Add your package to the appropriate category
3. Create a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Auto-Update

This list is automatically updated daily using GitHub Actions to ensure the latest packages are included.

---

**Total packages tracked**: {len(self.packages):,} | **Last generated**: Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return readme

def main():
    analyzer = PackageAnalyzer()
    analyzer.load_packages()
    analyzer.categorize_packages()
    
    # Generate and save README
    readme_content = analyzer.generate_readme_content()
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Print statistics
    stats = analyzer.get_category_stats()
    print("\\n📊 Category Statistics:")
    for category_id, stat in stats.items():
        print(f"  {stat['name']}: {stat['count']} packages (avg popularity: {stat['avg_popularity']:,.0f})")
    
    print(f"\\n✅ Generated README.md with {len(analyzer.packages)} packages!")

if __name__ == "__main__":
    main()
