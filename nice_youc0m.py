
import json
import requests
import time
from urllib.parse import quote
import re
import argparse
import random
import sys
import os
import readline
import glob
from datetime import datetime
from pathlib import Path
try:
    from pyfiglet import Figlet
    FIGLET_AVAILABLE = True
except ImportError:
    print("Installing required pyfiglet library...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet"])
    from pyfiglet import Figlet
    FIGLET_AVAILABLE = True

try:
    from termcolor import colored
    TERMCOLOR_AVAILABLE = True
except ImportError:
    print("Installing required termcolor library...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "termcolor"])
    from termcolor import colored
    TERMCOLOR_AVAILABLE = True

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    print("Installing required rich library...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True

try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    print("pdfkit not available. PDF export will be disabled.")
    PDFKIT_AVAILABLE = False
COLORS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
THEMES = {
    'default': {
        'banner': 'slant',
        'primary': 'cyan',
        'secondary': 'blue',
        'success': 'green',
        'warning': 'yellow',
        'error': 'red',
        'info': 'magenta'
    },
    'dark': {
        'banner': 'slant',
        'primary': 'white',
        'secondary': 'cyan',
        'success': 'green',
        'warning': 'yellow',
        'error': 'red',
        'info': 'blue'
    },
    'light': {
        'banner': 'slant',
        'primary': 'blue',
        'secondary': 'cyan',
        'success': 'green',
        'warning': 'yellow',
        'error': 'red',
        'info': 'magenta'
    },
    'ocean': {
        'banner': 'slant',
        'primary': 'cyan',
        'secondary': 'blue',
        'success': 'green',
        'warning': 'yellow',
        'error': 'red',
        'info': 'white'
    }
}

CONFIG_DIR = os.path.expanduser("~/.you_scraper")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
HISTORY_FILE = os.path.join(CONFIG_DIR, "history.json")

class Config:
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self):
        default_config = {
            "theme": "default",
            "banner_font": "slant",
            "auto_completion": True,
            "max_history": 100,
            "export_format": "txt"
        }
        
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
            
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except:
                return default_config
        return default_config
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()

class History:
    def __init__(self, max_items=100):
        self.max_items = max_items
        self.history = self.load_history()
        
    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history[-self.max_items:], f, indent=2)
    
    def add(self, prompt, response):
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response
        })
        self.save_history()
    
    def clear(self):
        self.history = []
        self.save_history()
    
    def get(self, limit=None):
        if limit:
            return self.history[-limit:]
        return self.history

