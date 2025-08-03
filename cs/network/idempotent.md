**멱등성(Idempotent)**

멱등하다 === 첫 번째 수행을 한 뒤 여러 차례 적용해도 결과를 변경시키지 않는 작업 또는 기능의 속성

즉, 멱등한 작업의 결과는 한 번 수행하든 여러 번 수행하든 같음

리소스 관점에서 생각!! -> 여러 번 요청해도 리소스가 동일하다면 멱등한 것으로 봐도 됨

| 메서드 | 멱등성 |
| :----: | :----: |
|  GET   |   O    |
|  POST  |   X    |
| DELETE |   O    |
|  PUT   |   O    |
| PATCH  |   X    |

-> 멱등성이 왜 필요할까?

- 요청의 재시도 때문
- 만약 HTTP 요청이 멱등하다면 실패해도 그냥 다시 재요청하면 됨
- 멱등성을 고려해서 재시도 요청해야함

1. GET

- 같은 요청을 N번 호출해도 동일하게 같은 결과가 조회됨
- 같은 요청을 여러 번 보내더라도 서버의 상태는 항상 같음

2. POST

- 요청을 새로 보낼때마다 매번 새로운 자원이 생겨남 === 서버의 상태가 변함
- 만약 서버에서는 정상 처리했는데 응답 과정에서 네트워크 문제로 응답을 받지 못했다면?
  - 다시 POST 재요청을 하면 서버에서는 한 번 더 처리함
  - 이게 만약에 결제 서비스였다면?

3. DELETE

- 처음에 자원이 있는 상태에서 DELETE 요청을 보냄 -> 삭제 성공(200)
- 다시 DELETE 요청 -> 404 NOT FOUND
- 응답 코드와 상관 없이 DELETE를 여러번 호출해도 서버는 자원이 없는 상태를 유지함

4. PUT

- PUT은 자원을 덮어씌워서 변경하거나 자원이 없다면 추가함
- 자원이 없으면 POST처럼 동작하는데 새로운 자원을 만드는 게 아니라 덮어씀
- 한 번, 여러 번 요청하든 서버의 상태는 같음
- 자원을 완전히 교체해버리기 때문에 멱등한 것
- 그전에 무엇이 있던 말던 상관없이 그냥 넣겠다는 의미로 생각

5. PATCH

- 기존의 상태에서 어떠한 상태로 변경
- 멱등하지 않은 patch 요청은 보통 현재 상태를 기준으로 업데이트일 때 발생함
- `{ point : +10 }` 한번 호출할 때마다 10이 더해짐 -> 멱등하지 않음
- 그럼 멱등한 PATCH도 있는건가?
- `{ name: "kim" }` 이렇게 요청을 보내면 이름을 고정으로 지정 -> 멱등함

=> patch는 요청 방식에 따라 멱등할 수도 아닐 수도 있음

## 참고한 글

[[HTTP] HTTP 메소드의 멱등성(Idempotent)과 Delete 메소드가 멱등한 이유](https://mangkyu.tistory.com/251)

[POST, PUT, PATCH의 차이점](https://docs.tosspayments.com/blog/rest-api-post-put-patch#post-put-patch의-차이점)

[멱등성이 뭔가요?](https://docs.tosspayments.com/blog/what-is-idempotency#멱등성이-뭔가요)

[Patch 메서드가 멱등이 아닌 이유](https://www.inflearn.com/community/questions/110644/patch-%EB%A9%94%EC%84%9C%EB%93%9C%EA%B0%80-%EB%A9%B1%EB%93%B1%EC%9D%B4-%EC%95%84%EB%8B%8C-%EC%9D%B4%EC%9C%A0?srsltid=AfmBOop0o8AjG5J70l0hPOafimeR6oSjVIEUL_vhkGa1KoxwSQopY-Cv)
