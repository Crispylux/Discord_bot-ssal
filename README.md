# Discord_bot-ssal
## info: https://r-pizzza.tistory.com/149
Python(discord.py)으로 만든 **디스코드 봇**입니다. **Oracle Cloude 서버**에서 24시간 상시 구동되어, 봇을 초대하면 어떤 디스코드 서버에서든 사다리타기와 추첨 기능을 사용할 수 있습니다.
<br><br>

### 💠개발자(1인 개발)
<table>
  <tbody>
    <tr>
      <td align="center">
        <img width="200" alt=" " src="https://github.com/user-attachments/assets/367bdef8-aff6-4b76-b0a4-fb23c267543a" /><br />
        <b>정세영 (<a href="https://github.com/Crispylux">@Crispylux</a>)</b>
      </td>
    </tr>
  </tbody>
</table>
<br>

### 💠기술 스택
![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![discord.py](https://img.shields.io/badge/discord.py-2.7-5865F2?logo=discord)
![Oracle Cloud](https://img.shields.io/badge/Oracle%20Cloud-Always%20Free-F80000?logo=oracle)
| 기술 | 설명 |
|---|---|
| 언어 | Python 3.9 |
| 라이브러리 | [discord.py](https://discordpy.readthedocs.io/) 2.7 |
| 환경설정 | python-dotenv |
| 호스팅 | Oracle Cloud Infrastructure (Always Free Tier) |
| 서버 OS | Oracle Linux 9 |
| 실행 방식 | Python venv + nohup |

<br>

### 💠기능
| 기능 | 명령어 | 설명 | 파라미터 |
|---|---|---|---|
| **사다리타기** | `/사다리타기` | 참가자와 결과를 입력하면 사다리타기 결과를 텍스트로 보여줍니다. | **참가자** (필수) 쉼표로 구분한 이름 목록<br>**결과** (선택) 쉼표로 구분한 결과 목록, 참가자 수와 개수가 같아야 함. 생략 시 자동으로 당첨/꽝으로 나뉨<br>**인원** (선택, 기본 1) 결과를 생략했을 때 당첨자로 할 인원 수 |
| **추첨** | `/추첨` | 참가자 목록 중 원하는 인원을 무작위로 뽑습니다. | **참가자** (필수) 쉼표로 구분한 이름 목록<br>**인원** (선택, 기본 1) 몇 명을 뽑을지<br>**중복허용** (선택, 기본 false) 같은 사람이 여러 번 뽑힐 수 있는지 |
| **모집시작** | `/모집시작` | 이모지 반응으로 참가 신청을 받고, 주최자가 "마감하고 진행" 버튼을 누르면 그 시점 참가자 명단으로 사다리타기/추첨을 자동 실행합니다. | **제목** (필수) 모집 제목<br>**방식** (필수) 사다리타기 또는 추첨 중 선택<br>**인원** (선택, 기본 1) 당첨자/추첨 인원 수<br>**정원** (선택) 최대 참가 인원 (표시용)<br>**설명** (선택) 모집 설명 |

<br>

### 💠주요 파일
| 파일 | 설명 | 서술 |
|---|---|---|
| `bot.py` | 실행 진입점 | 봇을 로그인시키고, `cogs` 폴더의 기능들을 불러와 슬래시 커맨드로 등록합니다. |
| `cogs/ladder.py` | `/사다리타기` 명령어 처리 | 참가자·결과 입력을 받아 `utils/ladder_render.py`로 계산하고 결과를 출력합니다. |
| `cogs/draw.py` | `/추첨` 명령어 처리 | 참가자 목록에서 무작위로 인원을 뽑아 출력합니다. |
| `cogs/recruit.py` | `/모집시작` 명령어 처리 | 이모지 반응으로 참가자를 모으고, "마감하고 진행" 버튼을 누르면 사다리타기/추첨을 자동 실행합니다. |
| `utils/ladder_render.py` | 사다리타기 알고리즘 | 무작위로 가로줄(사다리 다리)을 만들고, 각 참가자가 어느 결과에 도착하는지 계산합니다. |
| `utils/parsing.py` | 사용자 입력 문자열을 정리·검증 | 쉼표/띄어쓰기 혼용 입력을 리스트로 변환하고, 참가자 수를 제한(2~20명) 체크합니다. |
| `requirements.txt` | 필요한 파이썬 라이브러리 목록 | `discord.py`, `python-dotenv` |
| `.env.example` | 환경변수 설정 예시 파일 | 실제 사용 시 `.env`로 복사해서 봇 토큰을 입력합니다. |

<br><br><br>



## 🍚[봇]쌀 설명

### 🌾기능: 사다리타기, 추첨 <br>

### 🌾사용 방법
`[ ]`는 생략 가능합니다.

| 기능 | 명령어 | 예시 |
|---|---|---|
| **사다리타기** | `/사다리타기 참가자: (이름1),(이름2) 결과: (결과1),(결과2)` | `/사다리타기 참가자: 쌀1, 쌀2, 쌀3 결과: 탱커, 딜러, 힐러` |
| **추첨** | `/추첨 참가자: (이름1),(이름2),(이름3) 인원: (인원수) [중복허용]` | `/추첨 참가자: 쌀1, 쌀2, 쌀3 인원: 1` |
| **모집** | `/모집시작 제목: (제목) 방식: (사다리타기or추첨) [당첨인원: (인원수)] [정원: (인원수)]` | `/모집시작 제목: 빠대할 사람 모집 방식: 사다리타기 정원: 5` |

> 💡 모집: 이모지에 체크하면 사다리타기/추첨에 참여할 수 있습니다.
<img width="1020" height="653" alt="image" src="https://github.com/user-attachments/assets/1911b69c-a900-44e9-ae17-3399e182b74c" />

<br><br>

## 🍚구동 화면
### 🌾사다리타기

<img width="385" height="150" alt="image" src="https://github.com/user-attachments/assets/d6c9f6b2-5493-4b35-aca1-e78aaaf920d3" />

https://github.com/user-attachments/assets/9582fe39-0066-4828-ab79-39e08960a07a

<br><br>

### 🌾추첨

<img width="344" height="190" alt="image" src="https://github.com/user-attachments/assets/57b8ee37-8feb-4084-9ceb-243966d804f9" />

https://github.com/user-attachments/assets/b45bff1d-0f23-4017-90ed-e16f93841448

<br><br>

### 🌾모집

<img width="422" height="408" alt="image" src="https://github.com/user-attachments/assets/c41b5470-2f2b-43d0-8e01-6db082a67286" />

https://github.com/user-attachments/assets/bb206b20-4f6f-4e9f-8046-21e45b2bdd82





