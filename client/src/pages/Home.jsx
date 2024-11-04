import React, { useContext, useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import Sidebar from '../components/Sidebar.jsx';
import Navbar from '../components/Navbar.jsx';
import { TbSettingsAutomation } from "react-icons/tb";
import { MdSummarize } from "react-icons/md";
import { MdPlagiarism } from "react-icons/md";
import { CiSearch } from "react-icons/ci";
import vqlogo from '../assets/vq.png'
import { useNavigate } from 'react-router-dom';
import { Context } from '../context/Context.jsx';
import { MdHistoryToggleOff } from "react-icons/md";
import 'ldrs/bouncy';
import { FaYoutube } from "react-icons/fa";
import { LuListTodo } from "react-icons/lu";
import Input from '../ui/Input.jsx';
import { SiGreatlearning } from "react-icons/si";
const Container = styled.div`
  display: flex;
  
  // background: linear-gradient(120deg, #1E3A5F, #2B4A77); 
  // background: linear-gradient(135deg, #3a5da8, #2a406c);
  // background: linear-gradient(45deg, #004D4D, #009999);
  background: #000;
  font-family:Neue;
  height:100vh;

`;

const SubContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
`;

// const ContentContainer = styled.div`
//   display: flex;
//   flex-direction: column;
//   padding: 1rem;
//   height: 30vh;
//   margin: 0 2rem;
//   width: 30%;
//   border-radius: 10px;
//   cursor: pointer;
//   color: #242424;
//   // background: linear-gradient(to right, #a2c2e1, #d0e6f5);
//   background: linear-gradient(135deg, #a8e6ff, #84b6f4, #3b5998);



//   // box-shadow: 0 0 5px 5px #171717;
//   transition: 0.3s linear;
//   &:hover {
//     // box-shadow: 0 0 5px 5px #676767;
//   }
//   &:active {
//     transform: scale(0.9);
//   }
// `;
const ContentContainer = styled.div`
  display: flex;
  flex-direction: column;
  padding: 1rem;
  height: 30vh;
  margin: 0 2rem;
  width: 30%;
  border-radius: 10px;
  cursor: pointer;
  color: #fff;
  

    //  background: linear-gradient(45deg, #004D4D, #009999);
 /* Semi-transparent for glass effect */
  backdrop-filter: blur(10px); /* Frosted glass effect */
  border: 1px solid rgba(255, 255, 255, 0.2); /* Light border for the glass effect */
  
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); /* Soft shadow */
  -webkit-backdrop-filter: blur(10px); /* Safari support */

  transition: 0.3s linear;

  &:hover {
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2); /* Enhance shadow on hover */
  }

  &:active {
    transform: scale(0.9); /* Slightly reduce size on click */
  }
`;

const FlexContainer = styled.div`
  display: flex;
  justify-content:space-evenly;
`;


const FlexContainerSub = styled.div`
  display: flex;
  flex-direction: column;
  margin-top:-1rem;
`;

const SecondContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 500px;
  overflow-y: auto;
  max-height: 500px;
  padding: 2rem;
`;

const MessageContainerRight = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  width: 100%;
  align-self: flex-end;
  
`;

const MessageContainerLeft = styled.div`
  display: flex;
  justify-content: flex-start;
  margin-bottom: 1rem;
  max-width: 820px;
  align-self: flex-start;
`;

const P = styled.p`
  padding: 1rem 1.5rem;
  // background: linear-gradient(135deg, #3a5da8, #2a406c);
  background:#000;
  border-radius: 30px;
  font-size: 1.2rem;
  border:1px solid rgba(255, 255, 255, 0.2);
  letter-spacing: 1px;
`;

const P2 = styled.p`
  padding: 1rem 1.5rem;
  // background: linear-gradient(135deg, #3a5da8, #2a406c);
  border-radius: 30px;
  background:#000;
  font-size: 1.2rem;
  letter-spacing: 1px;
  border:1px solid rgba(255, 255, 255, 0.2);
`;
const Button = styled.button`
  width: 20%;
  height: 50px;
  padding: 10px;
  // margin: 2rem 0 0.5rem 0;
  border-radius: 29px;
  // background:linear-gradient(135deg, #a8e6ff, #84b6f4, #3b5998);
  color: #fff;
  font-weight: bolder;
  font-size: 17px;
  transition: all 0.4s ease;
  backdrop-filter: blur(10px); /* Frosted glass effect */
  border: 1px solid rgba(255, 255, 255, 0.2); /* Light border for the glass effect */
  
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); /* Soft shadow */
  -webkit-backdrop-filter: blur(10px); /* Safari support */

  transition: 0.3s linear;

  &:hover {
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2); /* Enhance shadow on hover */
  }

  &:active {
    transform: scale(0.9); /* Slightly reduce size on click */
  }
`;


export const Content = ({ style,name, content, icon }) => {
  const navigate = useNavigate();
  return (
    <ContentContainer  style={{style}} onClick={() => navigate(`/${name}`)}>
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: "10px" }}>
        <p style={{ fontSize: "40px", display: "flex", justifyContent: "center" }}>{icon}</p>
        <p style={{ textAlign: "center", fontSize: "22px", fontWeight: "600" }}>
          {name}
        </p>
      </div>
      <p style={{ margin: "2rem 0" ,fontSize:"1.1rem"}}>
        {content}
      </p>
    </ContentContainer>
  );
};

