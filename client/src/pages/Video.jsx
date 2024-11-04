import React, { useState, useEffect,useRef } from 'react';
import styled,{keyframes} from 'styled-components';
import axios from 'axios';
import Input from '../ui/Input';
import { CiSearch } from "react-icons/ci";

import ReactPlayer from "react-player";
import 'ldrs/bouncy';
const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

const ButtonAnimation = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
`;

const Container2 = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top:1rem;
  
  animation: ${fadeIn} 1s ease-in-out;
  color: white;
`;
const Dropdown = styled.select`
  margin-top:2rem;
  margin-right:1rem;
  // background:linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  border:1px solid rgba(255, 255, 255, 0.2);
  border-radius:10px; 
  height:50px;
  color:white;
`;
const Input2 = styled.input`
  color: black;
  padding: 10px;
  border: none;
  border-radius: 8px;
  width: 300px;
  font-size: 16px;
  margin: 20px 0;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  &:focus {
    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
  }
`;

const Button2 = styled.button`
  // background: linear-gradient(135deg, #3a5da8, #2a406c); 
  background: linear-gradient(45deg, #004D4D, #009999);

  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 16px;
  color: white;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s ease;
  
  box-shadow:0 0 2px 2px #fff;

  &:hover {
    background-color: #ff4d4d;
    animation: ${ButtonAnimation} 1s infinite;
  }

  &:disabled {
    background-color: #999;
    cursor: not-allowed;
  }
`;

const PlayerContainer = styled.div`
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 80%;
  margin-top: 40px;

  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const VideoWrapper = styled.div`
  // width: 30%;
  // height:30%;
  
  animation: ${fadeIn} 1.5s ease-in-out;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.05);
  }

  @media (max-width: 768px) {
    width: 90%;
  }
`;

const AudioWrapper = styled.div`  
  display:none;
  width: 45%;
  animation: ${fadeIn} 1.5s ease-in-out;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.05);
  }

  @media (max-width: 768px) {
    width: 90%;
    margin-top: 20px;
  }
`;

const Title = styled.h1`
  font-size: 30px;
  font-weight: bold;
  text-align: center;
  // margin-bottom: 30px;
  animation: ${fadeIn} 1s ease-in-out;

`;

const SubTitle = styled.h2`
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
  animation: ${fadeIn} 1.2s ease-in-out;
`;

const Container = styled.div`
  padding: 3rem 2rem 0 2rem;
  // background: linear-gradient(120deg, #1E3A5F, #2B4A77);
  // background: linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  height:100vh; 
  font-family:Neue;
`;

const SubContainer = styled.div`
  display: flex;
  gap: 1.5rem;
  // background: linear-gradient(120deg, #1E3A5F, #2B4A77); 
  // background: linear-gradient(45deg, #004D4D, #009999);
  background: #000;
`;

const FirstContainer = styled.div`
  display: flex;
  width: 50%;
  height: 85vh;
  border-radius: 12px;
//  background: linear-gradient(135deg, #3a5da8, #2a406c);
  // background: linear-gradient(45deg, #004D4D, #009999);
  background: #000;
  padding: 0rem;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  border:1px solid rgba(255, 255, 255, 0.2);
 
`;

const SecondContainer = styled.div`
  width: 50%;
  height: 85vh;
 
  border-radius: 12px;
  // background: linear-gradient(135deg, #3a5da8, #2a406c);
  // background: linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  padding: 1rem;
  border:1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 1.2rem;
`;

const Container3 = styled.div`
  display: flex;
  justify-content: center;
  padding: 2rem;
  
  
`;

const ChatbotContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 600px;
  border:none;
  border-radius: 20px;
  
  padding: 2rem;
  animation: ${fadeIn} 0.8s ease-in-out;
  color: #fff;
`;

const MessageContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 400px;
  overflow-y: auto;
  
  border-radius: 10px;
  margin-bottom: 1rem;
`;

const MessageBoxRight = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
  margin-bottom: 1rem;
`;

const MessageBoxLeft = styled.div`
  display: flex;
  justify-content: flex-start;
  margin-bottom: 1rem;
`;

const UserMessage = styled.p`
  padding: 1rem 1.5rem;
  // background:linear-gradient(135deg, #3a5da8, #2a406c);
  // background: linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  border-radius: 30px;
  font-size: 17px;
  letter-spacing: 1px;
  border:1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  max-width: 80%;
  margin-top:5px;
  margin-right:5px;
`;

