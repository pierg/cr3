

def save_lists_to_files(x, ya, yb):
    # Save the x list to a file
    with open("x_values.txt", "w") as f:
        for item in x:
            f.write(str(item) + "\n")

    # Save the ya list to a file
    with open("ya_values.txt", "w") as f:
        for item in ya:
            f.write(str(item) + "\n")

    # Save the yb list to a file
    with open("yb_values.txt", "w") as f:
        for item in yb:
            f.write(str(item) + "\n")


def import_lists_from_files():
    # Import the x list from a file
    with open("x_values.txt", "r") as f:
        x = [float(line.strip()) for line in f]

    # Import the ya list from a file
    with open("ya_values.txt", "r") as f:
        ya = [float(line.strip()) for line in f]

    # Import the yb list from a file
    with open("yb_values.txt", "r") as f:
        yb = [float(line.strip()) for line in f]
    return x,ya,yb
