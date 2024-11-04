import React, { useContext } from 'react'
import styled from 'styled-components'
import { PiOpenAiLogoLight } from "react-icons/pi";
import { MdOpenInNew } from "react-icons/md";
import { Context } from '../context/Context';
import vqlogo from '../assets/llogo.png'
const Container=styled.div`
display:flex;
justify-content:space-between;
padding:1.2rem 2rem;
border-bottom:1px solid #fff;
`
const Navside = () => {
  const {visible,setVisible,newPage,
    history,setHistory,
    setNewPage,prevPrompts,setPrevPrompts} =useContext(Context)
  return (
    <Container>
        <div style={{display:"flex",alignItems:"center",gap:"7px" }}>
        
        <img src={vqlogo} alt='logo' onClick={()=>setVisible(true)} style={{fontSize:"35px",cursor:"pointer",width:"50px",height:"50px"}}/>
        {/* <p style={{fontWeight:"600"}}>Verbique</p> */}
        </div>
        
        <MdOpenInNew  onClick={()=>{
          if(History){      
            setPrevPrompts([])
          }
          else{
            setHistory(true)
          }}} style={{fontSize:"35px",cursor:"pointer"}}/>
    </Container>
  )
}

export default Navside
