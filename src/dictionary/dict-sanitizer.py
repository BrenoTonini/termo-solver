import os

dictionary_path = os.path.join(os.path.dirname(__file__), 'dict-ptbr.txt')
output_path = os.path.join(os.path.dirname(__file__), 'valid-inputs.txt')

def sanitize_dictionary():
    """
    gera um novo arquivo de dicionário contendo apenas as palavras de 5 letras.

    return None: O arquivo 'valid-inputs.txt' é criado ou sobrescrito com as palavras válidas.
    """
    valid_words = []

    with open(dictionary_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        word = line.strip()
        if len(word) == 5:
            valid_words.append(word)

    print("Total inputs válidos (5 letras)", len(valid_words))

    with open(output_path, 'w') as file:
        for word in valid_words:
            file.write(word)
            if not word == valid_words[-1]:
                file.write('\n')

if __name__ == "__main__":
    sanitize_dictionary()