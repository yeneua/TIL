## 1. 호출 스케줄링

**호출 스케줄링**

- 일정 시간이 경과된 이후에 호출되도록 함수 호출을 예약하려면 타이머 함수를 사용해야함
- 이를 호출 스케줄링이라고 함

<br/>

- 타이머 생성 함수 : `setTimeout`, `setInterval`
- 타이머 제거 함수 : `clearTimeout`, `clearInterval`

→ ECMAScript 빌트인 함수X

→ 브라우저, Node.js 전역 객체 메서드로서 타이머 함수 제공

⇒ **타이머 함수는 호스트 객체**

<br/>

타이머 함수는 타이머가 만료되면 콜백 함수를 호출함

- `setTimeout` - 타이머 만료 시 한 번 호출
- `setInterval` - 타이머 만료될 때마다 반복 호출

자바스크립트 엔진은 **싱글 스레드(single thread)** 로 동작 => 타이머 함수는 **비동기(asynchronous)처리 방식**으로 동작

## 2. 타이머 함수

### 2.1 setTimeout / clearTimeout

**`setTimeout`**

단 한 번 동작하는 타이머 생성

```javascript
setTimeout(func[, delay, param1, param2, ...])
```

- func : 타이머 만료 뒤 호출될 콜백 함수
- delay : 타이머 만료 시간, 밀리초(ms) 단위(1초가 1000ms), 기본값은 0
- param1 : 콜백 함수에 전달해야 할 인수가 존재하는 경우 세번째 이후 인수로 전달 가능

```javascript
setTimeout(() => console.log('hi'), 1000) // 1초(1000ms)후 타이머가 만료되면 콜백 함수 호출
```

<br/>

**`clearTimeout`**

setTimeout 함수가 반환한 타이머 id를 clearTimeout 함수의 인수로 전달하여 타이머 취소 가능(호출 스케줄링 취소)

- 브라우저 환경 : 타이머 id가 숫자
- Node.js 환경 : 타이머 id가 객체

```javascript
const timerId = setTimeout(() => console.log('hi'), 1000)
clearTimeout(timerId)
```

- clearTimeout 함수로 타이머를 취소함
- 콘솔에 출력되지 않음

_궁금해서 알아본 것_<br/>
위 코드에서 1000ms 안에 clearTimeout 함수를 호출하지 못하면 타이머 함수가 실행됨

```javascript
// 1.
const timerId = setTimeout(() => console.log('hi'))
clearTimeout(timerId)

// 2.
const timerId = setTimeout(() => console.log('hi'))

const myClear = () => {
  clearTimeout(timerId)
}

setTimeout(myClear, 10000)
// hi
```

1번 코드에서 콘솔이 찍히지 않음!<br/>
setTimeout 함수에서 지연 시간을 생략하면 기본값은 0초이지만 **즉시 호출이 아니라** 함수 등록 시간을 지연 시키는 것임(4초 이후에 실행)

따라서 clearTimeout 함수 호출을 타이머 함수 호출 보다 늦게 실행하면 타이머 함수가 실행되어 콘솔이 출력됨!

### 2.2 setInterval / clearInterval

**`setInterval`**
반복 동작하는 타이머 생성<br/>
타이머가 만료될때마다 콜백 함수가 반복 호출<br/>
타이머가 취소될때까지 반복<br/>
delay 시간이 경과할 때마다 반복 실행되도록 호출 스케줄링<br/>

```javascript
setInterval(func[, delay, param1, param2, ...])
```

<br/>

**`clearInterval`**

타이머 id를 이용해 타이머 취소

- 브라우저 환경 : 타이머 id가 숫자
- Node.js 환경 : 타이머 id가 객체

```javascript
let count = 1
const timeoutId = setInterval(() => {
  console.log(count) // 1 2 3 4 5
  if (count++ === 5) clearInterval(timeoutId)
}, 1000)
```

## 3. 디바운스와 스로틀

디바운스와 스로틀은 짧은 시간 간격으로 연속해서 발생하는 이벤트를 그룹화해서 과도한 이벤트 핸들러의 호출을 방지하는 프로그래밍 기법

