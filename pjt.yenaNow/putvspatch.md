## 상황

- 회원 정보 수정 api를 연결 중이었음
- 이름, 닉네임, 전화번호 3가지 항목
- 각각 useState로 관리하는 게 좋은지 한번에 묶어서 하나의 객체 formData로 요청을 보내는 게 좋은지 고민이 됨

## 생각

- PUT 메서드가 아니라 PATCH 메서드이니 각각 관리하는 게 RESTful 하다고 생각
- 그런데 만약 항목이 3개가 아니라 더 많아진다면? 10개만 돼도 오히려 각각 관리하는 게 더 복잡하다고 생각

## 개념

**PUT**

- 자원의 전체 교체
- 교체 시 모든 필드 필요
- 일부만 전달할 경우 전달한 필드 모두 null 혹은 초기값 처리 됨
- i) 자원이 존재하지 않는 경우 -> 새로운 자원 저장
- ii) 자원이 존재하는 경우 -> 기존에 존재하는 자원을 새로운 자원으로 대체

**PATCH**

- 자원의 부분 교체
- 기존 자원이 반드시 있어야 함

## 결론

- 하나의 객체로 관리 -> 훨씬 효율적이라고 생각, 유지 보수 관점
- RESTful하게 변경된 항목만 PATCH 요청 보내기

## 추가

```typescript
const getPatchPayload = () => {
  const payload: Partial<UserMeInfoEditRequest> = {}

  if (myInfo.name !== userData.name) {
    payload.name = userData.name
  }

  if (myInfo.nickname !== userData.nickname) {
    payload.nickname = userData.nickname
  }

  if (myInfo.phoneNumber !== userData.phoneNumber) {
    payload.phoneNumber = userData.phoneNumber
  }

  return payload
}
```

위와 같은 형태로 값이 변경된 경우에만 patch 요청 전송하는 로직 작성

**⚠️error**

```
Argument of type 'Partial<UserMeInfoEditRequest>' is not assignable to parameter of type 'UserMeInfoEditRequest'.
Types of property 'name' are incompatible.
Type 'string | undefined' is not assignable to type 'string'.
Type 'undefined' is not assignable to type 'string'.
```

`undefined`일 수 있는 필드를 `string`으로 받아야 한다고 작성했기 때문에 발생

Partial로 일부 필드가 빠질 수 있는데 `userAPI.editUserMeInfo()`는 모든 필드를 요구하고 있음

**💡해결**

API 타입 `Partial`로 바꿔주기

```typescript
  editUserMeInfo: async (
    requestData: Partial<UserMeInfoEditRequest>,
  ): Promise<UserMeResponse> => {
    const response = await apiClient.patch('/users/me', requestData)
    return response.data
  },
```

## 추추가

내 정보 수정 필드가 `name`, `nickname`, `phoneNumber`에서 아래와 같이 바뀜

```json
{
  "email": "test@test.com",
  "name": "test",
  "nickname": "testNick",
  "gender": "MALE",
  "birthdate": "2001-01-01",
  "phoneNumber": "010-1234-5678",
  "profileUrl": "urllllllllllllllllllll"
}
```

왜??

- 초기 기획 단계에서는 nama, nickname, phoneNumber만 변할 수 있는 값이라고 생각하여 수정 가능한 필드로 설정
- 예를 들면 생일은 변하지 않기 때문 ~~잘못 입력하는 경우는? 한번에 제대로 입력하라해~~

  <br/>

- 그리고 우리 서비스에서 최초 회원가입 후에 회원 정보를 입력받고 있는데
- name, nickname만 필수 항목이고 나머지는 선택항목임
- 그럼 초기 회원 정보 입력에서 나머지 항목을 입력하지 않았다면
- 그 사용자는 나머지 필드를 입력할 수가 없음!
- '남성' 이라고 잘못 입력하면 다신 못 바꾸는 거임...
- 그래서 내 정보 수정 request 필드가 추가된 것
  <br/>

<br/>
=> 고민했던 부분이 왜 중요한지 느낄 수 있었음
<br/>
각각 필드 상태를 관리했더라면 추가된 필드 개수만큼 또 상태를 추가했어야 됐을 것임
<br/>

그치만 나는 userData라는 하나의 객체로 묶어서 관리하고 있었기 때문에 효율적!
