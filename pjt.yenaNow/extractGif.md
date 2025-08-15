## 영상을 gif 로 변환하기

> ffmpeg 라이브러리 사용

[`https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.5/dist/ffmpeg.min.js`](https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.5/dist/ffmpeg.min.js)

`ffmpeg -i video.mp4 -ss 3 -t 5 -vf "fps=15,scale=1080:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" -loop 0 output.gif`

**변환 옵션 파라미터 설명**

1. 시작 지점 (5초부터 시작)

   `-ss 5`

2. 전체 길이 (10초)

   `-t 10`

3. 반복 설정 (0: 무한반복, 1: 반복없음, n: n+1회 반복)

   `-loop 0`

4. [비디오 필터 옵션들](https://trac.ffmpeg.org/wiki/FilteringGuide)

- `-vf "..."` 이 사이에 넣어주면 됨.
  - `fps`: 초당 프레임
  - `scale=width:height`: 절대값(예: 320), 원본대비(예: iw/2), 종횡비유지자동조절(-1)
  - `flags=lanczos`: 스케일링 알고리즘 선택

5. 커스텀 팔레트 사용(split filter 사용해서 임시파일 생성하지 않음)

`palettegen`, `paletteuse`
