
arr = ['a', 'b', 'c']
number = [10, 20, 30]

dic = dict(zip(arr, number)) # 딕셔너리 만들기
print(dic)

'''
{10: 'a', 20: 'b', 30: 'c'}
'''

print('=========')

# enumerate를 활용해서 list를 dictionary로 만들기ㄴ
arr = ['a', 'b', 'c']
dic = {val : idx for idx, val in enumerate(arr)}
print(dic)

print('=========******')
# list를 두개를 dictionary로 만들기
arr =  ['a','b', 'c']
number = [10, 20, 30]

dic = {val: num for val, num in zip(arr, number)}
print(dic)

print('=========')

# Counter 객체
from collections import Counter
string = 'hello'
print(Counter(string)) # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

Counter(string).most_common()