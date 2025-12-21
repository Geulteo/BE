📖 자연어처리 - 기말 프로젝트 📖  

- 🧾 **프로젝트명**: 글터(Geulter) - 상황별 글쓰기 AI
- ⏳ **진행 기간**: 2025.11.12 ~ 2025.12.21  

<br>

## 👨‍👩‍👧‍👦 구성원

### 🖥️ Front-End

| Name | Role | GitHub |
|------|------|--------|
| 김채린 | Front-End Developer | [@chaeelin](https://github.com/chaeelin) |
| 김태규 | Front-End Developer | [@AiSamdasu](https://github.com/AiSamdasu) |

### 🛠️ Back-End

| Name | Role | GitHub |
|------|------|--------|
| 김채린 | Back-End Developer | [@chaeelin](https://github.com/chaeelin) |
| 김태규 | Back-End Developer | [@AiSamdasu](https://github.com/AiSamdasu) |
| 김정호 | Back-End Developer | [@wjdgh123](https://github.com/wjdgh123) |
| 최아원 | Back-End Developer | [@WAcAW9](https://github.com/WAcAW9) |

<br>

## 📝 개요

**핵심 키워드 기반 상황별 글쓰기 AI 서비스**로, 
<br>
사용자가 단어만 입력해도 상황·의도·대상에 맞는 문장을 자동으로 구성하고, 난이도 진단과 개선 피드백을 통해 표현력을 자연스럽게 향상시킬 수 있도록 설계된 서비스

<br>  

## 📝 핵심 기능

## 1. 키워드 기반 문장 생성
사용자가 입력한 키워드와 옵션(대상, 톤, 길이)을 기반으로 AI가 상황에 맞는 문장을 자동 생성합니다.

<br> 

## 2. 문장 재생성 및 수정
같은 조건으로 다른 버전의 문장을 생성하거나, 톤/길이를 조절하여 문장을 수정할 수 있습니다.

<br>

## 3. 문장 추천
사용자가 과거에 생성했던 문장들을 SBERT 임베딩 벡터로 저장해 두었다가, 현재 입력한 문장과 의미적으로 유사한 문장을 다시 추천해줍니다.

<br> 

## 4. TTS(음성 합성)
생성된 문장을 음성으로 변환하여 대신 읽어주는 기능으로, 전화 통화 등에 활용할 수 있습니다.

<br> 

## 5. 연습 모드 A - 직접 작성 연습
주어진 상황에 맞는 문장을 직접 작성하고, AI가 정중함/명확성/이해도 기준으로 평가 및 피드백을 제공합니다.

<br> 

## 6. 연습 모드 B - 표현 바꾸기 연습
주어진 문장을 다른 톤(반말→존댓말 등)으로 바꾸는 연습을 하고, AI가 변환 결과를 평가합니다.

<br> 

## 7. 사용자 인증 (회원가입/로그인)
JWT 기반 인증 시스템으로 사용자별 세션 관리 및 개인화된 히스토리를 제공합니다.

<br>
                                                                                                                                                        
## 🛠 기술 스택

## 💻 Front-End Stack

| Category              | Tech Stack |
|-----------------------|------------|
| **Language**          | <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white"> |
| **Framework** | ![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black) |
| **Version Control**   | ![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white) |

## 💻 Back-End Stack

| **Category**       | **Tech** |
|--------------------|----------|
| **Language**       | <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"> |
| **Framework**      | <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white"> |
| **Database**       | <img src="https://img.shields.io/badge/Qdrant-FF4F00?style=flat-square&logo=qdrant&logoColor=white"> <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white"> |
| **Version Control**| <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white"> |

<br>

## 🧾 발표 자료
<img width="1920" height="1080" alt="아원님  발표 자료01_시작" src="https://github.com/user-attachments/assets/c17df079-e8a5-4a71-a057-9e18c4dbf190" />
<img width="1920" height="1080" alt="아원님  발표 자료02_목차" src="https://github.com/user-attachments/assets/450766d1-59e6-4403-b905-985b0601e037" />
<img width="1920" height="1080" alt="아원님  발표 자료03_기획 배경" src="https://github.com/user-attachments/assets/90c3a6ce-4cd5-4ea5-b588-f0d2e05a3a6a" />
<img width="1920" height="1080" alt="아원님  발표 자료04_메인기능01" src="https://github.com/user-attachments/assets/06678397-e440-4c3b-a24c-45072f9d9e76" />
<img width="1920" height="1080" alt="아원님  발표 자료05_메인기능02" src="https://github.com/user-attachments/assets/6080accb-12ed-41cc-8acb-4c5151a08e87" />
<img width="1920" height="1080" alt="채린  발표 자료06_메인기능03" src="https://github.com/user-attachments/assets/31a1e087-c481-48df-a21c-2853c8dcf467" />
<img width="1922" height="1080" alt="채린  발표 자료07_메인기능04" src="https://github.com/user-attachments/assets/2f312f55-3555-4ec5-b7e5-22fc09604bc6" />
<img width="1922" height="1080" alt="채린  발표 자료08_메인기능05" src="https://github.com/user-attachments/assets/c4a13d25-c93f-4072-9f2c-9a6a8d5888e9" />
![채린  발표 자료09_메인기능06](https://github.com/user-attachments/assets/b86b9cba-4353-463b-97dc-bf3f0d0ea007)
<img width="1920" height="1080" alt="채린  발표 자료10_수정01" src="https://github.com/user-attachments/assets/7ed09858-2be2-413c-904f-3d02b939b8f6" />
<img width="1920" height="1080" alt="채린  발표 자료11_수정02" src="https://github.com/user-attachments/assets/d43a7934-366f-495c-8d51-1584ee3479b4" />
<img width="1920" height="1080" alt="채린  발표 자료12_추천01" src="https://github.com/user-attachments/assets/5dd90f11-98fd-4887-beda-afe7e19f4b03" />
<img width="1920" height="1080" alt="채린  발표 자료13_추천02" src="https://github.com/user-attachments/assets/701719dd-f5ad-4b73-936f-5f5cfd5599e7" />
<img width="1920" height="1080" alt="태규님  발표 자료14_진단01" src="https://github.com/user-attachments/assets/a97682d9-ad6c-48c1-a321-213b61aafb58" />
<img width="1920" height="1080" alt="태규님  발표 자료15_진단02" src="https://github.com/user-attachments/assets/15fb6267-87f6-47f6-9c3c-721100bee4b2" />
<img width="1920" height="1080" alt="태규님  발표 자료16_진단02" src="https://github.com/user-attachments/assets/7882733a-47fb-4583-beb6-71602c9fc1a3" />
<img width="1920" height="1080" alt="태규님  발표 자료17_연습01" src="https://github.com/user-attachments/assets/1e59ebf5-66c5-4aba-850b-95aa53e37f21" />
![태규님  발표 자료18_연습02](https://github.com/user-attachments/assets/021b6d61-e09a-4571-96e1-ed35dd362a1e)
![태규님  발표 자료19_연습03](https://github.com/user-attachments/assets/923a35f8-c6e0-4480-b820-c7d2399300f4)
<img width="1920" height="1080" alt="정호님  발표 자료21_팀원" src="https://github.com/user-attachments/assets/083960e0-c9f3-4a00-99dc-e4a3502973c8" />
<img width="1920" height="1080" alt="정호님  발표 자료22_개발 스택" src="https://github.com/user-attachments/assets/fc70fd1a-4a0c-43e6-af3a-b2ddbc90a698" />