이벤트 처리 시 유용하게 사용 가능

### 3.1 디바운스(debounce)

짧은 시간 간격으로 이벤트가 연속해서 발생하면 이벤트 핸들러를 호출하지 않다가 시간이 경과한 이후에 이벤트 핸들러가 한 번만 호출되도록 함

=> 짧은 시간 간격으로 발생하는 이벤트를 그룹화해서 마지막에 한번만 이벤트 핸들러가 호출되도록 함

<br/>

```html
<body>
  <input type="text" />
  <div class="msg"></div>
  <script>
    const $input = document.querySelector('input')
    const $msg = document.querySelector('.msg')

    const debounce = (callback, delay) => {
      let timerId

      return (event) => {
        if (timerId) clearTimeout(timerId)
        timerId = setTimeout(callback, delay, event)
      }
    }

    $input.oninput = debounce((e) => {
      $msg.textContent = e.target.value
    }, 300)
  </script>
</body>
```

- input 이벤트는 사용자가 값을 입력할 때마다 연속해서 발생
- 사용자가 입력을 완료했는지 여부는 알 수 없으니 300ms 동안 입력하지 않으면 완료된 것으로 간주

- `debounce` 함수 안에서
  - 이전 `setTimeout` 예약이 있으면 === `timerId`가 있으면 타이머 취소
  - 새로운 콜백을 300ms 뒤에 실행하도록 예약
- 300ms 동안 입력이 없으면 타이머에 등록된 콜백 실행(`msg.textContent = e.target.value`) -> 화면에 입력값 출력됨

  <br/>

```javascript
return (event) => {
  if (timerId) clearTimeout(timerId)
  timerId = setTimeout(callback, delay, event)
}
```

- 클로저 함수 : 외부 변수 기억하는 함수
- 이 함수가 timerId 변수를 계속 기억하고 있음(참조하고 있음)
- 다음 input 이벤트가 발생해서 debounce가 실행될때 이전 timerId에 접근해서 이전 타이머를 clear 할 수 있는 것

### 3.2 스로틀(throttle)

짧은 시간 간격으로 이벤트가 연속해서 발생하더라도 일정 시간 간격으로 이벤트 핸들러가 최대 한 번만 호출되도록 함

=> 짧은 시간 간격으로 발생하는 이벤트를 그룹화해서 일정 시간 단위로 이벤트를 그룹화해서 일정 시간 단위로 이벤트 핸들러가 호출되도록 호출 주기 만듦

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      .container {
        width: 300px;
        height: 300px;
        background-color: rebeccapurple;
        overflow: scroll;
      }

      .content {
        width: 300px;
        height: 1000vh;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="content"></div>
    </div>
    <div>
      일반 이벤트 핸들러가 scroll 이벤트를 처리한 횟수:
      <span class="normal-count">0</span>
    </div>
    <div>
      스로틀 이벤트 핸들러가 scroll 이벤트를 처리한 횟수:
      <span class="throttle-count">0</span>
    </div>

    <script>
      const $container = document.querySelector('.container')
      const $normalCount = document.querySelector('.normal-count')
      const $throttleCount = document.querySelector('.throttle-count')

      const throttle = (callback, delay) => {
        let timerId

        return (event) => {
          if (timerId) return
          timerId = setTimeout(() => {
            callback(event)
            timerId = null
          }, delay)
        }
      }

      let normalCount = 0
      $container.addEventListener('scroll', () => {
        $normalCount.textContent = ++normalCount
      })

      let throttleCount = 0
      $container.addEventListener(
        'scroll',
        throttle(() => {
          $throttleCount.textContent = ++throttleCount
        }, 100)
      )
    </script>
  </body>
</html>
```

- delay 시간이 경과하기 이전에 이벤트가 발생하면 아무것도 하지 않음
- delay 시간 경과 이후에 이벤트가 발생하면 콜백 함수를 호출하고 새로운 타이머 재설정
- delay 시간 간격으로 콜백 함수가 호출됨
