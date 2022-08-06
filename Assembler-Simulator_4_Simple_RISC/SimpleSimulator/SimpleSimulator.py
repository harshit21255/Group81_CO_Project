import sys

code = sys.stdin.read().split()


opcode_mapping={
    "10000":["add","A"],
    "10001":["sub","A"],
    "10010":["mov","B"],
    "10011":["mov","C"],
    "10100":["ld","D"],
    "10101":["st","D"],
    "10110":["mul","A"],
    "10111":["div","C"],
    "11000":["rs","B"],
    "11001":["ls","B"],
    "11010":["xor","A"],
    "11011":["or","A"],
    "11100":["and","A"],
    "11101":["not","C"],
    "11110":["cmp","C"],
    "11111":["jmp","E"],
    "01100":["jlt","E"],
    "01101":["jgt","E"],
    "01111":["je","E"],
    "01010":["hlt","F"]
}
register_mapping={
    "000":0,
    "001":1,
    "010":2,
    "011":3,
    "100":4,
    "101":5,
    "110":6,
    "111":7
}


flag=[0,0,0,0]
register_list=[0,0,0,0,0,0,0,flag]


halt = False

def sum(input1, input2):
  return (input1+input2)

def diff(input1, input2):
  return (input1-input2)

def mul(input1, input2):
  return (input1*input2)

def xor_func(input1, input2):
  return (input1^input2)

def or_func(input1, input2):
  return (input1 | input2)

def and_func(input1, input2):
  return (input1 & input2)

def compare(input1, input2):
  if (input1==input2):
    return True
  else:
    return False

def divide(input1, input2):
  return (input1/input2)

def mod(input1, input2):
  return (input1%input2)

def type_a_instruction(instruction,op_1,op_2):
    if compare(instruction,"add"):
        result=sum(op_1,op_2)
        result=overflow_func(result)
        return result

    elif compare(instruction,"sub"):
        result=diff(op_1,op_2)
        result=overflow_func(result)
        return result

    elif compare(instruction,"mul"):
        result = mul(op_1,op_2)
        result=overflow_func(result)
        return result

    elif compare(instruction,"xor"):
        result=xor_func(op_1,op_2)
        return result

    elif compare(instruction,"or"):
        result=or_func(op_1,op_2)
        return result

    elif compare(instruction,"and"):
        result=and_func(op_1,op_2)
        return result


def type_b_instruction(instruction,immediate,reg_variable):
    if compare(instruction,"mov"):
        return immediate

    elif compare(instruction,"rs"):
        return reg_variable>>immediate

    elif compare(instruction,"ls"):
        return reg_variable<<immediate


def type_c_instruction(instruction,update_var,op_var):
    if compare(instruction,"mov"):
        if compare(op_var,flag):
            op_var=int(convert_flag(),2)
        reset_flag()
        return op_var

    elif compare(instruction,"div"):
        register_list[0]=divide(update_var,op_var)
        register_list[1]=mod(update_var,op_var)
        return update_var

    elif compare(instruction,"not"):
        return op_var^65535

    elif compare(instruction,"cmp"):
        if compare(update_var,op_var):
            flag[3]=1
        elif update_var<op_var:
            flag[1]=1
        else:
            flag[2]=1

        return update_var


def type_d_instruction(instruction,memory,reg_variable):
    if compare(instruction,"ld"):
        return int(memo[memory], 2)

    elif compare(instruction,"st"):
        memo[memory]=converter(reg_variable)
        return reg_variable


def type_e_instruction(instruction,memory):
    global program_counter
    if compare(instruction,"jmp"):
        program_counter=diff(memory,1)
       
    elif compare(instruction,"jlt"):
        if flag[1]==1:
            program_counter=diff(memory,1)
            
    elif compare(instruction,"jgt"):
        if flag[2]==1:
            program_counter=diff(memory,1) 

    elif compare(instruction,"je"):
        if flag[3]==1:
            program_counter=diff(memory,1)
    reset_flag()



def type_f_instruction():
    global halt
    halt=True