const BotMessage = styled.p`
  padding: 1rem 1.5rem;
  // background: linear-gradient(135deg, #3a5da8, #2a406c);
  // background: linear-gradient(45deg, #004D4D, #009999);
  border-radius: 30px;
  font-size: 17px;
  letter-spacing: 1px;
  border:1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  max-width: 80%;
  margin-left:5px;
`;

const Button3 = styled.button`
  background: linear-gradient(135deg, #3a5da8, #2a406c);
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 16px;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
  box-shadow: 0 0 1px 1px #fff;

  &:hover {
    background-color: #ff4d4d;
    animation: ${ButtonAnimation} 1s infinite;
  }

  &:disabled {
    background-color: #999;
    cursor: not-allowed;
  }
`;

const Input3 = styled.input`
  width: 100%;
  padding: 12px;
  margin-top: 1rem;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  color: #333;
  outline: none;
`;

const AnswerBox = styled.div`
  padding: 1rem 1.5rem;
  background-color: #e6f7ff;
  border-radius: 8px;
  box-shadow: 0 0 4px 1px #fff;
  animation: ${fadeIn} 0.5s ease-in;
  margin-top: 10px;
  color: #333;
`;

const TypingText = styled.div`
  color: #fff;
  font-size: 16px;
`;

const Video = () => {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [summaryType, setSummaryType] = useState('English'); // Added for dropdown
  const [isLoading, setIsLoading] = useState(false);
  const playerRef = useRef(null);
  const audioRef = useRef(null);
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading,setLoading]= useState(false);
  const messagesEndRef = useRef(null);


  // Function to handle typing effect
  const typeWords = (words) => {
    let currentWordIndex = 0;
    const typeNextWord = () => {
      if (currentWordIndex < words.length) {
        const word = words[currentWordIndex];
        if (word) { // Ensure word is not undefined or null
          setMessages((prevMessages) => {
            const updatedMessages = [...prevMessages];
            const lastMessage = updatedMessages[updatedMessages.length - 1];
            const currentResult = lastMessage.result || '';
            updatedMessages[updatedMessages.length - 1] = {
              ...lastMessage,
              result: currentResult + word + ' ',
            };
            return updatedMessages;
          });
        }
        currentWordIndex++;
        setTimeout(typeNextWord, 70);
      }
    };
    typeNextWord();
  };

  // Function to handle form submission
  const handleQuestionSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    // Add user's question to messages
    const newMessage = { text: question, result: '', loading: true };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setQuestion('');

    try {
      // Send question to backend
      const response = await axios.post('http://localhost:5000/answer', { question });

      let answerText = response.data.answer;

      // Validate the response
      if (typeof answerText !== 'string') {
        answerText = 'I\'m sorry, I couldn\'t find an answer to your question.';
      }

      // Split the answer into words and filter out invalid entries
      const words = answerText.split(' ').filter(word => word && typeof word === 'string');

      // Update the last message to remove loading state
      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        const lastIndex = updatedMessages.length - 1;
        updatedMessages[lastIndex] = { ...updatedMessages[lastIndex], loading: false, result: '' };
        return updatedMessages;
      });

      // Start typing animation
      typeWords(words);
    } catch (error) {
      console.error('Error getting answer from chatbot:', error);
      // Update the last message with error state
      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        const lastIndex = updatedMessages.length - 1;
        updatedMessages[lastIndex] = { 
          ...updatedMessages[lastIndex], 
          loading: false, 
          result: 'Error: Could not fetch answer. Please try again later.' 
        };
        return updatedMessages;
      });
    }
  };

  // Scroll to the bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleTranslate = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/process", {
        youtube_url: youtubeUrl,
      });
      setAudioUrl(response.data.audio_url);
      setIsLoading(false);
    } catch (error) {
      console.error("Error processing the video:", error);
      setIsLoading(false);
    }
  };

  const syncAudioWithVideo = () => {
    if (audioRef.current && playerRef.current) {
      audioRef.current.currentTime = playerRef.current.getCurrentTime();
    }
  };

  const handlePlay = () => {
    if (audioRef.current) {
      audioRef.current.volume = 1.0;
      audioRef.current.play();
    }
  };

  const handlePause = () => {
    if (audioRef.current) {
      audioRef.current.pause();
    }
  };

  useEffect(() => {
    if (audioRef.current && playerRef.current) {
      audioRef.current.addEventListener("timeupdate", syncAudioWithVideo);
    }

    return () => {
      if (audioRef.current) {
        audioRef.current.removeEventListener("timeupdate", syncAudioWithVideo);
      }
    };
  }, []);
  return (
    <Container>
      <SubContainer>
        <FirstContainer>
        <Container2>
      <Title>YouTube Translator</Title>
      <div style={{display:"flex"}}>
      <Input
        style={{ width: "500px",border:"1px solid rgba(255, 255, 255, 0.2)"
  , color: "#fff" }}
        type="text"
        placeholder="Enter YouTube URL"
        value={youtubeUrl}
        onChange={(e) => setYoutubeUrl(e.target.value)}
      />
      {/* <Button2 onClick={handleTranslate} disabled={isLoading}> */}
        {/* {isLoading ? "Processing..." : "Translate Video"} */}
        <CiSearch onClick={handleTranslate} style={{ display: "flex",cursor:"pointer", justifyContent: "center", alignItems: "center", width: "70px", height: "35px", marginLeft: "-1.5rem",marginTop:"2.3rem" }} />
      {/* </Button2> */}
      <Dropdown
      style={{padding:"0 1rem"}}
              value={summaryType}
              onChange={(e) => setSummaryType(e.target.value)} // Added dropdown handling
            >
              <option style={{background:"linear-gradient(45deg, #004D4D, #009999)",color:"black"}} value="English">English</option>
              <option style={{color:"black"}} value="Tamil">Tamil</option>
              <option value="Hindi" style={{color:"black"}}>Hindi</option>
      </Dropdown>
      </div>
      {isLoading ? <>
                  <l-bouncy
        
                    size="45"
                    speed="1.75"
                    color="#fff"
                  ></l-bouncy>
                  <h1>Processing</h1>
      </>:<>
      {youtubeUrl && audioUrl && (
        <PlayerContainer>
          <VideoWrapper>
            {/* <SubTitle>Original Video</SubTitle> */}
            <ReactPlayer
            style={{maxWidth:"80%",maxHeight:"40%",marginTop:"-1.5rem"}}
              url={youtubeUrl}
              controls
              ref={playerRef}
              onPlay={handlePlay}
              onPause={handlePause}
              onSeek={(seconds) => (audioRef.current.currentTime = seconds)}
            />
          </VideoWrapper>
          <AudioWrapper>
            <SubTitle>Translated Audio</SubTitle>
            <audio controls ref={audioRef} src={`http://localhost:5000${audioUrl}`} />
          </AudioWrapper>
        </PlayerContainer>
      )}</>}
    </Container2>
        </FirstContainer>
        <SecondContainer>
        <Container3>
        <ChatbotContainer>
        <Title>Ask any Question</Title>
         <MessageContainer>
           {messages.map((message, index) => (
            <div key={index}>
              {/* User Message */}
              {message.text && (
                <MessageBoxRight>
                  <UserMessage>{message.text}</UserMessage>
                </MessageBoxRight>
              )}
              {/* Loading Animation */}
              {message.loading && (
                <MessageBoxLeft>
                  <l-bouncy size="45" speed="1.75" color="#fff"></l-bouncy>
                </MessageBoxLeft>
              )}
              {/* Bot Response */}
              {!message.loading && message.result && (
                <MessageBoxLeft>
                  <BotMessage>{message.result}</BotMessage>
                </MessageBoxLeft>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </MessageContainer>
        <form onSubmit={handleQuestionSubmit}>
          {/* <Input3
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask your question"
            required
          />
          <div style={{display:"flex",width:"100%",justifyContent:"center"}}><Button3 type="submit">Get Answer</Button3></div> */}
          <Input
                style={{ width: "500px",border:"1px solid rgba(255, 255, 255, 0.2)"
                  , color: "#fff" }}
                placeholder="Ask Anything"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                type="text"
              />
              
            <button type="submit">
              <CiSearch style={{ display: "flex", justifyContent: "center", alignItems: "center", width: "70px", height: "35px", marginLeft: "-5rem" ,marginBottom:"-0.6rem"}} />
            </button>
        </form>
      </ChatbotContainer>
    </Container3>
       </SecondContainer>
    </SubContainer>
    </Container>
  );
}

export default Video;