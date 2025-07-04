#!/usr/bin/env python3
"""
Code Comment Remover Tool
Author: 7xmohamed
GitHub:  https://github.com/7xmohamed
Website: https://7xmohamed.com

Removes comments from source code files (Python, JavaScript, PHP, Java).
"""

import os
import re
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def remove_comments(code: str, language: str) -> str:
    if language == 'python':
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\")', '', code)
    elif language in ['javascript', 'java']:
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    elif language == 'php':
        code = re.sub(r'(//|#).*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    return '\n'.join([line for line in code.split('\n') if line.strip()])

def detect_language(filename: str) -> str:
    ext = filename.split('.')[-1].lower()
    return {
        'py': 'python',
        'js': 'javascript',
        'jsx': 'javascript',
        'java': 'java',
        'php': 'php'
    }.get(ext, None)

def process_file(input_path: str, output_path: str = None) -> bool:
    if not os.path.exists(input_path):
        print(Fore.RED + f"❌ Error: File '{input_path}' not found.")
        return False
    language = detect_language(input_path)
    if not language:
        print(Fore.RED + f"❌ Unsupported file extension: {input_path}")
        return False

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        clean_code = remove_comments(code, language)
        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_no_comments{ext}"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(clean_code)
        print(Fore.GREEN + f"\n✅ Success! Comments removed from: {os.path.basename(input_path)}")
        print(Fore.CYAN + f"📄 Clean file saved as: {os.path.basename(output_path)}")
        print(Fore.YELLOW + f"📁 Location: {os.path.dirname(os.path.abspath(output_path))}")
        return True
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {str(e)}")
        return False

def get_file_path() -> str | None:
    print(Fore.CYAN + "\n" + "="*50)
    print(Fore.MAGENTA + "🧹 Code Comment Remover Tool")
    print(Fore.CYAN + "="*50)
    print(Fore.YELLOW + "\nEnter the path to the file (or 'quit' to exit):")
    user_input = input("> ").strip()
    if user_input.lower() in ['quit', 'exit']:
        return None
    if os.path.exists(user_input):
        return user_input
    possible_path = os.path.join(os.getcwd(), user_input)
    if os.path.exists(possible_path):
        return possible_path
    print(Fore.RED + f"\n❌ File not found: {user_input}")
    return None

def get_output_option(input_path: str) -> str | None:
    base, ext = os.path.splitext(input_path)
    default_output = f"{base}_no_comments{ext}"
    print(Fore.YELLOW + "\nChoose output option:")
    print(f"1. Default: {default_output}")
    print("2. Specify custom output path")
    print("3. Overwrite original file")

    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            return None
        elif choice == '2':
            return input("Enter new file path: ").strip()
        elif choice == '3':
            confirm = input("⚠️ Overwrite original file? (y/n): ").strip().lower()
            if confirm == 'y':
                return input_path
        else:
            print(Fore.RED + "Invalid choice. Enter 1, 2, or 3.")

def main():
    while True:
        input_path = get_file_path()
        if not input_path:
            print(Fore.CYAN + "\n👋 Exiting. Goodbye!")
            break
        output_path = get_output_option(input_path)
        success = process_file(input_path, output_path)
        if success:
            again = input(Fore.BLUE + "\nProcess another file? (y/n): ").strip().lower()
            if again != 'y':
                print(Fore.CYAN + "\n👋 Done. See you!")
                break

if __name__ == "__main__":
    main()