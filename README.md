This code uses 4 classes:

CPU:

this imitates the function of the CPU(according to A-Level Computer Science Standards)
This has an instruction set used to decode instructions as when recieved in preparation for execution.

RAM:

This has two seperate memory units: Address and Data
There are functions within this to fetch the data from the Ram.

Assembler:

This is used to take an input, tokenise it, genrate a symbol tree and finally generate machine code.

VM:

This is a 'virtual machine' class which I use to pull the other classes together.
It makes use of two main functions:

Load - This will take the input run it through each stage of the assembler and then load the instructions and data into RAM as needed.

Run - This will create a loop moving through each stage of the FDE cycle which runs until the code reaches 'HALT' at which point the loop stops.

The program uses my own instructions based on those from places like LMC they are as follows:

INP- Input

OUT - Output

STO - Store

LOAD - Load

ADD - Add

SUB - Sub

HALT - End of the code

JMP - Jump/branch Always

JMZ - Jump/branch if zero

JMPP - Jump/branch if positive

When branching put a tag after the branch command:

JMP loop

And then put a reference with a colon higher in the code:

Loop:

  INP
  
  OUT
  
  JMP Loop
  
  HALT

Here I will paste an example code to multiply two inputs:
  
        INP
        STO NUM1      
        INP        
        STO NUM2
      
    LOOP:
  
        LOAD ANS
        ADD NUM1
        STO ANS
        LOAD NUM2
        SUB ONE
        STO NUM2
        SUB ONE
        JMPP LOOP
        LOAD ANS
        OUT
        HALT
      
    NUM1 DAT 0
    
    NUM2 DAT 0
    
    ANS DAT 0
    
    ONE DAT 1
