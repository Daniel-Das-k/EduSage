import React from 'react'
import styled from 'styled-components'
import { CiSettings } from "react-icons/ci";
const Container=styled.div`
display:flex;
justify-content:start;
align-items:center;
gap:8px;
margin:0 0 1rem 0;
padding:17px 0 0 1.5rem;
cursor:pointer;
transition:0.1s linear;
font-size:18px;
border-top:1px solid #fff;
// &:hover{
// background:#676767;
// color:#fff;
// border-radius:7px;

// }

`
const FooterSide = () => {
  return (
    <Container>
      <CiSettings style={{fontSize:"40px"}}/>
      <p>Settings</p>
    </Container>
  )
}

export default FooterSide
