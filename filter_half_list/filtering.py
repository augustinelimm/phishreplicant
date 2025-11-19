def keep_even_lines(input_file, output_file):
    """
    Remove odd-numbered lines (1, 3, 5, ...) and keep even-numbered lines (2, 4, 6, ...)
    """
    with open("tobefiltered.txt", 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        
        # Keep lines at indices 1, 3, 5... (which are lines 2, 4, 6... in 1-based counting)
        for i in range(1, len(lines), 2):  # Start at index 1, step by 2
            outfile.write(lines[i])
    
    print(f"Processed {len(lines)} lines")
    print(f"Kept {len(range(1, len(lines), 2))} even-numbered lines")
    print(f"Output saved to: {output_file}")

# Usage
keep_even_lines('input.txt', 'output.txt')