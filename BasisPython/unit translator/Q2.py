# CMT309 Coursework 1
# student number:
import sys

def unit_translator(filename, D = None):
    length_units = {
        "mm":1,
        "cm":10,
        "m": 1000,
        "km":1000000
    }
    filesize_units = {
        "B":1,
        "KB":1024**1,
        "MB":1024**2,
        "GB":1024**3,
        "TB":1024**4,
        "PB":1024**5
    }
    time_units = {
        "sec":1,
        "min":60,
        "h":3600
    }
    #找到单位之间的倍数关系

    with open(filename,encoding="utf-8") as f:
        text = f.read()

    #读取文件

    words = text.split(" ")

    words_list = []

    def ISFLOAT(x):

        digital = True
        for char in x:

            if char != "." and str.isdigit(char) == False:
                digital = False

        # 除小数点外都是数字

        if digital:
                return  True

        return  False
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

    for word in words:

        if "." not in word:

            words_list.append(word)

        else:

            partA,partB = word.split(".")

            if str(partA).isdigit() and str(partB).isdigit():

                words_list.append(word)

            else:

                words_list.append(partA)

                words_list.append(".")

                words_list.append(partB)
    #分割文中的单词 每个单词首先按空格分割。但是有些单词是句号连在一起的 比如 mm.over 这时候要用"." 分割，
    #但是有些小数也是"."分割 所以要判断分割后的两部分是否为数字 如果都是数字 说明是小数 不能这么分割，如果不是分两部分假如单词列表


    for i in range(len(words_list)):

        this_word = words_list[i]

        if this_word in length_units:
            #如果这个单词是一个长度单位
            if "length" not in D:
                #D中要求了对长度进行转换
                continue
            else:
                if ISFLOAT(words_list[i - 1]):
                    value = float(words_list[i - 1])

                else:
                    continue
                # 出现了单位 前面如果是数值。 也有可能不是数值 比如 some GB 这种就跳过

                multioperator = length_units[this_word] / length_units[D["length"]]
                words_list[i - 1] = str(value *  multioperator)
                words_list[i] = D["length"]

        elif this_word in filesize_units:
            if "filesize" not in D:
                continue
            else:
                if ISFLOAT(words_list[i - 1]):
                    value = float(words_list[i - 1])

                else:
                    continue
                multioperator = filesize_units[this_word] / filesize_units[D["filesize"]]
                words_list[i - 1] = str(value *  multioperator)
                words_list[i] = D["filesize"]

        elif this_word in time_units:

            if "time" not in D:
                continue

            else:

                if ISFLOAT(words_list[i - 1]):
                    value = float(words_list[i - 1])

                else:
                    continue
                multioperator = time_units[this_word] / time_units[D["time"]]
                words_list[i - 1] = str(value * multioperator)
                words_list[i] = D["time"]

    transfered_text =REPLACE( " ".join(words_list)," .",".")
    with open("Q2_example_text_translated.txt",'w') as f:
        f.write(transfered_text)
# define dictionary here
D = {"length":"cm","filesize":"GB"}

# ---- DO NOT CHANGE THE CODE BELOW ----
if __name__ == "__main__":
    unit_translator("Q2_example_text.txt",D)
    #if len(sys.argv)<2: raise ValueError('Provide filename as input argument')
    #filename = sys.argv[1]
    #print('filename is "{}"'.format(filename))
    #unit_translator(filename, D)
