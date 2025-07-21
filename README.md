## 환경 변수 설정

AI 챗봇으로 Hugging Face Inference API를 사용합니다.
API 키를 Hugging Face 계정에서 발급받아야 하며, 아래와 같이 설정해주세요.

### 1. '.env' 파일 설정

/backend 에 '.env' 파일을 만들고 다음 내용을 추가합니다.

`HF_API_TOKEN=your_huggingface_api_token_here`

- your_huggingface_api_token_here 자리에 발급 받은 키로 교체하세요.

### 2. API 키 발급 방법

1. [Hugging Face 웹사이트](https://huggingface.co/)에 로그인
2. 우측 상단 프로필 > Settings > Access Tokens 메뉴 이동
3. 'New token' 생성 후, 발급 받은 토큰 복사
4. 위 `.env` 파일에 붙여넣기
