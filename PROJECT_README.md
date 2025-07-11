# 🚀 OHPM Awesome - OpenHarmony Package Manager Awesome List

This project automatically crawls and categorizes all OpenHarmony packages from the official OHPM registry to create a comprehensive awesome list.

## 🎯 Features

- **🕷️ High-Performance Crawler**: Asynchronous crawler that fetches all packages in under 1 second
- **🧠 Intelligent Categorization**: AI-powered categorization system with 22+ categories
- **📊 Rich Analytics**: Package insights, trends, and statistics
- **🔍 Advanced Search**: CLI search tool with multiple filters
- **🤖 Auto-Updates**: GitHub Actions workflow for daily updates
- **📈 Visualizations**: Charts, word clouds, and trend analysis

## 📁 Project Structure

```
ohpm-awesome/
├── crawler.py          # High-performance package crawler
├── analyzer.py         # Package categorization and README generation
├── search.py          # CLI search and filter tool
├── insights.py        # Analytics and visualization generator
├── packages.json      # Raw package data (auto-generated)
├── README.md          # Main awesome list (auto-generated)
└── .github/workflows/ # GitHub Actions for automation
```

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/nutpi/ohpm-awesome.git
cd ohpm-awesome

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Crawl Packages
```bash
python crawler.py
```

### Generate Categorized README
```bash
python analyzer.py
```

### Search Packages
```bash
# Basic search
python search.py "animation"

# Advanced search with filters
python search.py "ui" --org "ohos" --min-likes 10 --detailed

# List organizations
python search.py --list-orgs

# Show statistics
python search.py --stats
```

### Generate Insights
```bash
python insights.py
```

## 📊 Package Categories

The system automatically categorizes packages into 22+ intelligent categories:

- 🧪 **Testing & Quality Assurance** - Testing frameworks and QA tools
- 🎨 **UI Components & Design** - UI components and design systems
- 🛠️ **Utilities & Tools** - Helper libraries and development tools
- 🌐 **Networking & APIs** - HTTP clients and API integrations
- 💾 **Data & Storage** - Database and storage solutions
- 🎵 **Media & Multimedia** - Audio, video, and image processing
- 📍 **Location & Maps** - GPS and mapping services
- 📱 **Sensors & Hardware** - Device sensors and hardware interfaces
- 🔒 **Security & Encryption** - Security and encryption libraries
- 🧭 **Navigation & Routing** - App navigation and routing
- 🔄 **State Management** - State management solutions
- 🌍 **Internationalization** - i18n and localization tools
- ✨ **Animation & Effects** - Animation libraries and effects
- 🎮 **Gaming & Graphics** - Game development and graphics
- 📤 **Social & Sharing** - Social media integration
- 💰 **E-commerce & Payment** - Payment and e-commerce features
- 🥽 **AR/VR & Immersive** - Augmented and virtual reality
- 🤖 **AI & Machine Learning** - AI and ML capabilities
- 🏠 **IoT & Smart Devices** - Internet of Things integration
- 📊 **Productivity & Business** - Business and productivity tools
- 📚 **Education & Learning** - Educational applications
- 💪 **Health & Fitness** - Health and fitness tracking
- 💬 **Communication & Messaging** - Chat and messaging tools

## 🤖 Automation

The project includes a GitHub Actions workflow that:

- Runs daily at 00:00 UTC (8:00 AM Beijing time)
- Crawls all packages from OHPM registry
- Updates categorization and generates new README
- Commits changes automatically
- Provides detailed update summaries

## 📈 Statistics

Current package statistics:
- **Total Packages**: 1,808+
- **Categories**: 22+
- **Categorization Rate**: 90%+
- **Update Frequency**: Daily
- **Crawl Speed**: < 1 second

## 🔧 Technical Details

### Crawler Features
- Asynchronous HTTP requests for maximum performance
- Intelligent rate limiting and error handling
- Comprehensive data extraction (name, description, popularity, etc.)
- Robust error handling and retry logic

### Categorization Algorithm
- Keyword-based scoring system
- Multiple matching strategies (exact word, partial match)
- Confidence thresholds to ensure quality
- Extensible category system

### Search Capabilities
- Full-text search in names and descriptions
- Multiple filters (organization, license, popularity, likes)
- Sorting by popularity
- Detailed and summary view modes

## 🤝 Contributing

Contributions are welcome! You can:

1. **Add new categories**: Extend the categorization system
2. **Improve algorithms**: Enhance search and categorization
3. **Add features**: New analysis tools or visualizations
4. **Fix bugs**: Report and fix issues
5. **Documentation**: Improve guides and documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenHarmony community for the amazing ecosystem
- OHPM registry for providing the package data
- All package authors and maintainers

---

**Auto-generated and updated daily** | [View the awesome list](README.md) | [Search packages](search.py)