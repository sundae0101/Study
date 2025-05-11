#################
#               #
#   Library     #
#               #
################# 



# from tabulate import tabulate



#################
#               #
#   Definition  #
#               #
################# 



def start_input():
    print("\n\nPlease input all 4-variable minterm (0~15) or None")
    list_minterm = list(map(int, input().split()))
    if (list_minterm):
        if (max(list_minterm) > 15 or min(list_minterm) < 0): 
            print("Error, please integer 0 ~ 15")
    
    
    print("Please input all 4-varibale don't care (0~15 or None)")
    list_DC = list(map(int, input().split()))
    
    if (list_DC):
        if (max(list_DC) > 15 or min(list_DC) < 0): 
            print("Error, please integer 0 ~ 15")
        
    
    
#   print("minterm:", end = ' ')
#   print(list_minterm)
#   print("don't care:", end = ' ')
#   print(list_DC)
    return list_minterm, list_DC

def merge_list(List_a, List_b): # 두 리스트를 합치는 함수, minterm과 don't care 항을 합치는 용도로 쓰이거나 두 리스트 합칠때 씀
    return List_a + List_b
    
def decimal_to_binary(num): # num을 입력받으면 
    list_decimal_to_binary = [2, 2, 2, 2]
    N = num
    for i in range(3, -1, -1):
        list_decimal_to_binary[i] = N % 2
        N //= 2
    return list_decimal_to_binary

def num_to_group(dict_group, num, list_binary_num):
    #기본항을 [-1, -1, -1, -1] 로 저장되지만 port에 저장되어있는것만 사용하므로 사실 상관없음
    group_num = sum(list_binary_num)
    dict_group[group_num].append([[num], list_binary_num]) # ex) 2 0010 ---> [2], [0, 0, 1 ,0]
    
def print_list(List): # [0, 0, 1, 0] 과 같은 리스트를 0010 처럼 붙여서 출력하기 위한 함수, 단 element가 2일경우 '-' 를 출력함
    for element in List:
        if (element == 2): print('-', end = '')
        else: print(element, end = '')

def compare_binary_list(List_a, List_b): ## 4칸의 binary list에 대해서 비교하여 1칸만 다를경우 다른 위치를 출력함. 
    check = 0
    index = -1
    for num in range(4):
        if (List_a[num] != List_b[num]):
            check += 1
            index = num
            
    if (check == 1): # 1칸만 다를경우
        return True, index
    else: # 아예 똑같거나 2칸 이상 다를경우
        return False, -1
        
def list_binary_compare_merge(List, index): #list와 index를 입력받으면 그 index 번째의 자료를 2로 바꿈
    new_list = List[:]
    new_list[index] = 2
    return new_list 

def list_binary_to_char(List): #binary list를 문자 list로 변환
    new_list = []
    
    if (List[0] == 1): new_list.append("A")
    elif (List[0] == 0): new_list.append("A'")
    
    if (List[1] == 1): new_list.append("B")
    elif (List[1] == 0): new_list.append("B'")
    
    if (List[2] == 1): new_list.append("C")
    elif (List[2] == 0): new_list.append("C'")
    
    if (List[3] == 1): new_list.append("D")
    elif (List[3] == 0): new_list.append("D'")
        
    return new_list
    
def list_to_string_comma(List):
    new_list = List[:]
    String = "".join(new_list)
    return String

def print_implicant_chart(list_minterm):
    print()
    print(" "*30, end = '| ')
    for i in list_minterm:
        print(i, end = ' '*2)
    print()
    print("-"*(30), end = '')
    print("+", end = '')
    print("-" * (len(list_minterm)*3 + 2), end = '\n')
    
    for line in range(PI_count):
        if (line in list_Index):
            print(">>> {0} {1}".format(list_PI[line][0], list_to_string_comma(list_PI[line][1])).rjust(30), end = '| ')
        
        else:
            print("{0} {1}".format(list_PI[line][0], list_to_string_comma(list_PI[line][1])).rjust(30), end = '| ')
            
        for row in range(len(list_minterm)):
            if list_minterm[row] in list_PI[line][0]:
                if list_minterm[row] in list_ESP:
                    print("⊗", end = '  ')
                else:
                    print("X", end = '  ')
                
                if (list_minterm[row] >= 9):
                    print(end = '  ')
            else:
                print(end = '   ')        
        print()
            
                


#################
#               #
#   Main Code   #
#               #
#################



list_minterm, list_DC = start_input() #입력 받아서 저장

port = merge_list(list_minterm, list_DC)
port.sort() #minterm과 don't care 합치기

dict_group = {0: [], 1: [], 2: [], 3: [], 4: []}

list_binary = [[-1, -1, -1, -1] for i in range(16)]


for num in port:
    
    list_binary[num] = decimal_to_binary(num) # list_binary애 십진수를 binary list의 형태로 list_binary 에 저장함
    
    num_to_group(dict_group, num, list_binary[num]) # 십진수 num에 대해 1의 개수에 따른 group 넘버를 dict_group에 저장함

dict_columns_2 = {0: [], 1: [], 2: [], 3: []}
dict_columns_3 = {0: [], 1: [], 2: []}
dict_columns_4 = {0: [], 1: []}
dict_columns_5 = {0: []}

list_dict_columns = [dict_group, dict_columns_2, dict_columns_3, dict_columns_4, dict_columns_5] 

# 5개의 dict를 저장하는 list를 만듬
# dict_group 의 역할은 dict_columns_1과 같음, 그러나 dict_group의 key는 그룹 넘버를 의미하며 
# 나머지 dict_columns의 key는 단지 이웃끼리 결합할 수 있는지를 확인하기 위함

