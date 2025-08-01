# LCS

## 개념

- LCS(Longest Common Subsequence), 최장 공통 부분 수열
- 두 문자열을 비교할 때 공통 부분 수열 중 길이가 가장 긴 부분 수열

문자열 ACAYKP와 CAPCAK를 이용하여 예시를 살펴보면<br/>
**ACA**Y**K**P<br/>
C**A**P**CAK**<br/>

위 예시에서 공통 부분 수열은 AC, ACA, AP, AK 등이 있고 길이가 가장 긴 부분 수열 LCS는 ACAK가 된다. <br/><br/>
=> 즉 문자열이 연속적이지 않아도 된다는 의미로
두 문자열을 비교할 때 공통 부분 수열 중 길이가 가장 긴 부분 수열을 의미한다.

## 구현 과정 및 동작 원리

DP(Dynamic Programming)를 사용하여 구현할 수 있다.

str1이 `ACAYKP`, str2가 `CAPCAK`라고 할 때

아래와 같이 2차원 배열 dp를 생성한다.

<details>
<summary>dp 배열에서 0행, 0열을 추가하는 이유</summary>
0행과 0열은 각각 빈 문자열과의 비교 결과를 나타낸다.<br/>
`dp[i][j] = dp[i-1][j-1] + 1` 등을 계산할 때 인덱스 예외 처리 없이 계산이 가능하기 때문이다.
</details>

|     | -   | C   | A   | P   | C   | A   | K   |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| A   | 0   | 0   | 1   |     |     |     |     |
| C   | 0   | 1   |     |     |     |     |     |
| A   | 0   |     |     |     |     |     |     |
| Y   | 0   |     |     |     |     |     |     |
| K   | 0   |     |     |     |     |     |     |
| P   | 0   |     |     |     |     |     |     |

- dp[1][1] : 'A'와 'C'를 비교하여 일치하지 않으므로 0
- dp[1][2] : 'A'와 'A'를 비교하여 일치하므로 1
- dp[2][1] : 'C'와 'C'를 비교하여 일치하므로 1

---

이처럼 두 문자열을 비교하여 dp를 채워나간다.
| | - | C | A | P | C | A | K |
| - | - | - | - | - | - | - | - |
| - | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| C | 0 | 1 | | | | | |
| A | 0 | | | | | | |
| Y | 0 | | | | | | |
| K | 0 | | | | | | |
| P | 0 | | | | | | |

- dp[1][2] 이후 열에서 'A'와 일치하지 않더라도 이미 공통된 문자가 한번 등장했기 때문에 그 뒤의 칸들은 이전까지 구한 최장 공통 부분 수열의 길이인 1로 유지

---

|     | -   | C   | A   | P   | C     | A   | K   |
| --- | --- | --- | --- | --- | ----- | --- | --- |
| -   | 0   | 0   | 0   | 0   | 0     | 0   | 0   |
| A   | 0   | 0   | 1   | 1   | 1     | 1   | 1   |
| C   | 0   | 1   | 1   | 1   | **2** |     |     |
| A   | 0   |     |     |     |       |     |     |
| Y   | 0   |     |     |     |       |     |     |
| K   | 0   |     |     |     |       |     |     |
| P   | 0   |     |     |     |       |     |     |

- dp[2][4] : 문자열 'AC'와 'CAPC'까지의 비교 결과

- 문자열 'A'와 'CAP'의 최종 공통 부분 수열의 길이가 1인 상태에서 str1[1], str2[3]의 문자가 각각 'C'로 동일하다.
- 따라서 직전 결과 dp[1][3]의 값에 1을 더한 2가 들어간다.<br/>
  **`dp[2][4] = dp[1][3] + 1`**

---

|     | -   | C   | A   | P   | C   | A     | K   |
| --- | --- | --- | --- | --- | --- | ----- | --- |
| -   | 0   | 0   | 0   | 0   | 0   | 0     | 0   |
| A   | 0   | 0   | 1   | 1   | 1   | 1     | 1   |
| C   | 0   | 1   | 1   | 1   | 2   | 2     | 2   |
| A   | 0   | 1   | 2   | 2   | 2   | 3     | 3   |
| Y   | 0   | 1   | 2   | 2   | 2   | 3     | 3   |
| K   | 0   | 1   | 2   | 2   | 2   | **3** |     |
| P   | 0   |     |     |     |     |       |     |

- dp[5][5] : 문자열 'ACAYK'와 'CAPCA'까지의 비교 결과
- dp[5][4] : 문자열 'CAPC'와 'ACAYK'까지의 비교 결과 => 2
- dp[4][5] : 문자열 'CAPCA'와 'ACAY'까지의 비교 결과 => 3
- 현재 비교 중인 문자열이 'K'와 'A'로 다르기 때문에 직전 결과 dp[5][4]와 dp[4][5] 중 더 긴 LCS를 선택한다.
  <br/>
  **`dp[5][5] = max(dp[5][4], dp[4][5])`**

---

위 과정을 거쳐 아래와 같은 dp 테이블이 완성된다.

|     | -   | C   | A   | P   | C   | A   | K   |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| A   | 0   | 0   | 1   | 1   | 1   | 1   | 1   |
| C   | 0   | 1   | 1   | 1   | 2   | 2   | 2   |
| A   | 0   | 1   | 2   | 2   | 2   | 3   | 3   |
| Y   | 0   | 1   | 2   | 2   | 2   | 3   | 3   |
| K   | 0   | 1   | 2   | 2   | 2   | 3   | 4   |
| P   | 0   | 1   | 2   | 3   | 3   | 3   | 4   |

---

**📌 즉, 문자가 일치하지 않을 때는
`dp[i][j] = max(dp[i][j-1], dp[i-1][j])`<br/>
문자가 일치할 때는
`dp[i][j] = dp[i-1][j-1] + 1`**

## 코드

```python
str1 = list(input())
str2 = list(input())

dp = [[0] * (len(str2)+1)  for _ in range(len(str1)+1)]

for i in range(1, len(str1)+1):
    for j in range(1, len(str2)+1):
        if str1[i-1] == str2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i][j-1], dp[i-1][j])
```

## 관련 문제

[BOJ 9251 - LCS](https://www.acmicpc.net/problem/9251)
