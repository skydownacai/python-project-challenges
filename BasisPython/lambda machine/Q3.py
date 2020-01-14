# CMT309 Coursework 1
# student number:
import sys

def lambda_machine(filename):

    with open(filename) as f:

        codelines = f.readlines()

    #将代码按每行读取

    lambda_statement = [ ] # 包含lambda 且不是 深嵌套的代码行

    code_pointer = 0 #一个行数指针

    def REPLACE(x, old, new):

        old_len = len(old)

        while True:
            exist = False

            for i in range(len(x) - old_len + 1):

                sub_str = x[i:i + old_len]

                if sub_str == old:
                    exist = True
                    x = x[:i] + new + x[min(len(x), i + old_len):]

            if not exist:
                break

        return x
    while code_pointer <= len(codelines) - 1:

        line = codelines[code_pointer]

        if "lambda" in line :

            no_space_line = REPLACE(line," ","")

            equal_start= no_space_line.index("=")

            if no_space_line[equal_start + 1] == "(":

                equal_start += 1

            expected = no_space_line[equal_start + 1: equal_start + 7]

            if expected == "lambda":

                lambda_statement.append(line)

            #如果一行代码不是嵌套的lambda 那么 lambda关键字应该出现在等号后面

        elif "def" in line:

            #如果是函数定义,首先找到参数

            line = REPLACE(line," ","")

            left_bracket = line.index("(")

            right_bracket = line.index(")")


            function_name = line[3:left_bracket]

            arguments = line[left_bracket + 1:right_bracket]

            arguments = arguments.split(",")

            def_statements = [ ]

            for j in range(code_pointer + 1,len(codelines)) :


                if ord(codelines[j][0]) == 10:
                     #ord是字符的ascii 码 可以百度查看
                     #是个空白行
                     continue

                if ord(codelines[j][0]) == 9 or codelines[j][0] == " ":
                    #ord() == 9 表明是tab符号  如果开头是tab或者空格 表明有缩进
                    def_statements.append(codelines[j])
                else:
                    break
            if len(def_statements) == 1:

                #表明只有一个return
                statement = REPLACE(def_statements[0]," ","")

                #找到返回值
                return_value = REPLACE(statement,"return","")

                #完整的表达式应该为

                new_lambda_statement = function_name + " = lambda " + ",".join(arguments) + " : " + return_value

                lambda_statement.append(new_lambda_statement)


            elif len(def_statements) == 4:

                if_condintion = def_statements[0]

                for char in [":","\t","\n",chr(9)]:

                    if_condintion = REPLACE(if_condintion,char,"")

                i_index = if_condintion.index("i")

                if_condintion = if_condintion[i_index: ]

                if_value =  def_statements[1]
                for char in ["return","\t","\n",chr(9)," "]:

                    if_value = REPLACE(if_value,char,"")


                else_value =  def_statements[1]
                for char in ["return","\t","\n",chr(9)," "]:

                    else_value = REPLACE(else_value,char,"")


                #替换掉tab符号 空格 与换行符

                new_lambda_statement = function_name + " = lambda " + ",".join(arguments) + " : "

                new_lambda_statement += if_value + " " + if_condintion + " "

                new_lambda_statement += "else " + else_value + "\n"

                lambda_statement.append(new_lambda_statement)
            #找到参数之后,我需要找到与函数相关的表达式,通过缩进判断

        else:
            if ord(line[0]) not in [9,10,32]:

                lambda_statement.append(line)

        code_pointer += 1

    #转换掉所有的表达式之后输出

    with open("lambda_mytest.py","w") as f:

        for lambda_expression in lambda_statement:

               f.write(lambda_expression)
# ---- DO NOT CHANGE THE CODE BELOW ----
if __name__ == "__main__":
    if len(sys.argv)<2: raise ValueError('Provide filename as input argument')
    filename = sys.argv[1]
    print('filename is "{}"'.format(filename))
    lambda_machine(filename)
