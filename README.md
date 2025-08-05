
# YOU.COM Scraper

A feature-rich command-line interface for scraping and interacting with you.com's search API. This tool provides an interactive chat experience with advanced features like command system, result formatting, export functionality, auto-completion, and customizable interface.

![Banner](https://img.shields.io/badge/Python-3.6%2B-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## Features

- **Interactive Chat Mode**: Continuous conversation with you.com's AI
- **Command System**: Special commands for enhanced functionality
- **Result Formatting**: Rich text formatting with syntax highlighting and table rendering
- **Export Functionality**: Export conversations in multiple formats (TXT, MD, JSON, PDF)
- **Auto-completion**: Tab completion for commands and history
- **Customizable Interface**: Multiple themes and configurable settings
- **Conversation History**: Persistent storage of all interactions
- **Progress Indicators**: Visual feedback during searches
- **Interactive Elements**: Expandable sections and formatted responses

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Install from Source

```bash
git clone https://github.com/ousax/niceYouc0m.git
cd niceYouc0m
pip install -r requirements.txt
```

### Requirements

The script will automatically install required dependencies if they're not available:
- `pyfiglet` - For ASCII art banners
- `termcolor` - For colored terminal output
- `rich` - For advanced terminal formatting
- `pdfkit` (optional) - For PDF export functionality

## Usage

### Basic Usage

Run the script without any arguments to start interactive mode:

```bash
python nice_youc0m.py.py
```

### Command Line Arguments

```bash
python nice_youc0m.py [OPTIONS]

Options:
  -p, --prompt TEXT    Initial prompt to process
  -pa, --page INTEGER  Number of pages to search (default: 1)
  -r, --results INTEGER  Number of results per page (default: 1)
  --help               Show this message and exit
```

### Example with Initial Prompt

```bash
python nice_youc0m.py -p "What is artificial intelligence?"
```

## Command System

Once in interactive mode, you can use the following commands:

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show available commands | `/help` |
| `/history [n]` | Show conversation history (last n items) | `/history 5` |
| `/clear` | Clear conversation history | `/clear` |
| `/export [format]` | Export conversation (txt, md, json, pdf) | `/export pdf` |
| `/theme [name]` | Change color theme (default, dark, light, ocean) | `/theme dark` |
| `/settings` | Show current settings | `/settings` |
| `/reset` | Reset configuration to defaults | `/reset` |
| `/exit` | Exit the program | `/exit` |

## Customization

### Themes

The tool comes with several built-in themes:

- **default**: Standard color scheme
- **dark**: Dark theme optimized for low-light environments
- **light**: Light theme with bright colors
- **ocean**: Blue-themed color scheme

### Configuration

All settings are stored in `~/.nice_youc0m.py/config.json`. You can modify this file directly or use the `/settings` and `/theme` commands to customize your experience.

### Auto-completion

Auto-completion is enabled by default and provides:
- Command completion (type `/` then press Tab)
- History-based completion (type part of a previous prompt then press Tab)

## Export Formats

You can export your conversations in multiple formats:

- **TXT**: Plain text format with timestamps
- **MD**: Markdown format with proper formatting
- **JSON**: Structured data format for programmatic use
- **PDF**: Professional document format (requires pdfkit)

Example export command:
```
/export md
```

## Interactive Elements

The tool provides several interactive elements:

### Code Blocks

Code snippets are automatically detected and formatted with syntax highlighting:

```
```python
def hello_world():
    print("Hello, World!")
```
```

### Tables

Tabular data is automatically formatted as tables:

```
| Name | Age | Occupation |
|------|-----|------------|
| John | 30  | Developer  |
| Jane | 25  | Designer   |
```

### Progress Indicators

Visual feedback is provided during searches:

```
Searching... ████████████████████████████████████████ 100%
```

## File Structure

```
you-scraper/
├── nice_youc0m.py.py       # Main script
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .nice_youc0m.py/       # User configuration directory (created automatically)
    ├── config.json     # User settings
    └── history.json    # Conversation history
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [you.com](https://you.com) for providing the search API
- [pyfiglet](https://github.com/pwaller/pyfiglet) for ASCII art generation
- [rich](https://github.com/willmcgugan/rich) for rich terminal formatting
- [pdfkit](https://github.com/JazzCore/python-pdfkit) for PDF generation

## Disclaimer

This tool is not affiliated with or endorsed by you.com. Use responsibly and in accordance with you.com's terms of service.
