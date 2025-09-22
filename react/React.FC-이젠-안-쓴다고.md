타입스크립트를 쓸 때 아무 생각 없이 아래와 같은 형태로 작성했었다.<br/>

`const Login:React.FC<LoginProps> = ({props}) => {}`

그런데 React.FC는 이제 옛날 거라는 얘기를 듣고 찾아보게 되었다.

## React.FC란?

- Function Component의 줄임말
- react + ts 조합으로 개발할 때 사용하는 함수형 컴포넌트에 사용하는 타입

## React.FC 사용을 지양해야 하는 이유

### 1. children

React.FC를 사용하면 props에 기본적으로 children이 들어가 있음<br/>

정확한 타입을 지정해 주기 위해 ts를 사용하는데 React.FC를 사용하면 children이 있을 수 있다는 것을 가정하기 때문에 타입이 명확하지 않다는 단점 존재

### 2. 제네릭 지원 X

```ts
type GenericComponentProps<T> = {
  prop: T;
  callback: (t: T) => void;
};
const GenericComponent = <T>(props: GenericComponentProps<T>) => {
  /* ... */
};
```

위와 같이 제네릭을 사용할 수 있지만 React.FC를 사용하면 T를 넘겨줄 방법이 없기 때문에 제네릭을 사용할 수 없다.

```ts
const GenericComponent: React.FC</*...*/> = <T>(
  props: GenericComponentProps<T>
) => {
  /*...*/
};
```

React.FC는 타입 자체가 제네릭을 외부에서 주입받을 수 있는 구조가 아님<br/>
React.FC는 Props의 타입만을 제네릭으로 받도록 설계되어 있음

<br/>

**제네릭이란?**
: 타입을 파라미터로 받는 기능<br/>

클래스나 함수, 인터페이스 등을 다양한 타입에서 재사용할 수 있도록 만들어 줌<br/>
컴포넌트나 함수를 사용하는 시점에 타입을 결정하게 하는 도구<br/>
재사용성 & 타입 안정성 ↑

1. 제네릭이 없는 경우 - 숫자만 처리, 문자열만 처리하는 함수 각각 따로 작성

```ts
function getFirstElementNumber(arr: number[]): number {
  return arr[0];
}

function getFirstElementString(arr: string[]): string {
  return arr[0];
}

const num = getFirstElementNumber([1, 2, 3]); // 1
const str = getFirstElementString(["a", "b", "c"]); // 'a'
```

2. 제네릭 사용

```ts
function getFirstElement<T>(arr: T[]): T {
  return arr[0];
}

const num = getFirstElement<number>([1, 2, 3]); // 1
const str = getFirstElement<string>(["a", "b", "c"]); // 'a'
```

### 3. 네임 스페이스 패턴 이용 시 불편해짐

1. FC를 사용하지 않을 때

```ts
const Select = (props: SelectProps) => {
  /*...*/
};

Select.Item = (props: ItemProps) => {
  /*...*/
};
```

2. FC 사용

```ts
const Select: React.FC<SelectProps> & { Item: React.FC<ItemProps> } = (
  props
) => {
  /*...*/
};
```

- `&` : 교차 타입이라는 뜻, 두 개 이상의 타입을 가짐
- SelectProps와 ItemProps 속성을 가진다는 뜻

**네임 스페이스 패턴이란?**
서로 관련된 컴포넌트들을 하나의 부모 컴포넌트 객체 아래에 속성처럼 묶어서 관리하는 기법

```ts
import Select from "./Select";

<Select>
  <Select.Label>과일</Select.Label>
  <Select.Item>사과</Select.Item>
</Select>;
```

```ts
// Select 컴포넌트

const Select = (props) => {
  // 1. 부모 컴포넌트
  return <div className="select-box">{props.children}</div>;
};

const Item = (props) => {
  // 2. 자식 컴포넌트
  return <div className="select-item">{props.children}</div>;
};

Select.Item = Item; // 3. 부모(Select)에 자식(Item)을 속성으로 붙여주기 -> // js에서 함수도 객체이므로 속성을 가질 수 있음

export default Select;
```

## 결론

React.FC는 react 18 이상에서는 없어짐 [해당 PR](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/56210)

아래처럼 사용하자!

```ts
const Component = (props: ComponentProps) => {};
```

React.FC를 사용하면 코드가 조금 더 길어진다는 이유도 있었는데 1번 이유를 제외하고는 React.FC를 무조건 지양해야 한다고는 생각이 들지 않았다.
그럼에도 타입스크립트를 사용하는 목적에 있어서는 React.FC를 사용하지 않는 게 맞다고 생각이 든다.
