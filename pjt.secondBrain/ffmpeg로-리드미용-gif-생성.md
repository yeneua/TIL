<small>리드미에 들어갈 gif 만들기<br/>gif 변환 사이트 무료 리미트에 걸려서 ffmpeg 명령어로 만들었다.<br/>샤라웃투 예나 나우...</small>

### mp4 to gif

```bash
ffmpeg -i input.mp4 -vf "fps=15,scale=960:-1:flags=lanczos,palettegen" input.png
ffmpeg -i input.mp4 -i input.png -lavfi "fps=15,scale=960:-1:flags=lanczos [x]; [x][1:v] paletteuse" output.gif
```

- 중간 png 만드는 단계가 있는 이유 => GIF 색상 팔레트를 생성하기 위해
- gif는 최대 256색만 사용할 수 있는 형식임
- 영상을 그대로 변환하면 색 표현이 제대로 안될 수 있음
- 따라서 gif에 사용할 256개 색을 뽑아 저장한 색상표(palette)를 만듦
- gif 생성시 색상 팔레트 적용하면 더 깨끗한 색감의 gif 생성 가능

### mp4 자르기

```bash
ffmpeg -ss 0 -i input.mp4 -t 6 -c:v libx264 -c:a aac part1.mp4 # 시작 ~ 6초
ffmpeg -ss 00:01:01 -i input.mp4 -c:v libx264 -c:a aac part2.mp4 # 1분 1초 ~ 끝
ffmpeg -ss 20 -i input.mp4 -to 25 -c:v libx264 -c:a aac output.mp4 # 20초 ~ 25초
```

### mp4 영상 연결

```bash
# 방법1. 영상 형식이 모두 동일한 경우 - 빠르고 품질 손실이 없지만 영상 형식이 모두 동일해야함

# list.txt 파일 생성
file 'input1.mp4'
file 'input2.mp4'

# ffmpeg 실행
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# 방법2.
ffmpeg -i "part1.mp4" -i "part2.mp4" -i "part3.mp4" -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a] concat=n=3:v=1:a=1 [v][a]" -map "[v]" -map "[a]" -c:v libx264 -c:a aac output.mp4
```

### mp4 배속

```bash
ffmpeg -i input.mp4 -filter:v "setpts=1/1.5\*PTS" -an output.mp4
```

`-an` → 오디오 제거 옵션, 해당 옵션을 제거하면 영상만 배속됨
