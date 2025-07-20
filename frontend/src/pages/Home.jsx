import { useEffect, useState } from "react";
import { getMyMembership } from "../api";
import { Link } from "react-router-dom";

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [membership, setMembership] = useState(null);

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

  return (
    <div>
      <h1>home</h1>
      {isLoggedIn ? (
        membership ? (
          <div>
            <h2>내 멤버십</h2>
            <p>이름: {membership.membership_type.name}</p>
            <p>만료일: {membership.end_date}</p>
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