const Home = () => {
  const { messages, setMessages, visible, setVisible, generate, prevPrompts, setPrevPrompts, input, setInput } = useContext(Context);
  
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();
  const handleVisibility = async () => {
    if (input.trim()) {
      setVisible(false);
      const newMessage = { text: input, result: '', loading: true };
      setMessages([...messages, newMessage]);
      setInput('');
      setPrevPrompts(prev => [...prev, input]);
      // Generate result
      const result = await generate(input);

      let resultArray = result.split("");
      let newArray = '';
      for (let i = 0; i < resultArray.length; i++) {
        if (i === 0 || i % 2 !== 1) {
          newArray += resultArray[i];
        } else {
          newArray += resultArray[i];
        }
      }
      let newArray2 = newArray.split("*").join("<br/>");
      let newArray3 = newArray2.split("undefined").join("<br/>");

      // Initialize the typing effect
      const newResponseArray = newArray3.split(" ");
      typeWords(newResponseArray);

      // Update the last message with the result and stop loading
      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        updatedMessages[updatedMessages.length - 1] = {
          ...updatedMessages[updatedMessages.length - 1],
          loading: false,
        };
        return updatedMessages;
      });
    }
  };

  const typeWords = (words) => {
    let currentWordIndex = 0;
    const typeNextWord = () => {
      if (currentWordIndex < words.length) {
        setMessages((prevMessages) => {
          const updatedMessages = [...prevMessages];
          const currentResult = updatedMessages[updatedMessages.length - 1].result || '';
          const nextWord = words[currentWordIndex] + ' ';
          updatedMessages[updatedMessages.length - 1] = {
            ...updatedMessages[updatedMessages.length - 1],
            result: currentResult + nextWord,
          };
          return updatedMessages;
        });
        currentWordIndex++;
        setTimeout(typeNextWord, 70);
      }
    };
    // Start with the first word
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages];
      updatedMessages[updatedMessages.length - 1] = {
        ...updatedMessages[updatedMessages.length - 1],
        result: words.length > 0 ? words[0] + ' ' : '', // Ensure we start with the first word
      };
      return updatedMessages;
    });
    typeNextWord();
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleChange = (e) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleVisibility();
    }
  };

  return (
    <Container>
      {/* <Sidebar /> */}
      <SubContainer>
        <Navbar />
        {visible ? (<>
        
          <FlexContainerSub>
            {/* <div style={{ display: "flex", justifyContent: "center", margin:"-4rem 0 2rem 0", fontSize: "60px" }}>
              <img src={vqlogo} alt='logo'/>
            </div> */}
            <FlexContainer >
              <Content
                icon={<TbSettingsAutomation />}
                content="The virtual whiteboard enhances collaboration by allowing users to draw, annotate, and share ideas in real time."
                name="Automation"
              />
              <Content
                icon={<FaYoutube/>}
                content="Quickly summarize videos using AI tools, condensing key points to help you save time and focus on what matters the most."
                name="Youtube Summarizer"
              />
               <Content
                icon={<MdPlagiarism />}
                content="The YouTube live relay translator provides real-time translations and answers viewer questions, enhancing accessibility and engagement."
                name='Translator'
              />
             
            </FlexContainer>
            <FlexContainer style={{marginTop:"2rem"}}>
            {/* <Content
              content="Stay organized and on track with this dynamic, animated to-do list tailored. "
              icon={<LuListTodo />}
              name="ToDoList"/> 
            <Content
            icon={<SiGreatlearning/>}
            content="The learning section offers interactive modules, resources, and assessments to enhance understanding and foster skill development. "
            name="Learning"/>  */}
            </FlexContainer>
          </FlexContainerSub>
          {/* <div  style={{display:"flex",justifyContent:"center",width:"100%",marginTop:"1rem"}}>
            <Button onClick={()=>{
              navigate('/Email')}
              }>Take a Test</Button>
          </div> */}
          
          </>
        ) : (
          <SecondContainer>
            {messages.map((message, index) => (
              <div key={index}>
                {message.text && (
                  <MessageContainerRight>
                    <P>{message.text}</P>
                  </MessageContainerRight>
                )}
                {message.loading && (
                  <l-bouncy
                    size="45"
                    speed="1.75"
                    color="#fff"
                  ></l-bouncy>
                )}
                {!message.loading && message.result && (
                  <MessageContainerLeft>
                    <P2 dangerouslySetInnerHTML={{ __html: message.result }} />
                  </MessageContainerLeft>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </SecondContainer>
        )}
        <div style={{ display: "flex", justifyContent: "center"}}>
          <Input
        
          // disabled={!input.trim()} // Disable button when input is empty or whitespace
           className="text-xl"  
          required
            type='text'
            placeholder='Message Verbiqube'
            name='textbox'
            value={input}
            onChange={handleChange}
            onKeyPress={handleKeyPress} // Align input field to the right
          />
          <button onClick={handleVisibility}>
            <CiSearch style={{ width: "70px", height: "30px", marginLeft: "-5rem" }} />
          </button>
        </div>
      </SubContainer>
    </Container>
  );
};

export default Home;