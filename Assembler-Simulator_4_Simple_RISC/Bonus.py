from math import *
import sys

def cell_size_gen(in2):
    if (in2==1):
        cell_size =1
    if (in2==2):
        cell_size =4
    if (in2==3):
        cell_size =8
    if (in2==4):
        cell_size = ceil(log2(sys.maxsize))+1
    return cell_size

def extract_num_from_string(st):
    num=0
    for x in st:
        if x.isdigit():
            num=num*10 + int(x)

    return num

def bits_calculate(num, G_K_M, B_b):

    if (G_K_M in ["G", "g"]):
        num*=1024*1024*1024
    elif (G_K_M in ["M", "m"]):
        num*=1024*1024
    elif (G_K_M in ["K", "k"]):
        num*=1024

    if B_b=="B":
        num*=8
    
    return num

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
in1 = input("Enter Memory Space: ")  #input memory space

mem_space = extract_num_from_string(in1) # take the number before the unit

mem_space= bits_calculate(mem_space, in1[-2], in1[-1])  #convert entered memory space to bits

in2 = int(input("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Bit Addressable Memory
2. Nibble Addressable Memory
3. Byte Addressable Memory
4. Word Addressable Memory

Choose the type of Memory Addresability (Enter option number): """))
cell_size= cell_size_gen(in2)

choice = int(input("\nEnter Query number: "))
if (choice==1) :
    
    print()
    instruction_len= int(input("Enter Length of an INSTRUCTION (in bits): "))
    register_len= int(input("Enter Length of a REGISTER (in bits): "))

    address_len=log2(mem_space/cell_size)
    opcode_len = instruction_len-register_len-address_len
    filler_bits = instruction_len-(2*register_len)-opcode_len
    if (filler_bits<0):
        filler_bits = 0

    print("\nMinimum number of bit needed to represent an address:", int(address_len))
    print("Number of bits needed by opcode:", int(opcode_len))
    print("Number of filler bits in Instruction type 2:", int(filler_bits))
    print("Maximum number of instructions supported:", int(pow(2, opcode_len)))
    print("Maximum number of registers supported:", int(pow(2, register_len)))

else:
    q2_type = int(input("Enter the Type of System Enhancement Query (1 or 2): "))

    cpu_bits= int(input("\nEnter how many bits the CPU is: "))

    if (q2_type==1):
        in2 = int(input("Choose the type of Memory Addresability of the CPU [from the above table] (Enter option number): "))

        if (in2==4):
            new_cell_size = cpu_bits
        else:
            new_cell_size = cell_size_gen(in2)

        current_pins=log2(mem_space/cell_size)
        new_pins=log2(mem_space/new_cell_size)

        if (new_pins>current_pins):
            print("Additional Pins Required: ", int(floor(new_pins-current_pins)))
        else:
            print("Pins Saved: ", int(floor(new_pins-current_pins)))

    else:

        address_pins = int(input("Enter address pins the CPU has: "))
        in2 = int(input("Choose the type of Memory Addresability of the CPU [from the above table] (Enter option number): "))

        if (in2==4):
            new_cell_size = cpu_bits
        else:
            new_cell_size = cell_size_gen(in2)

        mem_space = int(pow(2,address_pins)*new_cell_size)/8

        print("\nMaximum size of main memory: ", end="")
        if (mem_space<1024000):
            print(int(mem_space/1024), " K", "B", sep="")
        elif (mem_space>=1024000 and mem_space<1048576000):
            print(int(mem_space/(1024*1024)), " M", "B", sep="")
        else:
            print(int(mem_space/(1024*1024*1024)), " G", "B", sep="")