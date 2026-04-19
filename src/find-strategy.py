import os

def character_occurrences():
    file_path = os.path.join(os.path.dirname(__file__), 'dictionary', 'valid-inputs.txt')
    lines = open(file_path).readlines()
    occurrences = {}
    for line in lines:
        for char in line.strip():
            if char not in occurrences:
                occurrences[char] = 0
            occurrences[char] += 1
    return occurrences

def start():
    occurrences = character_occurrences()
    sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_occurrences:
        print(f"{char}: {count}")


if __name__ == "__main__":
    start()