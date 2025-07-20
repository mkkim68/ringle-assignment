import { useEffect, useState } from "react";
import { getMyMembership, consumeCoupon } from "../api";
import { Link, useNavigate } from "react-router-dom";

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [membership, setMembership] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsLoggedIn(true);
      getMyMembership().then((data) => {
        if (data) {
          setMembership(data);
          console.log(data);
        }
      });
    }
  }, []);
  const canChat = membership && membership.is_active;

  const handleEnterChat = async () => {
    try {
      await consumeCoupon("conversation");
      navigate("/chat");
    } catch (err) {
      console.error("Home: 쿠폰 사용 실패");
    }
  };

  return (
    <div>
      <h1>home</h1>
      {isLoggedIn ? (
        membership ? (
          <div>
            <h2>내 멤버십 정보</h2>
            <p>이름: {membership.membership_type.name}</p>
            <p>만료일: {membership.end_date}</p>
            <p>
              남은 대화 횟수:{" "}
              {membership.remaining_conversations === -1
                ? "무제한"
                : membership.remaining_conversations}
            </p>
            <p>
              남은 분석 횟수:{" "}
              {membership.remaining_analyses === -1
                ? "무제한"
                : membership.remaining_analyses}
            </p>
            {canChat && (
              <button onClick={handleEnterChat}>AI 채팅방 입장하기</button>
            )}
          </div>
        ) : (
          <p>멤버십 정보를 불러오는 중...</p>
        )
      ) : (
        <div>
          <h2>로그인을 해주세요</h2>
          <Link to="/login">로그인하러 가기</Link>
        </div>
      )}
    </div>
  );
}

export default Home;
