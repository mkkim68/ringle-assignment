import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api";

export const login = async (username, password) => {
  try {
    const res = await axios.post(`${BASE_URL}/login/`, {
      username,
      password,
    });

    const token = res.data.token;
    localStorage.setItem("token", token);

    console.log("로그인 성공");
  } catch (err) {
    console.error("로그인 실패");
  }
};

export const getMyMembership = async () => {
  const token = localStorage.getItem("token");
  try {
    const res = await axios.get(`${BASE_URL}/my-membership/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    return res.data;
  } catch (err) {
    console.error("멤버십을 불러오지 못했습니다.");
    return null;
  }
};

export const consumeCoupon = async (kind) => {
  const token = localStorage.getItem("token");
  try {
    const res = await axios.post(
      `${BASE_URL}/use-coupon/`,
      { kind: kind },
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );
  } catch (err) {
    console.error("api: 쿠폰 사용 실패");
  }
};
