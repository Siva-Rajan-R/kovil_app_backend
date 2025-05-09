import re

async def clean_phone_numbers(input_string:str):
    # Find all digit sequences and join them with a hyphen
    numbers = re.findall(r'\d+', input_string)
    return ','.join(numbers)

# # Example usage
# input_string = "1234567890-1234567890,1234567890 1234567890"
# cleaned = clean_phone_numbers(input_string)
# print("Cleaned phone numbers:", cleaned)
