import sys
regaddr={ "R0": "000",
        "R1": "001",
        "R2":"010",
        "R3":"011",
        "R4":"100",
        "R5":"101",
        "R6":"110",
        "FLAGS":"111"}

opcode ={ 
        "var": "00000",
         "la"
        "add": "10000",
        "sub": "10001",
        "mov": ["10010", "10011"],
        "ld" : "10100",
        "st" : "10101",
        "mul": "10110",
        "div": "10111",
        "rs" : "11000",
        "ls" : "11001",
        "xor": "11010",
        "or" : "11011",
        "and": "11100",
        "not": "11101",
        "cmp": "11110",
        "jmp": "11111",
        "jlt": "01100",
        "jgt": "01101",
        "je" : "01111",
        "hlt": "01010",
      }

D={    "var": ["var"],
       "label": ["label:"],
       "a": ["add", "sub", "mul", "xor", "or", "and"],
       "b": ["mov", "rs", "ls"],
       "c": ["mov", "div", "not", "cmp"],
       "d": ["ld", "st"],
       "e": ["jmp", "jlt", "jgt", "je"],
       "f": ["hlt"]}
    
Dlen={
    "var": 2,
    "a": 4,
    "b": 3,
    "c": 3,
    "d": 3,
    "e": 2,
    "f": 1,
    "syntax": 0

}


def type(a, movReg=69):
    if a=="var":
      return "var"

    D={"a": ["add", "sub", "mul", "xor", "or", "and"],
       "b": ["mov", "rs", "ls"],
       "c": ["mov", "div", "not", "cmp"],
       "d": ["ld", "st"],
       "e": ["jmp", "jlt", "jgt", "je"],
       "f": ["hlt"]}

    if (movReg==1):
        return "b"
    elif (movReg==0):
        return "c"
    for i in D.keys():
        if a in D[i]:
            return i
    
    if(a[-1]==":"):
      return "label"
      
    return "syntax"


inputlines=[]

# with open("in.txt", "r") as f:
#     data = f.readlines()
#     for i in data:
#         inputlines.append(i.strip())
data= sys.stdin.readlines()
for i in data:
  inputlines.append(i.strip())

linecount=0
varcount=0
count=1
errors=[]
hltcount=0
variables={}
label={}

for linecount in range(len(inputlines)):
  line=inputlines[linecount].split()
  if not line:
    continue
  t=type(line[0]) 
  if t=="syntax":
    print('ERROR: Typos in Instruction Name or Register Name @ Line',linecount+1,sep=" ")
    errors.append(linecount+1)
    break
  if(t=='label'):
    label[line[0]]=0
    line.pop(0)
  if len(line)==0:
    print("ERROR: Syntax Error @ Line",linecount+1,sep=" ")
    errors.append(linecount+1)
    break
  t=type(line[0])
  if t=='label':
    print("ERROR: Syntax Error @ Line",linecount+1,sep=" ")
    errors.append(linecount+1)
    break
  if len(line)!=Dlen[t]:
    print('ERROR: Length Does Not Match Error @ Line',linecount+1,sep=" ")
    errors.append(linecount+1) 
    break
  if t=='e' and line[1] not in label.keys():
    print("ERROR: Label Error @ Line",linecount+1,sep=" ")
    errors.append(linecount+1)
    break

  if(line[0])=="var":
    varcount+=1   
    variables[line[1]]=0
  else:
    count+=1
  if t=='d' and line[2] not in variables.keys():
    print("ERROR: Variable Error @ Line",linecount+1,sep=" ")
    errors.append(linecount+1)
    break
  if line[0]=="hlt":
    hltcount+=1
  
  if (linecount==len(inputlines)-1 and line[0]!="hlt"):
    
    print('ERROR: hlt Not Last Line Error @ Line',linecount+1,sep=" ")
    errors.append(linecount+1)
    break

  if hltcount>1:
    print('ERROR: Multiple hlt Error @ Line',linecount+1,sep=" ")
    errors.append(linecount+1)
    break

linecount=0
for linecount in range(len(inputlines)):
  line=inputlines[linecount].split()
  

#_--------------------------------------------------------------------


