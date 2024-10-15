import React, { useContext } from 'react'
import Navside from '../ui/Navside'
import FooterSide from '../ui/FooterSide'
import styled from 'styled-components'
import { Context } from '../context/Context.jsx'
import { MdHistoryToggleOff } from "react-icons/md";
const Container=styled.div`
display:flex;
flex-direction:column;
height:100vh;
min-width:320px;
max-width:320px;
// background:linear-gradient(120deg, #1E3A5F); 
background:#242424;
border-right:1px solid #fff;
text-align:center;
color:#fff;

`
const SubContainer=styled.div`
height:80vh;
max-height:79.5vh;
overflow-y:auto;
margin:0 0 1rem 0;
`
const P=styled.p`
display:flex;
justify-content:start;
align-items:center;
width:100%;
margin:0.5rem 0.5rem 0.5rem 0.5rem;
padding:10px ;
color:#fff;
font-weight:200;
font-size:17px;
border-radius:5px;
cursor:pointer;
transition:0.1s ;
&:hover{
background:#424242;
}
`
const Sidebar = () => {
  const {prevPrompts,history,setMessages,messages,setInput}=useContext(Context);
  return (
    <Container>
        <Navside/>
        <SubContainer>
          {history && (
            <>
            <div>
          {prevPrompts.map((prompts)=>{
            return(<>
            <div style={{display:"flex",justifyContent:"start",alignItems:"center"}}>
              <MdHistoryToggleOff style={{fontSize:"23px",margin:"0 0 0 10px"}} />
                <P onClick={()=>{
                  const newMessage = { text: prompts, result: '', loading: true };
                  setMessages([...messages, newMessage]);
                }}>
                {prompts}
                </P>
            </div>
            
            </>
              
            )
            
          })}
        </div>
            </>
          )}
          
        </SubContainer>
        <FooterSide/>
    </Container>
  )
}

export default Sidebar
