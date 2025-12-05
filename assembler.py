import json #чтение файлов json
import sys #чтение аргументов в консоли
import os #узнать размер созданного файла

LOAD_CONST = 10
READ_MEMORY = 3
WRITE_MEMORY = 4
SGN_OPERATION = 6

def read_json(filename): #функция чтения json файла с программой, возвращает список словарей.
    try:
        with open(filename, "r",encoding="utf-8") as file:
            program = json.load(file)
        return program
    except FileNotFoundError:
        print(f"ОШИБКА: Файл '{filename}' не найден!")
        exit(1)
    except Exception as e:
        print(f"ОШИБКА: Не удалось прочитать файл '{filename}': {e}")
        exit(1)

def parse_command(command_dict): #функция растаскивающая этот словарь на отдельные переменные
    command = command_dict["command"]
    if command == "load_const":
        A=LOAD_CONST
        B=command_dict["register"]
        C=command_dict["value"]
        return A,B,C
   
    elif command == "read_mem":
        A=READ_MEMORY
        B=command_dict["register"]
        C=command_dict["memory_address"]
        return A,B,C
    elif command== "write_mem":
        A=WRITE_MEMORY
        B=command_dict["value_register"]
        C=command_dict["address_register"]
        return A,B,C
    elif command =="sgn_operation":
        A=SGN_OPERATION
        B=command_dict["base_register"]
        C=command_dict["target_register"]
        D=command_dict["offset"]
        return A,B,C,D
    else:
        raise Exception(f"Неизвестная команда: '{command}'")

def make_bytes(*args): #функция которая переводит в двоичную систему исчисления, склеивает всю команду в 40 битов
#и разбивает эти 40 битов на 5 байт в шестнадцатиричной
    if len(args) == 3:
        A, B, C = args
        a_bits = bin(A)[2:].zfill(4)
        b_bits = bin(B)[2:].zfill(5)
        c_bits = bin(C)[2:].zfill(31)
        full_bits = c_bits + b_bits + a_bits
        
    elif len(args) == 4:
        A, B, C, D = args
        a_bits = bin(A)[2:].zfill(4)
        b_bits = bin(B)[2:].zfill(5)
        c_bits = bin(C)[2:].zfill(5)
        d_bits = bin(D)[2:].zfill(12)
        full_bits = '0' * 14 + d_bits + c_bits + b_bits + a_bits
    
    bytes_list = []
    for i in range(0, 40, 8):
        byte_bits = full_bits[i:i+8]
        byte_value = int(byte_bits, 2)
        bytes_list.append(byte_value)
    
    bytes_list.reverse()
    return [f"0x{byte:02X}" for byte in bytes_list]

        
def load_const():
    print("*отработка команды load_const")

def read_mem():
    print("*отработка команды read_mem")

def write_mem():
    print("*отработка команды write_mem")

def sgn_operation():
    print("*отработка команды sgn_operation")

def write_file(output_name,hex_bytes): #Этап 2 - функция записи в файл получившихся байтов, вывод реального размера
    bytes_list = [int(h[2:], 16) for h in hex_bytes]
    with open(output_name,"wb") as output_file:
        output_file.write(bytes(bytes_list))
        print("*байты записаны в файл")
        
    size = os.path.getsize(output_name)
    print(f"размер файла:{size} байт")

def main(): 
    if len(sys.argv) < 3: #проверяем сколько аргументов в cmd 
        print("Использование: python assembler.py <входной_файл> <выходной_файл> [--test]")
        print("Пример: py assembler.py program.json output.bin --test")
        exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = "--test" in sys.argv
    
    print(f"Входной файл: {input_file}")
    print(f"Выходной файл: {output_file}")
    print(f"Режим тестирования: {'ВКЛ' if test_mode else 'ВЫКЛ'}")
    
    command_dict = read_json(input_file)
    result = parse_command(command_dict)
    
    if test_mode: #тестовый режим
    
        if len(result) == 3:
            A, B, C = result
            hex_bytes = make_bytes(A, B, C)
            print(f"Тест (A={A}, B={B}, C={C}):")
            print(", ".join(hex_bytes))
        else:
            A, B, C, D = result
            hex_bytes = make_bytes(A, B, C, D)
            print(f"Тест (A={A}, B={B}, C={C}, D={D}):")
            print(", ".join(hex_bytes))

    else: #обычный режим
        if len(result) == 3:
            A, B, C = result
            hex_bytes =make_bytes(A, B, C)

            if A == 10:
                write_file(output_file,hex_bytes)
                load_const()
                
            elif A == 3:
                write_file(output_file,hex_bytes)
                read_mem()
            elif A == 4:
                write_file(output_file,hex_bytes)
                write_mem()
        else:
            A, B, C, D = result
            hex_bytes = make_bytes(A, B, C, D)
            if A == 6:
                write_file(output_file,hex_bytes)
                sgn_operation()
if __name__ == "__main__":
    main()