last_columns_num = -1

## 병합 main logic

for step in range(4): #Column 1~5까지 존재할 수 있는데 dict_columns_1은 이미 만들었으므로 step은 4개까지 제작, 더 이상 결합이 되지 않는다면 중간에 break
    step_check = 1 #만약 단 하나라도 병합가능하다면 그대로 진행, 단 하나라도 병합이 안되었다면  for문을 종료
    
    seen = set() # 중복 방지용
    
    group_count = len(list_dict_columns[step]) # group 개수를 추출
    
    for group_num in range(group_count-1):
        
        for before_element_list in list_dict_columns[step][group_num]: # [[1], [0, 0, 0, 1]]
            for after_element_list in list_dict_columns[step][group_num + 1]: # [[5], [0, 1, 0, 1]]
                flag, index = compare_binary_list(before_element_list[1], after_element_list[1])
                
                if (flag): 
                    step_check = 0 #한번이라도 병합이 되었을 경우
                    merged_element = merge_list(before_element_list[0], after_element_list[0]) #element list를 병합
                    merged_list = list_binary_compare_merge(before_element_list[1], index) #한가지 요소를 2로 ('-') 바꾼 list
                    
                    merged_element.sort()
                    check = tuple(merged_element)
                    
                    if (check in seen): #만약 중복된다면 그냥 넘어갈것
                        continue
                    
                    else:
                        seen.add(check)
                        list_dict_columns[step + 1][group_num].append([merged_element, merged_list])
    
    if (step_check): #병합이 멈췄을경우
        last_columns_num = step  # 마지막 컬럼 넘버 - 1을 저장하고 break
        break
    
port_seen = set()
list_PI = [] #주항 저장할 리스트
# 주항 main logic

for step in range(last_columns_num, -1, -1):
    step_seen = set()
    group_num = len(list_dict_columns[step])
    
    for group_step in range(group_num):
        for element_list in list_dict_columns[step][group_step]:
            
            check = set(element_list[0])
            if (check - port_seen):
                step_seen = step_seen | check
                list_PI.append([element_list[0], list_binary_to_char(element_list[1]), len(element_list[0])])
            else:
                continue
    
    port_seen = port_seen | step_seen
        
    
    
# ESP 찾는 main logic
PI_count = len(list_PI)
dict_minterm_check = dict() #minterm이 한번씩은 포함되었는가
dict_minterm_count = dict() #minterm의 개수, 1인놈은 필수라는 것을 알 수 있음, 1회용임
dict_element_to_track_PI = dict() #minterm만 저장해야함
list_ESP = []
index = -1

Result = []
list_Index = []

for element in list_minterm:
    dict_minterm_check[element] = 1
    dict_minterm_count[element] = 0

for list_element in list_PI:
    for element in list_element[0]:
        if not (element in list_DC):
            dict_minterm_count[element] += 1

for element in dict_minterm_count: # 필수 주항을 찾는 과정
    if (dict_minterm_count[element] == 1):
        list_ESP.append(element)

for element in list_minterm: # 이 logic을 통해 어떤 minterm 하나에 대해서 이를 포함하고 있는 주항의 위치를 추적할 수 있음
    dict_element_to_track_PI[element] = []
    for element_list_index in range(PI_count):
        if element in list_PI[element_list_index][0] and element in list_minterm: #don'tcare 은 제외하고 minterm만 저장
            dict_element_to_track_PI[element].append(element_list_index)  

#먼저, 필수주항이 있다면 먼저 제거한다.

for element in list_ESP:
    
    # 9 -> 0
    list_Index.append(dict_element_to_track_PI[element][0])
    
    list_num_element = list_PI[dict_element_to_track_PI[element][0]][0]
    Result.append(list_PI[dict_element_to_track_PI[element][0]][1])
    
    for num_element in list_num_element: # num_elemnt 는 0, 1, 8, 9가 나올것임
        if num_element in list_DC: #don't care 항은 무시
            continue
        dict_minterm_check[num_element] = 0 # 이미 한번 포함하였음, 실제 logic에서는 같은 행의 요소를 다 제거하는 것
        list_PI[dict_element_to_track_PI[element][0]][2] = 0 # 더이상 필요없음
        
        # 각 num_element의 동일한 열도 찾아서 제거해야함
        
        for num_element_2 in dict_element_to_track_PI[num_element]: # num_element_2는 0 -> 0, 1 -> 0, 3
            
            if (list_PI[num_element_2][2]): # 아직까지 항이 남아있을경우 
                list_PI[num_element_2][2] -= 1
                
# 이후 그리디 방식으로, 남은 항이 제일 많은 주항을 골라 차례대로 제거해간다.



while(1):
    
    if (sum(dict_minterm_check.values()) == 0):
        break 
    
    flag = -1
    index = -1
        
    for list_index in range(PI_count):
        count = list_PI[list_index][2]
        if (count > flag):
            flag = count
            index = list_index
                
    list_PI[index][2] = 0
    Result.append(list_PI[index][1])
    list_Index.append(index)
    for element in list_PI[index][0]: # 5, 7
        if element in list_DC: #don't care 항은 무시
            continue
        
        
        
        dict_minterm_check[element] = 0
        for PI_index in dict_element_to_track_PI[element]: # 5 -> index 3, 4 추출
            if (list_PI[PI_index][2]): # 아직까지 항이 남아있을경우 
                list_PI[PI_index][2] -= 1
                



print("\n")
for i in Result:
    print_list(i)
    print(end = ' ')
print("\n")
print_implicant_chart(list_minterm)
print("\n\n")
