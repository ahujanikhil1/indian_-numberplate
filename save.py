import datetime

def write(message):
    """Write valid plate to data.txt if not already present."""
    try:
        with open("data.txt", "r") as f:
           
            result = f.read().find(message)
    except FileNotFoundError:
        with open("data.txt", "w") as f:
            f.write("")  
        result = -1 

    
    if result == -1:
        with open("data.txt", "a") as f:
            time = datetime.datetime.now()
            f.write(message + " ")
            f.write(str(time) + "\n")
        print(f"Plate saved to data.txt: {message}")
    else:
        print(f"Plate already recorded: {message}")
