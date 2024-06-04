def extract_groq_key(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("GROQ_KEY="):
                    groq_key = line.strip().split('=', 1)[1]
                    return groq_key
        print("Grog_key lipseste din secrets.txt!")
        return None 
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None