def register_allocation(type,line,instruction):
    check_for_reset(instruction,type)
    if compare(type,"A"):
        op_1=register_list[register_mapping[line[10:13]]]
        op_2=register_list[register_mapping[line[13:]]]

        register_list[register_mapping[line[7:10]]]=type_a_instruction(instruction,op_1,op_2)

    elif compare(type,"B"):
        immediate=int(line[8:],2)
        reg_variable=register_list[register_mapping[line[5:8]]]

        register_list[register_mapping[line[5:8]]]=type_b_instruction(instruction,immediate,reg_variable)

    elif compare(type,"C"):
        updated=register_list[register_mapping[line[10:13]]]
        op_var = register_list[register_mapping[line[13:]]]

        register_list[register_mapping[line[10:13]]]=type_c_instruction(instruction,updated,op_var)

    elif compare(type,"D"):
        memory = int(line[8:], 2)
        y_axis.append(memory)
        x_axis.append(cycle_count)
        reg_variable = register_list[register_mapping[line[5:8]]]

        register_list[register_mapping[line[5:8]]]=type_d_instruction(instruction,memory,reg_variable)


    elif compare(type,"E"):
        memory = int(line[8:], 2)
        type_e_instruction(instruction,memory)

    else:
        type_f_instruction()

def gt_lt(input1, input2):
  if (input1 > input2):
    return 1
  elif (input1 < input2):
    return 2

def overflow_func(reg_variable):
    if(gt_lt(reg_variable,0)==2):
        reg_variable=0
        flag[0]=1
    
    if(gt_lt(reg_variable,65535)==1):
        flag[0]=1
        reg_variable=lower(reg_variable)
    return reg_variable


def lower(n_input):
    b_var=bin(n_input)[2:]
    l_var=diff(len(b_var),16)
    n_input=int(b_var[l_var:],2)
    return n_input


def check_for_reset(ins_var,typ_var):
    if(compare(ins_var,"jlt") or compare(ins_var,"jgt") or compare(ins_var,"je")):
        return
    if(compare(ins_var,"mov") and compare(typ_var,"C")):
        return
    else:
        reset_flag()


def reset_flag():
    for i in range(4):
        flag[i]=0


def converter(num):
    a=bin(int(num))[2:]
    b=(diff(16,len(a)))*"0" + a
    return b


def converter_8_func(num):
    a=bin(int(num))[2:]
    b=(diff(8,len(a)))*"0" + a
    return b


def convert_flag():
    f_var="000000000000"

    for var in flag:
        f_var=f_var+str(var)
    return f_var


def write_func(program_counter):
    print(converter_8_func(program_counter)+" "+converter(register_list[0])+" "+converter(register_list[1])+" "+converter(register_list[2])
          +" "+converter(register_list[3])+" "+converter(register_list[4])+" "+converter(register_list[5])+" "+
          converter(register_list[6])+" "+convert_flag())


list_var="0000000000000000"
memo=[list_var]*256

i_var=0
for line in code:
    memo[i_var]=line
    i_var=sum(i_var,1)


program_counter=0  

cycle_count=0
memory=[]
cycle_list=[]
y_axis=[]
x_axis=[]



while halt == False:
    opcode=code[program_counter][:5]
    instruction=opcode_mapping[opcode][0]
    type=opcode_mapping[opcode][1]
    current = program_counter
    register_allocation(type,code[program_counter],instruction)

    cycle_list.append(cycle_count)
    memory.append(current)
    cycle_count=sum(cycle_count,1)

    write_func(current)
    program_counter=sum(program_counter,1)

c_var=0

for variable in memo:
    print(variable)
    c_var=sum(c_var,1)


import matplotlib.pyplot
import numpy
cycle_list.extend(x_axis)
memory.extend(y_axis)
matplotlib.pyplot.scatter(numpy.array(cycle_list),numpy.array(memory),marker="*")
matplotlib.pyplot.xlabel("Cycle")
matplotlib.pyplot.ylabel("Memory")
matplotlib.pyplot.show()