class CommandSystem:
    def __init__(self, config, history):
        self.config = config
        self.history = history
        self.commands = {
            "/help": self.show_help,
            "/history": self.show_history,
            "/clear": self.clear_history,
            "/export": self.export_conversation,
            "/theme": self.change_theme,
            "/settings": self.show_settings,
            "/reset": self.reset_config,
            "/exit": self.exit_program
        }
        
    def process(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        
        if cmd in self.commands:
            return self.commands[cmd](args)
        else:
            return colored(f"Unknown command: {cmd}. Type /help for available commands.", "red")
    
    def show_help(self, args):
        help_text = """
        Available Commands:
        
        /help           - Show this help message
        /history [n]    - Show conversation history (last n items, default 10)
        /clear          - Clear conversation history
        /export [format]- Export conversation (txt, md, json, pdf)
        /theme [name]   - Change color theme (default, dark, light, ocean)
        /settings       - Show current settings
        /reset          - Reset configuration to defaults
        /exit           - Exit the program
        """
        return colored(help_text, "blue")
    
    def show_history(self, args):
        limit = int(args[0]) if args and args[0].isdigit() else 10
        history = self.history.get(limit)
        
        if not history:
            return colored("No conversation history yet.", "yellow")
        
        output = ""
        for i, item in enumerate(history, 1):
            timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            output += f"\n[{i}] {timestamp}\n"
            output += colored(f"> {item['prompt']}\n", "green")
            output += f"{item['response'][:100]}{'...' if len(item['response']) > 100 else ''}\n"
        
        return output
    
    def clear_history(self, args):
        self.history.clear()
        return colored("Conversation history cleared.", "green")
    
    def export_conversation(self, args):
        format_type = args[0] if args else self.config.get("export_format", "txt")
        history = self.history.get()
        
        if not history:
            return colored("No conversation history to export.", "yellow")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"you_export_{timestamp}.{format_type}"
        
        try:
            if format_type == "txt":
                self._export_txt(history, filename)
            elif format_type == "md":
                self._export_md(history, filename)
            elif format_type == "json":
                self._export_json(history, filename)
            elif format_type == "pdf":
                if PDFKIT_AVAILABLE:
                    self._export_pdf(history, filename)
                else:
                    return colored("PDF export requires pdfkit library. Install with: pip install pdfkit", "red")
            else:
                return colored(f"Unsupported export format: {format_type}", "red")
            
            return colored(f"Conversation exported to {filename}", "green")
        except Exception as e:
            return colored(f"Export failed: {str(e)}", "red")
    
    def _export_txt(self, history, filename):
        with open(filename, 'w') as f:
            for item in history:
                timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}]\n")
                f.write(f"> {item['prompt']}\n")
                f.write(f"{item['response']}\n\n")
    
    def _export_md(self, history, filename):
        with open(filename, 'w') as f:
            f.write("# YOU.COM Conversation Export\n\n")
            for item in history:
                timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"## {timestamp}\n\n")
                f.write(f"**Prompt:** {item['prompt']}\n\n")
                f.write(f"**Response:**\n\n{item['response']}\n\n---\n\n")
    
    def _export_json(self, history, filename):
        with open(filename, 'w') as f:
            json.dump(history, f, indent=2)
    
    def _export_pdf(self, history, filename):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>YOU.COM Conversation Export</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .timestamp { color: #666; font-size: 0.9em; }
                .prompt { font-weight: bold; color: #0066cc; }
                .response { margin-bottom: 20px; }
            </style>
        </head>
        <body>
        <h1>YOU.COM Conversation Export</h1>
        """
        
        for item in history:
            timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            html_content += f"""
            <div class="timestamp">{timestamp}</div>
            <div class="prompt">Prompt: {item['prompt']}</div>
            <div class="response">{item['response']}</div>
            <hr>
            """
        
        html_content += "</body></html>"
        pdfkit.from_string(html_content, filename)
    
    def change_theme(self, args):
        if not args:
            themes = ", ".join(THEMES.keys())
            return colored(f"Available themes: {themes}", "blue")
        
        theme_name = args[0].lower()
        if theme_name in THEMES:
            self.config.set("theme", theme_name)
            return colored(f"Theme changed to {theme_name}", "green")
        else:
            themes = ", ".join(THEMES.keys())
            return colored(f"Unknown theme: {theme_name}. Available themes: {themes}", "red")
    
    def show_settings(self, args):
        settings = self.config.config
        output = "Current Settings:\n\n"
        for key, value in settings.items():
            output += f"{key}: {value}\n"
        return output
    
    def reset_config(self, args):
        self.config.config = Config().load_config()
        self.config.save_config()
        return colored("Configuration reset to defaults.", "green")
    
    def exit_program(self, args):
        raise KeyboardInterrupt

class AutoCompleter:
    def __init__(self, commands, history):
        self.commands = commands
        self.history = history
        self.matches = []
        readline.set_completer(self.complete)
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(" \t\n")
    
    def complete(self, text, state):
        if state == 0:
            line = readline.get_line_buffer()
            
            if line.startswith("/"):
                options = [cmd for cmd in self.commands if cmd.startswith(text)]
            else:
                options = [item["prompt"] for item in self.history.get() if item["prompt"].startswith(text)]
            
            self.matches = sorted(options)
        
        try:
            return self.matches[state]
        except IndexError:
            return None

class ResultFormatter:
    def __init__(self, theme):
        self.theme = theme
        self.console = Console() if RICH_AVAILABLE else None
    
    def format(self, text):
        if not RICH_AVAILABLE:
            return text
        text = re.sub(r'```(\w+)?\n(.*?)\n```', self._format_code, text, flags=re.DOTALL)
        
        if re.search(r'\|.*\|.*\|', text):
            text = self._format_table(text)
        try:
            md = Markdown(text)
            with self.console.capture() as capture:
                self.console.print(md)
            return capture.get()
        except:
            return text
    
    def _format_code(self, match):
        language = match.group(1) or "text"
        code = match.group(2)
        
        syntax = Syntax(code, language, theme="monokai", line_numbers=False)
        with self.console.capture() as capture:
            self.console.print(Panel(syntax, title=f"Code ({language})"))
        return capture.get()
    
    def _format_table(self, text):
        lines = text.split('\n')
        table_lines = []
        in_table = False
        
        for line in lines:
            if '|' in line:
                if not in_table:
                    table = Table(title="Data Table")
                    in_table = True
                
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if not table.columns:
                    for cell in cells:
                        table.add_column(cell)
                else:
                    table.add_row(*cells)
            else:
                if in_table:
                    with self.console.capture() as capture:
                        self.console.print(table)
                    table_lines.append(capture.get())
                    in_table = False
                table_lines.append(line)
        
        if in_table:
            with self.console.capture() as capture:
                self.console.print(table)
            table_lines.append(capture.get())
        
        return '\n'.join(table_lines)

class YOU:
    """
    Simple class that uses you.com service to scrap the answer of a given prompt
    """
    def __init__(self, prompt, page=1, count=1, theme="default"):
        self.prompt = prompt
        self.page = page
        self.count = count
        self.theme = theme
        self.formatter = ResultFormatter(theme)
    
    def GenerateAnswer(self):
        """
        https://you.com/api/streamingSearch?q=qu%27est%20ce%20qu%27on%20entend%20par%20la%20comptabilit%C3%A9%20g%C3%A9n%C3%A9rale&page=1&count=1&safeSearch=Moderate&mkt=en-US&responseFilter=WebPages,Translations,TimeZone,Computation,RelatedSearches&domain=youchat&use_personalization_extraction=true
        """
        self.prompt = quote(self.prompt)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Host": "you.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-User": "?1"
        }
        
        API = f"https://you.com/api/streamingSearch?q={self.prompt}&page={self.page}&count={self.count}&safeSearch=Moderate&mkt=en-US&responseFilter=WebPages,Translations,TimeZone,Computation,RelatedSearches&domain=youchat&use_personalization_extraction=true"
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                task = progress.add_task("Searching...", total=None)
                
                reqApi = requests.get(API, headers=headers, timeout=20, allow_redirects=False)
                progress.update(task, completed=True)
            
            if reqApi.ok:
                sse_response = reqApi.text
                paragraph = ""
                events = sse_response.strip().split("\n\n")
                
                for event in events:
                    if not event:
                        continue
                    
                    event_lines = event.split("\n")
                    event_type = None
                    event_data = None
                    
                    for line in event_lines:
                        if line.startswith("event:"):
                            event_type = line.split("event:")[1].strip()
                        elif line.startswith("data:"):
                            event_data = line.split("data:")[1].strip()
                    
                    if event_type == "youChatToken" and event_data:
                        try:
                            data = json.loads(event_data)
                            if "youChatToken" in data:
                                paragraph += data["youChatToken"]
                        except json.JSONDecodeError:
                            pass
                    
                    elif event_type == "done":
                        break
                
                formatted_response = self.formatter.format(paragraph.strip())
                return formatted_response
            else:
                return colored(f"Error: API request failed with status code {reqApi.status_code}", "red")
        
        except requests.RequestException as e:
            return colored(f"Error: Network request failed - {str(e)}", "red")
        except Exception as e:
            return colored(f"Error: {str(e)}", "red")

def display_banner(theme):
    """Display a random colored banner"""
    theme_colors = THEMES.get(theme, THEMES["default"])
    banner_color = theme_colors["primary"]
    
    if FIGLET_AVAILABLE and TERMCOLOR_AVAILABLE:
        f = Figlet(font=theme_colors["banner"])
        banner_text = f.renderText('YOU.COM SCRAPER')
        print(colored(banner_text, banner_color))
        print(colored("=" * 60, banner_color))
        print(colored("A feature-rich web scraper for you.com\nBy Ousax", banner_color))
        print(colored("Type /help for available commands", banner_color))
        print(colored("Press Ctrl+C to exit", banner_color))
        print(colored("=" * 60, banner_color))
    else:
        print("YOU.COM SCRAPER")
        print("=" * 60)
        print("A feature-rich web scraper for you.com\nBy Ousax")
        print("Type /help for available commands")
        print("Press Ctrl+C to exit")
        print("=" * 60)

def main():
    config = Config()
    history = History(max_items=config.get("max_history", 100))
    
    display_banner(config.get("theme", "default"))
    
    parser = argparse.ArgumentParser(description="You.com Scraper - Interactive Chat Mode")
    parser.add_argument("-p", "--prompt", help="Initial prompt", type=str, default=None)
    parser.add_argument("-pa", "--page", help="Number of the pages", type=int, default=1)
    parser.add_argument("-r", "--results", help="Results count", type=int, default=1)
    args = parser.parse_args()
    
    command_system = CommandSystem(config, history)
    
    if config.get("auto_completion", True):
        AutoCompleter(command_system.commands, history)
    
    if args.prompt:
        you = YOU(args.prompt, args.page, args.results, config.get("theme", "default"))
        answer = you.GenerateAnswer()
        print(colored("\n🤖 YOU.COM:", "cyan"))
        print(answer)
        history.add(args.prompt, answer)
    
    try:
        while True:
            try:
                print(colored("\n💬 Enter your prompt (or /help for commands):", "green"))
                user_input = input("> ")
                
                if not user_input.strip():
                    print(colored("Please enter a valid prompt.", "yellow"))
                    continue
                
                if user_input.startswith("/"):
                    result = command_system.process(user_input)
                    print(result)
                    continue
                
                you = YOU(user_input, args.page, args.results, config.get("theme", "default"))
                answer = you.GenerateAnswer()
                
                print(colored("\n🤖 YOU.COM:", "cyan"))
                print(answer)
                history.add(user_input, answer)
                
            except KeyboardInterrupt:
                print(colored("\n\nOperation cancelled. Try again or press Ctrl+C to exit.", "yellow"))
                sys.exit(0)
                
    except KeyboardInterrupt:
        print(colored("\n\n👋 Thank you for using YOU.COM SCRAPER. Goodbye!", "magenta"))
        sys.exit(0)

if __name__ == "__main__":
    main()
