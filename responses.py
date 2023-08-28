

def handle(message:str, channel:str, server:str, prefix:str) -> str:
    full_message = message
    message = message.lower()

    if message == f"{prefix}example":
        return "Example Message"
    
    elif message.startswith(f"{prefix}prefix"):
        new_prefix = message.removeprefix(f"{prefix}prefix ")
        if message == f"{prefix}prefix" or new_prefix.endswith(" "):
            return f"# Prefix syntax\n{prefix}prefix <string>"
        
        else:
            if new_prefix == prefix:
                return f"Prefix is already *{prefix}*"
            
            else:
                with open(f"data/server/{server}/prefix.txt", "w") as f:
                    f.write(new_prefix)

                print(f"Changed prefix in server: '{server}' to {new_prefix}")
                return f"Changed prefix from: *{prefix}* to: *{new_prefix}*"