# python 정렬 sort, sorted 차이

## 1. sort 함수

- `리스트명.sort()`
- 리스트 객체 메서드
- 반환값 None
- 리스트 자체의 값이 바뀜(inplace 함수). 원본 변경

```py
a = [3, 2, 4]
a.sort()
print(a) # [2, 3, 4]
```

## 2. sorted 함수

- `sorted(리스트명)`
- 내장 함수
- 리스트 자료형 반환

```py
a = [3, 2, 4]
b = sorted(a)
print(a) # [3, 2, 4]
print(b) # [2, 3, 4]
```

## 시간복잡도

`sort()`와 `sorted()`는 Timesort 알고리즘 사용

- Timesort 알고리즘은 Insert sort와 Merge sort를 결합한 하이브리드 알고리즘
- 최선: O(n)
- 평균: O(n log n)
- 최악: O(n log n)