def regAddr(reg):
    D={ "R0": "000",
        "R1": "001",
        "R2":"010",
        "R3":"011",
        "R4":"100",
        "R5":"101",
        "R6":"110",
        "FLAGS":"111"}

    if reg in D.keys():
        return D[reg]
    else:
        return "not found"

def opcode(a, movReg=69):
    D={ "add": "10000",
        "sub": "10001",
        "mov": ["10010", "10011"],
        "ld" : "10100",
        "st" : "10101",
        "mul": "10110",
        "div": "10111",
        "rs" : "11000",
        "ls" : "11001",
        "xor": "11010",
        "or" : "11011",
        "and": "11100",
        "not": "11101",
        "cmp": "11110",
        "jmp": "11111",
        "jlt": "01100",
        "jgt": "01101",
        "je" : "01111",
        "hlt": "01010"}

    if (movReg==69):
        return D[a]
    elif (movReg==1):
        return D["mov"][0]
    else:
        return D["mov"][1]


def binary(n):
    st = str(bin(int(n))[2:])
    
    return st.zfill(8)

def typeA(opc, r1, r2, r3):
  print(opcode(opc),"00",regAddr(r1),regAddr(r2),regAddr(r3), sep="")

def typeB(opc, r1, i, imm=-1):
  if imm==-1:
    print(opcode(opc),regAddr(r1),binary(i[1::]), sep="")
  elif imm==1:
    print(opcode(opc, 0),regAddr(r1),binary(i[1::]), sep="")
  else:
    print(opcode(opc, 1),regAddr(r1),binary(i[1::]), sep="")

def typeC(opc, r1, r2, imm=-1):
  if r1=='FLAGS' and r2!='FLAGS':
    print(opcode(opc, 1),"00000",regAddr(r1),regAddr(r2), sep="")
  elif imm==-1:
    print(opcode(opc),"00000",regAddr(r1),regAddr(r2), sep="")
  elif imm==1:
    print(opcode(opc, 0),"00000",regAddr(r1),regAddr(r2), sep="")
  else:
    print(opcode(opc, 1),"00000",regAddr(r1),regAddr(r2), sep="")

#change in type D and type E functions to tackle VARIABLE ERROR
def typeD(opc, r1, mem_add):
    # yaha pe mem_add mein jo bhi print karna hai vo bhi aayega
    # same for type E
    mem_address=variables[mem_add]
    print(opcode(opc),regAddr(r1),binary(mem_address), sep="")

def typeE(opc, mem_add):
    mem_address=label[mem_add]
    print(opcode(opc),"000",binary(mem_address), sep="")


def drivercode(line,t):
  if (line[0]=="mov"):
    if (line[2][0]=="$"):
        imm=1
    else:
        imm=0
  else:
    imm=-1    
  if t=="a":
    typeA(line[0], line[1], line[2], line[3])
  elif t=="b" and(imm==1 or imm==-1):
    typeB(line[0], line[1], line[2], imm)
  elif t=="c" or imm==0:
    typeC(line[0], line[1], line[2],imm)
  elif t=="d":
    typeD(line[0], line[1], line[2])
  elif t=="e":
    typeE(line[0], line[1])
  elif t=="f":
    print("0101000000000000")


variables={}
label={}
linecount=0
consecBlank=0

count=0
linecount=0

for linecount in range(len(inputlines)):
  line=inputlines[linecount].split()
  if len(line)!=0 and line[0]!="var":
    count+=1

linecount=0
variablecounter=0
flag=0
if len(errors)!=0:
  flag=1

for linecount in range(len(inputlines)):
  if flag==1:
    break
  #line has different words of each line, [word 1,word 2,.....word n]
  line = inputlines[linecount].split()  
  if not line:
    continue  
  t=type(line[0])
  if t=="var":
    #if a variable is found, insert it into dictionary
    variables[line[1]]=count+variablecounter
    variablecounter+=1
  elif t=="label":
    #if a label is found, appended in dictionary along with count
    label[line[0]]=linecount
    line.pop(0)
    t=type(line[0])
    drivercode(line,t)
  elif t!="syntax":
    drivercode(line,t)

# if flag==1:
#   print("SYNTAX ERROR")
