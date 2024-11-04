import React, { useContext } from 'react';
import styled from 'styled-components';
import { Context } from '../context/Context';
import logo from '../assets/defaultlogo.png'
const SubContainer = styled.div`
  display: flex;
  justify-content: space-between;
  width: 100%;
`;

const P = styled.h1`
  height: 50px;
  margin: 0.5rem 2rem 2rem 2rem;
  padding: 10px 10px;
  color: #fff;
  font-size: 2rem;
  font-weight: 600;
  &:hover {
    // background: linear-gradient(135deg, #3a5da8, #2a406c);
    border-radius: 8px;
    cursor: pointer;
    transition: 0.3s ease;
  }
`;

const Img = styled.img`
  width: 70px;
  height: 70px;
  margin: 0.5rem 2rem 0 2rem;
  padding: 10px 10px;
  border-radius: 50%;
  cursor: pointer;
`;

const Username = styled.p`
  color: #fff;
  font-size: 1.2rem;
  margin: 0 -1rem 0 0;
  display: flex;
  align-items: center;
  justify-content: center;
  text-transform: capitalize;
`;

const Navbar = () => {
  const { username, photo } = useContext(Context);

  const photoUrl = photo ? `http://localhost:5000/uploads/${photo}` : logo;

  return (
    <SubContainer>
      <P>Procura</P>
      <div style={{ display: "flex", alignItems: "center" ,marginBottom:"0.5rem"}}>
        {username && <Username>{username}</Username>}
        <Img src={photoUrl} alt='user photo' />
      </div>
    </SubContainer>
  );
};

export default Navbar;
