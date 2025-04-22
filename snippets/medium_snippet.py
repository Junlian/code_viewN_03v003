def fibonacci_seq(n):
    """Generate a Fibonacci sequence up to n terms."""
    result = []
    a, b = 0, 1
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

def print_sequence(sequence):
    """Print a sequence with indices."""
    for i, num in enumerate(sequence):
        print(f"F({i}) = {num}")

def main():
    # Generate and print first 10 Fibonacci numbers
    n = 10
    print(f"First {n} Fibonacci numbers:")
    seq = fibonacci_seq(n)
    print_sequence(seq)
    
# Call the main function
if __name__ == "__main__":
    main()