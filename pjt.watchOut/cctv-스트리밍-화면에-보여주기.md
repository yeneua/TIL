### cctv 모니터링 페이지

cctv를 보여줄때 이미지 태그에 api 주소를 넣어서 불러오고 있음

```ts
<img css={iFrameBox} src={`${API_BASE_URL}${cctv.springProxyUrl}`}></img>
```

따라서 이미지를 요청할 때 `Authorization` 헤더에 `accessToken`을 담아서 보내지 않기 때문에 401 에러 발생

**찾아 본 해결 방법**

=> fetch + blob URL 사용하기

1. fetch를 사용해서 헤더에 토큰을 포함시켜 데이터 요청하기
2. 서버로 받은 데이터를 blob 형태로 변환
3. `URL.createObjectURL()` 메서드를 사용해서 해당 blob 가리키는 임시 url 생성
4. 그 임시 url을 img 태그 src에 넣기

-> 안됨
백엔드 서버에서 `permitAll()`하는 식으로 처리함

**cctv 화면 보여주는 프로세스**

1. `/cctv/infer/start-all`
   위 주소로 POST 요청을 보내서 카메라를 켠다

2. `/cctv/views/area`
   GET 요청을 보내서 `response`로 오는 `springProxyUrl` 앞에 서버 주소를 붙여서 이미지 태그로 보여주기

   ```ts
   export interface CctvViewAreaItem {
     uuid: string;
     name: string;
     springProxyUrl: string;
     fastapiMjpegUrl: string;
     online: boolean;
   }

   export interface CctvViewAreaResponse {
     areaUuid: string;
     useFastapiMjpeg: boolean;
     items: CctvViewAreaItem[];
   }

   <div key={cctv.uuid} css={cell}>
     <img css={iFrameBox} src={`${API_BASE_URL}${cctv.springProxyUrl}`}></img>
     <div css={labelBox}>
       <p>{cctv.name}</p>
     </div>
     <div css={overlay} onClick={() => onCctvClick(cctv)}></div>
   </div>;
   ```

**BLOB이란?**

BLOB(Binary Large Object)

: 크기가 큰 바이너리 데이터를 저장하고 다루기 위한 데이터 타입

파일 그 자체를 덩어리로 취급하는 객체

1. db에서 blob

   이미지, 동영상, 소리 파일, pdf 등 구조화되지 않은 대용량 바이너리 데이터를 컬럼에 직접 저장할 때 사용

2. 웹 개발에서의 blob

- 불변(immutable)하는 원시 데이터를 다룰 때 유용하게 사용됨
- 파일 다운로드 : 서버에서 받은 데이터나 사용자 생성 데이터를 blob으로 만들어 파일처럼 다운로드하게 할 수 있음
- 파일 분할 및 전송 : 대용량 파일을 작은 blob으로 나누어 서버에 업로드 가능
- 임시 URL 생성 : URL.createObjectURL() 메서드를 사용해 blob 데이터를 고유한 URL 생성 가능, img 태그의 src나 a 태그의 href 속성에 사용하여 이미지 미리보기나 파일 접근에 활용

**바이너리 데이터**

바이너리 데이터 : 0과 1로만 이루어진 데이터 텍스트가 아닌 모든 종류의 데이터를 말함

텍스트 데이터 : 사람이 읽고 이해할 수 있는 문자로 구성된 데이터

(바이너리 데이터 예시)

- 이미지 파일: JPG, PNG, GIF

- 오디오 파일: MP3, WAV

- 비디오 파일: MP4, AVI

- 문서 파일: PDF, DOCX(MS Word), HWP(한컴)

- 실행 파일: EXE, DMG

- 압축 파일: ZIP, RAR

  -> 이 파일들을 보려면 전용 프로그램으로 열어서 해석해야함(이미지 뷰어, 워드 등)
