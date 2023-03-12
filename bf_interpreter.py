#by gloop#5445
instructions = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
data_pointer,instruction_pointer = 0,0
tape = [0]*1000
data = tape[data_pointer]
output = ""
def run_command():
    global data_pointer, instruction_pointer, tape, output
    c = instructions[instruction_pointer]
    match c:
        case ">":
            data_pointer+=1
        case "<":
            data_pointer-=1
        case "+":
            tape[data_pointer]+=1
        case "-":
            tape[data_pointer]-=1
        case ".":
            output +=chr(tape[data_pointer])
        case ",":
            tape[data_pointer]=ord(input()[0])
        case "[":
            if tape[data_pointer] == 0:
                depth = 1
                while depth > 0:
                    instruction_pointer += 1
                    c = instructions[instruction_pointer]
                    if c == "[":
                        depth += 1
                    elif c == "]":
                        depth -= 1
        case "]":
            depth = 1
            while depth > 0:
                instruction_pointer -= 1
                c = instructions[instruction_pointer]
                if c == '[':
                    depth -= 1
                elif c == ']':
                    depth += 1
            instruction_pointer -= 1
    tape[data_pointer]%=256
    instruction_pointer+=1
while instruction_pointer<len(instructions)-1:
    run_command()
print(output)
print(tape[0:100])