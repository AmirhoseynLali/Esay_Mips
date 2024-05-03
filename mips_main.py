
import os

class mips():

    def __init__(self) ->None:
        self.back_point = {}  # نقاط بازگشتی
        self.memory_R = {'$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0, '$s4': 0, '$s5': 0, '$s6': 0
            , '$s7': 0, '$zero': 0, '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0, '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0}
        self.len_book = 0
        self.first_page = 0
        self.memory_e = 0
        self.memory_m1 = 0
        self.memory_m2 = 0
        self.limite_c = 300
        self.erro = False
        self.erro_Massage = ""
        self.decimal_range = 7

        self.Data = None
        self.Data_Binary = None
        self.last_page = "Value : -1 | Line = -1"


    

    def make_thing_ready(self, path , limite = 300):
        #back to default
        self.back_point = {}  # نقاط بازگشتی
        self.memory_R = {'$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0, '$s4': 0, '$s5': 0, '$s6': 0
            , '$s7': 0, '$zero': 0, '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0, '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0}
        self.len_book = 0
        self.first_page = 0
        self.memory_e = 0
        self.memory_m1 = 0
        self.memory_m2 = 0
        self.limite_c = limite
        self.erro = False
        self.erro_Massage = ""
        self.decimal_range = 7

        self.Data = None
        self.Data_Binary = None
        self.last_page = "Value : -1 | Line = -1"

        try:
            if ".text" in path.lower() or ".txt" in path.lower():
                with open(os.path.join(path), encoding='utf8') as f:
                    self.book = f.readlines()
                    f.close()
            else:
                self.erro = True
                self.erro_Massage = "Type File Erro"
                raise ValueError(self.erro_Massage)
                
        except FileNotFoundError:
            self.erro = True
            self.erro_Massage = "File Not Founded"
            raise ValueError(self.erro_Massage)
        
        self.make_back_points()
        
        # self.reader(self.first_page, self.len_book, 0)
        self.reader(start=0, end=self.len_book, f2=0)
        return 1      
        # self.sort_values()
        # self.make_values_binary()
        # print(self.memory_R)
        
    def make_back_points(self):
        for i in self.book:  # ساخت نقاط بازگشتی
            if str(i).find('end_set') != -1:
                self.first_page = (self.len_book + 1)
            if self.first_page == 0:
                test = str(i)
                if test.find('array') != -1:
                    self.fix_memory(test, 0, 'update')
                if test.find('=') != -1:
                    test = test.split('=')
                    self.fix_memory(test[0], int(test[1]), 'update')
                elif test.find(',') != -1:
                    self.set_array(test)

            if str(i).find(':') != -1:
                test = i.find(':')
                test = i[:test]
                self.back_point.update({test: self.len_book})
            self.len_book += 1

    def set_array(self, value):
        value = value.split(',')
        for i_1 in self.memory_R:
            if i_1.find(str(value[0])) != -1:
                if type(self.memory_R[i_1]) == dict:
                    self.memory_R[i_1].update({str(value[1]): int(value[2])})

    def fix_memory(self, case, case2, case3):  # کیس 1 خود حافظه است و کیس دو مفدار عددی است که قرار به حافظه داده شه و کیس سه دستور
    # پیدا کردن مقدار حافظه یا دستور عوض کردن مقدار ان است
        if case3 == 'find':
            prov = False
            save = int()
            for i2 in self.memory_R:
                if case == i2:
                    prov = True
                    save = self.memory_R[i2]
                    break
            if not prov:
                print('memory cant be found ERROR')
                exit()
            elif prov:
                return save
        elif case3 == 'update':
            if case.find('array') != -1:
                case = case.replace('array', " ")
                case = case.strip()
                for i3 in self.memory_R:
                    if case.find(i3) != -1:
                        self.memory_R[i3] = {}
                        break
            else:
                for i3 in self.memory_R:
                    if case.find(i3) != -1:

                        self.memory_R[i3] = case2
                        break
    

    def add(self, line):
        line = line.replace('add', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        b = self.fix_memory(b, 0, 'find')
        c = self.fix_memory(c, 0, 'find')
        value = int(b) + int(c)
        self.fix_memory(a, value, 'update')

    def addi(self,line):
        line = line.replace('addi', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        b = self.fix_memory(b, 0, 'find')
        value = int(b) + int(c)
        self.fix_memory(a, value, 'update')
    
    def sub(self, line):
        line = line.replace('sub', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        b = self.fix_memory(b, 0, 'find')
        c = self.fix_memory(c, 0, 'find')
        value = int(b) - int(c)
        self.fix_memory(a, value, 'update')

    def lw(self, line):
        line = line.replace('lw', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        b = b.replace('(', ',')
        b = b.split(',')
        c = str(b[0])
        b = b[1]
        b = b.replace(")", " ")
        b = b.strip()
        value = self.memory_R[b][c]
        self.fix_memory(a, value, 'update')

    def sw(self,line):
        line = line.replace('sw', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        a = self.fix_memory(a, 0, 'find')
        b = line[1]
        b = b.replace('(', ',')
        b = b.split(',')
        c = str(b[0])
        b = b[1]
        b = b.replace(")", " ")
        b = b.strip()
        self.memory_R[b][c] = a

    def sll(self, line):
        line = line.replace('sll', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        b = self.fix_memory(b, 0, 'find')
        value = int(b) * (int(c) * 2)
        self.fix_memory(a, value, 'update')

    def srl(self,line):
        line = line.replace('srl', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        b = self.fix_memory(b, 0, 'find')
        value = int(b) / (int(c) * 2)
        self.fix_memory(a, int(value), 'update')
    
    def slt(self,line):
        line = line.replace('slt', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        try:
            c = int(c)
        except ValueError:
            c = self.fix_memory(c, 0, 'find')

        b = self.fix_memory(b, 0, 'find')
        value = 0
        if int(b) < int(c):
            value = 1
        self.fix_memory(a, value, 'update')

    
    def max_i(self, start, items):
        answer_index = start
        for index in range(start, len(items)):
            if (items[index] > items[answer_index]):
                answer_index = index
        return answer_index


    def sort_values(self):
        keys = list(self.memory_R.keys())
        values = list(self.memory_R.values())
        new_memory_R = dict()

        for index in range(0, len(values)):

            max_index = self.max_i(index, values)
            temp_v , temp_k = values[max_index], keys[max_index]
            values[max_index] , keys[max_index] = values[index], keys[index]
            values[index], keys[index] = temp_v, temp_k
            new_memory_R[keys[index]] = values[index]

        self.memory_R = new_memory_R
    
        
        
    def make_values_binary(self):
        for item in self.memory_R:
            self.memory_R[item] = self.num_to_binary(self.memory_R[item])


    def num_to_binary(self,num):
    
        r = 1
        c = 0
    # print('the binary of ', num)
        while int(num) != 0:
            c += int(num % 2) * r
            r *= 10
            num = int(num / 2)
    # print('is ', c)
        c = self.fix_binary(c)
        return c
    
   
    def fix_binary(self, binary):
        binary = str(binary)
        n = 7
        n -= len(binary)
        answer = str()
        while n > -1:
            answer += '0'
            n -= 1
        if (len(answer) + len(binary)) == 8:
            answer += binary
        else:
            if len(binary) > 8:
                answer = str()
                tt = len(binary)
                tt -= 8
                for j in range(0, 8):
                    answer += binary[tt]
                    tt += 1
            else:
                answer = binary
        return answer


    def binary_to_num(self,binary):
        n = len(binary)
        n -= 1
        n2 = n
        answer = 0
    # print('the number of ', binary)
        while n > -1:
            if binary[n] == '1':
                answer += (2 ** (n2 - n))
            n -= 1
    # print('is ', answer)
        return answer

    def and_f(self, line):
        line = line.replace('and', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        b = self.fix_memory(b, 0, 'find')
        b = self.num_to_binary(int(b))
        c = self.fix_memory(c, 0, 'find')
        c = self.num_to_binary(int(c))
        ss = str()
        for i2 in range(0, 8):
            if b[i2] != c[i2]:
                ss += '0'
            else:
                ss += b[i2]
        value = self.binary_to_num(ss)
        self.fix_memory(a, value, 'update')

    
    def or_f(self,line):
        line = line.replace('or', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        b = self.fix_memory(b, 0, 'find')
        b = self.num_to_binary(int(b))
        c = self.fix_memory(c, 0, 'find')
        c = self.num_to_binary(int(c))
        ss = str()
        for i2 in range(0, 8):
            if b[i2] == '0' and c[i2] == '0':
                ss += '0'
            else:
                ss += '1'
    # print('final is ', ss)
        value = self.binary_to_num(ss)
    # print('value is ', value)
        self.fix_memory(a, value, 'update')

    def or_i(self, line):
        line = line.replace('ori', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = int(line[2])
        b = self.fix_memory(b, 0, 'find')
        b = self.num_to_binary(int(b))
        c = self.num_to_binary(int(c))
    # print('b is ', b)
    # print('c is ', c)
        ss = str()
        for i2 in range(0, 8):
            if b[i2] == '0' and c[i2] == '0':
                ss += '0'
            else:
                ss += '1'
    # print('final is ', ss)
        value = self.binary_to_num(ss)
    # print('value is ', value)
        self.fix_memory(a, value, 'update')


    def andi(self,line):
        line = line.replace('andi', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = line[2]
        b = self.fix_memory(b, 0, 'find')
        b = self.num_to_binary(int(b))
        c = self.num_to_binary(int(c))
    # print('b is ', b)
    # print('c is ', c)
        ss = str()
        for i2 in range(0, 8):
            if b[i2] != c[i2]:
                ss += '0'
            else:
                ss += b[i2]
    # print('final is ', ss)
        value = self.binary_to_num(ss)
    # print('value is ', value)
        self.fix_memory(a, value, 'update')


    def nori(self,line):
        line = line.replace('nori', " ")
        line = line.strip()
        line = line.split(',')
        a = line[0]
        b = line[1]
        c = int(line[2])
        b = self.fix_memory(b, 0, 'find')
        b = self.num_to_binary(int(b))
        c = self.num_to_binary(c)
        ss = str()
        for i2 in range(0, 8):
            if b[i2] == '0' and c[i2] == '0':
                ss += '1'
            else:
                ss += '0'
    # print('final is ', ss)
        value = self.binary_to_num(ss)
    # print('value is ', value)
        self.fix_memory(a, value, 'update')
    
    def brain(self, page):
        if page.find('addi') != -1:
            self.addi(page)
            return True
        elif page.find('add') != -1:
            self.add(page)
            return True
        elif page.find('sub') != -1:
            self.sub(page)
            return True
        elif page.find('lw') != -1:
            self.lw(page)
            return True
        elif page.find('sw') != -1:
            self.sw(page)
            return True
        elif page.find('sll') != -1:
            self.sll(page)
            return True
        elif page.find('srl') != -1:
             self.srl(page)
             return True
        elif page.find('andi') != -1:
            self.andi(page)
            return True
        elif page.find('and') != -1:
            self.and_f(page)
            return True
        elif page.find('nori') != -1:
            self.nori(page)
            return True
        elif page.find('ori') != -1:
            self.or_i(page)
            return True
        elif page.find('or') != -1:
            self.or_f(page)
            return True
        elif page.find('slt') != -1:
              self.slt(page)
              return True
        else:
            return False
    

    def jump(self, page):
        if page[0] == 'j' and page[1] == " ":
            page = page.replace('j', " ")
            page = page.strip()
            for point in self.back_point:
                if point.find(page) != -1:
                    page = self.back_point[point]
                    return page
        elif page.find('beq') != -1:
            page = page.replace('beq', " ")
            page = page.strip()
            page = page.split(',')
            a = self.fix_memory(page[0], 0, 'find')
            b = self.fix_memory(page[1], 0, 'find')
            c = page[2]
            c = c.strip()
            if int(a) == int(b):
                for point in self.back_point:
                    if point.find(c) != -1:
                        page = self.back_point[point]
                        return page
            else:
                return -1
            
        elif page.find('bne') != -1:
            page = page.replace('bne', " ")
            page = page.strip()
            page = page.split(',')
            a = self.fix_memory(page[0], 0, 'find')
            b = self.fix_memory(page[1], 0, 'find')
            c = page[2]
            if int(a) != int(b):
                c = c.strip()
                for point in self.back_point:
                    if point.find(c) != -1:
                    # print('iam found beq point very well ', back_point[point])
                        page = self.back_point[point]
                        return page
            else:
                return -1
        
        else:
            return -1
        

    def reader(self, start, end, f2):
        page = start
        while page < end:
            if f2 >= self.limite_c:
                self.erro_Massage = "Loop At It's Limit"
                self.erro = True
                raise ValueError(self.erro_Massage)
            f2 += 1
            # print(f2, ' _ ', page, 'end = ', end, '  and start = ', start)
            new = str(self.book[page])
            if new != '\n':
                new = new.replace('\n', ' ')
                self.last_page = f"Value : ( {new} ) | Line = {page + 1}"
            new = new.strip()
            if new.find(':') == -1 and len(new) > 1:
                try:
                    founded = self.brain(new)
                    if not founded:
                        go = self.jump(new)
                        if go >= 0:
                            self.reader(int(go), end, f2)
                            break
                except TypeError:
                    self.erro_Massage = f"Problem At Line {page+1} (Probebly Cauesd By Back Points)"
                    self.erro = True
                    raise ValueError(self.erro_Massage)
            page += 1



# model = mips()
# try:
#     model.make_thing_ready("mips_compiler\\mips\\ضرب.txt")
# except ValueError:
#     print(model.erro_Massage)


# print(model.memory_R)