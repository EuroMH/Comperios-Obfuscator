import os
import time
import zlib
import base64
import random_string
import shutil

output_dir = "./output"
pycache_dir = os.path.join(output_dir, "__pycache__")

if os.path.exists(pycache_dir):
    shutil.rmtree(pycache_dir)
if os.path.exists(os.path.join(output_dir, "obfuscated.py")):
    os.remove(os.path.join(output_dir, "obfuscated.py"))

def main():
    os.system("cls")
    is_in_dir = input("Load from this folder? (y/n) >> ").strip().lower()
    
    file_to_obf = None  

    if is_in_dir == "n":
        file_to_obf = input("Enter the path of the file to obfuscate >> ").strip()
    elif is_in_dir == "y":
        current_directory = os.getcwd()
        items = os.listdir(current_directory)
        files = [item for item in items if os.path.isfile(item)]

        non_dir_file = [(index, item) for index, item in enumerate(files, start=1)]
        
        if not non_dir_file:
            print("No files found in the current directory to obfuscate.")
            time.sleep(2)
            return
        
        for index, item in non_dir_file:
            print(f"{index}. {item}")
        
        try:
            file_to_obf_index = int(input("Choose the index of the file you want to obfuscate >> "))
            
            if 1 <= file_to_obf_index <= len(non_dir_file):
                selected_file = non_dir_file[file_to_obf_index - 1][1]
                file_to_obf = os.path.join(current_directory, selected_file)  
                print(f"You selected: {file_to_obf}")
            else:
                print("Invalid index selected. Please choose a valid index.")
                time.sleep(2)
                main()  
                return
        except ValueError:
            print("Please enter a valid integer index.")
            time.sleep(2)
            main()  
            return
        
    if file_to_obf:  
        try:
            with open(file_to_obf, "r") as file:
                content_to_obf = file.readlines()
            
        except FileNotFoundError:
            print("File doesn't exist.")
            time.sleep(3)
            main()  
            return
        except Exception as e:
            print(e)
            return

        print(f"{len(content_to_obf)} lines to obfuscate.")

        new_code = ""
        all_rdm_lines = []

        for line in content_to_obf:
            chars = []
            line_rdm = random_string.generate(32, 32, "Il")  
            if line_rdm not in all_rdm_lines:
                line_char = f"{line_rdm}="
                all_rdm_lines.append(line_rdm)
            else:
                return
            
            for character in line:
                chars.append(ord(character))
            line_char += f"{[ch for ch in chars]}"
            new_code += line_char + ";"
            chars.clear()

        if len(all_rdm_lines) == 1:
            new_code = f"{new_code}z=[chr(c) for c in {all_rdm_lines[0]}];code=''\nfor c in z:code+=c\nexec(code)"
        else:
            new_code += f"z=[]"
            for line in all_rdm_lines:
                new_code += f"\nz+=[chr(c) for c in {line}]"
            new_code += "\ncode=''\nfor p in z:code+=p\nexec(code)"

        second_step_obf_lines = new_code.splitlines()
        
        os.makedirs(output_dir, exist_ok=True)

        new_code = ""

        for line in second_step_obf_lines:
            encoded_line = base64.b64encode(line.encode('utf-8')).decode('utf-8')
            t = f"exec(__import__('base64').b64decode('{encoded_line[::-1]}'[::-1]))"
            
            compressed_t = zlib.compress(t.encode('utf-8'))
            new_code += f"exec(__import__('zlib').decompress({compressed_t}))\n"
            new_code = new_code.replace("0", "\x30").replace("1", "\x31") \
                    .replace("2", "\x32").replace("3", "\x33") \
                    .replace("4", "\x34").replace("5", "\x35") \
                    .replace("6", "\x36").replace("7", "\x37") \
                    .replace("8", "\x38").replace("9", "\x39")

        new_code_bytes = new_code.encode("utf-8")
        encoded_code = base64.a85encode(new_code_bytes)
        exec_code = f"exec(__import__('base64').a85decode({encoded_code!r}))"

        with open(os.path.join(output_dir, "obfuscated.py"), "w") as f:
            f.write(exec_code)

        os.system("py -m compileall \"./output/obfuscated.py\" ")

        with open(os.path.join(output_dir, "__pycache__", "obfuscated.cpython-313.pyc"), "rb") as f:
            compiled_content = f.read()

        if os.path.exists(pycache_dir):
            shutil.rmtree(pycache_dir)
        if os.path.exists(os.path.join(output_dir, "obfuscated.py")):
            os.remove(os.path.join(output_dir, "obfuscated.py"))

        with open(os.path.join(output_dir, "obfuscated.py"), "wb+") as f:
            f.truncate(0)
            f.write(compiled_content)

        print(f"{len(exec_code.splitlines())} obfuscated lines generated.")

    input("Finish obfuscating!\nPress enter to quit...")

if __name__ == "__main__":
    main()