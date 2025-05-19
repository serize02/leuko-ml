import os

directories = [
    ".github/workflows",
    "configs",
    "data",
    "models",
    "notebooks",
    "utils"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created: {directory}")