import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import styled,{ keyframes }  from 'styled-components';
import Sidebar from '../components/Sidebar.jsx';
import Navbar from '../components/Navbar';
import Input from '../ui/Input';
import { CiSearch } from "react-icons/ci";
import 'ldrs/bouncy';

const Container = styled.div`
    display: flex;
    height:100vh;
    font-family:Neue;
`;

const SubContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    // background:linear-gradient(45deg, #004D4D,#009999);
    background: #000;
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
//   background:linear-gradient(45deg, #004D4D,#009999);

    border:1px solid rgba(255, 255, 255, 0.2);
    border-radius: 30px;
  font-size: 17px;
  letter-spacing: 1px;
  
`;

const P2 = styled.p`
  padding: 1rem 1.5rem;
//   background:linear-gradient(45deg, #004D4D,#009999);
  
border:1px solid rgba(255, 255, 255, 0.2);
border-radius: 30px;
  font-size: 1.1rem;
  letter-spacing: 1px;
  
`;
const ButtonAnimation = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
`;
const Button = styled.button`
  background:linear-gradient(45deg, #004D4D,#009999);
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 16px;
  color: white;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s ease;
  
  box-shadow:0 0 1px 1px #fff;

  &:hover {
    background-color: #ff4d4d;
    animation: ${ButtonAnimation} 1s infinite;
  }

  &:disabled {
    background-color: #999;
    cursor: not-allowed;
  }
`;


function Summarization() {
    const [youtubeLink, setYoutubeLink] = useState('');
    const [messages, setMessages] = useState([]);
    const messagesEndRef = useRef(null);

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
        typeNextWord();
    };

    const handleSummarize = async () => {
        if (youtubeLink.trim()) {
            const newMessage = { text: youtubeLink, result: '', loading: true };
            setMessages([...messages, newMessage]);
            setYoutubeLink('');
    
            try {
                // Request to generate the summary
                const response = await axios.post('http://localhost:5000/summarize_youtube', { youtube_link: youtubeLink });
    
                // Fetch the summary file
                const res = await axios.get('http://localhost:5000/outputs/ytVideoSummarizer/youtube_summary.md');
                let summaryText = res.data;
    
                // Remove any occurrence of the word "undefined" from the summary text
                summaryText = summaryText.replace(/undefined/g, '');
    
                // Process the summary text
                let resultArray = summaryText.split("");
                let newArray = '';
                for (let i = 0; i < resultArray.length; i++) {
                    if (i === 0 || i % 2 !== 1) {
                        newArray += resultArray[i];
                    } else {
                        newArray += resultArray[i];
                    }
                }
                let newArray2 = newArray.split("*").join("<br/>");
                let newArray3 = newArray2.split("#").join("<br/>");
    
                // Update the last message with the processed summary using typing effect
                setMessages((prevMessages) => {
                    const updatedMessages = [...prevMessages];
                    updatedMessages[updatedMessages.length - 1] = {
                        ...updatedMessages[updatedMessages.length - 1],
                        loading: false,
                        result: '',
                    };
                    return updatedMessages;
                });
    
                // Trigger the typing effect
                typeWords(newArray3.split(' '));
            } catch (error) {
                console.error(error);
                setMessages((prevMessages) => {
                    const updatedMessages = [...prevMessages];
                    updatedMessages[updatedMessages.length - 1] = {
                        ...updatedMessages[updatedMessages.length - 1],
                        loading: false,
                        result: 'Error: ' + (error.response?.data?.message || error.message),
                    };
                    return updatedMessages;
                });
            }
        }
    };
    
    

    // Scroll to bottom when messages change
    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    return (
        <Container>
            
            <SubContainer>
                <Navbar />
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
                                <>
                                <MessageContainerLeft>
                                    <P2 dangerouslySetInnerHTML={{ __html: message.result }} />
                                    
                                </MessageContainerLeft>
                                {/* <Button> Narrate</Button> */}
                                </>
                            )}
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </SecondContainer>
                <div style={{ display: "flex", justifyContent: "center", width: "100%" }}>
                    <Input
                    className="text-xl"
                        required
                        placeholder={"Enter any YouTube Link"}
                        name="summarizer"
                        type="text"
                        value={youtubeLink}
                        onChange={(e) => { setYoutubeLink(e.target.value) }}
                    />
                    <button onClick={handleSummarize}>
                        <CiSearch style={{ width: "70px", height: "30px", marginLeft: "-5rem" }} />
                    </button>
                </div>
            </SubContainer>
        </Container>
    );
}

export default Summarization;

// import React, { useState, useEffect, useRef } from 'react';
// import axios from 'axios';
// import styled, { keyframes } from 'styled-components';
// import 'ldrs/bouncy'; // Ensure this library is installed or replace with your loading animation

// // Keyframe animations
// const ButtonAnimation = keyframes`
//   0% { transform: scale(1); }
//   50% { transform: scale(1.1); }
//   100% { transform: scale(1); }
// `;

// const fadeIn = keyframes`
//   from {
//     opacity: 0;
//   }
//   to {
//     opacity: 1;
//   }
// `;

// // Styled components
// const Container = styled.div`
//   display: flex;
//   justify-content: center;
//   padding: 2rem;
//   background: #f0f2f5;
//   min-height: 100vh;
// `;

// const ChatbotContainer = styled.div`
//   display: flex;
//   flex-direction: column;
//   width: 100%;
//   max-width: 600px;
//   background: linear-gradient(135deg, #3a5da8, #2a406c);
//   border-radius: 20px;
//   box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
//   padding: 2rem;
//   animation: ${fadeIn} 0.8s ease-in-out;
//   color: #fff;
// `;

// const MessageContainer = styled.div`
//   display: flex;
//   flex-direction: column;
//   height: 400px;
//   overflow-y: auto;
//   padding: 1rem;
//   background: rgba(255, 255, 255, 0.1);
//   border-radius: 10px;
//   margin-bottom: 1rem;
// `;

// const MessageBoxRight = styled.div`
//   display: flex;
//   justify-content: flex-end;
//   margin-bottom: 1rem;
// `;

// const MessageBoxLeft = styled.div`
//   display: flex;
//   justify-content: flex-start;
//   margin-bottom: 1rem;
// `;

// const UserMessage = styled.p`
//   padding: 1rem 1.5rem;
//   background: linear-gradient(135deg, #6fb1fc, #3a5da8);
//   border-radius: 30px;
//   font-size: 17px;
//   letter-spacing: 1px;
//   box-shadow: 0 0 4px 1px #fff;
//   color: #fff;
//   max-width: 80%;
// `;

// const BotMessage = styled.p`
//   padding: 1rem 1.5rem;
//   background: linear-gradient(135deg, #3a5da8, #2a406c);
//   border-radius: 30px;
//   font-size: 17px;
//   letter-spacing: 1px;
//   box-shadow: 0 0 4px 1px #fff;
//   color: #fff;
//   max-width: 80%;
// `;

// const Button = styled.button`
//   background: linear-gradient(135deg, #3a5da8, #2a406c);
//   border: none;
//   padding: 12px 24px;
//   border-radius: 10px;
//   font-size: 16px;
//   color: white;
//   cursor: pointer;
//   transition: background-color 0.3s ease;
//   box-shadow: 0 0 1px 1px #fff;

//   &:hover {
//     background-color: #ff4d4d;
//     animation: ${ButtonAnimation} 1s infinite;
//   }

//   &:disabled {
//     background-color: #999;
//     cursor: not-allowed;
//   }
// `;

// const Input = styled.input`
//   width: 100%;
//   padding: 12px;
//   margin-top: 1rem;
//   border-radius: 10px;
//   border: none;
//   font-size: 16px;
//   color: #333;
//   outline: none;
// `;

// const AnswerBox = styled.div`
//   padding: 1rem 1.5rem;
//   background-color: #e6f7ff;
//   border-radius: 8px;
//   box-shadow: 0 0 4px 1px #fff;
//   animation: ${fadeIn} 0.5s ease-in;
//   margin-top: 10px;
//   color: #333;
// `;

// const TypingText = styled.div`
//   color: #fff;
//   font-size: 16px;
// `;

// function Chatbot() {
//   const [question, setQuestion] = useState('');
//   const [messages, setMessages] = useState([]);
//   const messagesEndRef = useRef(null);

//   // Function to handle typing effect
//   const typeWords = (words) => {
//     let currentWordIndex = 0;
//     const typeNextWord = () => {
//       if (currentWordIndex < words.length) {
//         const word = words[currentWordIndex];
//         if (word) { // Ensure word is not undefined or null
//           setMessages((prevMessages) => {
//             const updatedMessages = [...prevMessages];
//             const lastMessage = updatedMessages[updatedMessages.length - 1];
//             const currentResult = lastMessage.result || '';
//             updatedMessages[updatedMessages.length - 1] = {
//               ...lastMessage,
//               result: currentResult + word + ' ',
//             };
//             return updatedMessages;
//           });
//         }
//         currentWordIndex++;
//         setTimeout(typeNextWord, 70);
//       }
//     };
//     typeNextWord();
//   };

//   // Function to handle form submission
//   const handleQuestionSubmit = async (e) => {
//     e.preventDefault();
//     if (!question.trim()) return;

//     // Add user's question to messages
//     const newMessage = { text: question, result: '', loading: true };
//     setMessages((prevMessages) => [...prevMessages, newMessage]);
//     setQuestion('');

//     try {
//       // Send question to backend
//       const response = await axios.post('http://localhost:5000/answer', { question });

//       let answerText = response.data.answer;

//       // Validate the response
//       if (typeof answerText !== 'string') {
//         answerText = 'I\'m sorry, I couldn\'t find an answer to your question.';
//       }

//       // Split the answer into words and filter out invalid entries
//       const words = answerText.split(' ').filter(word => word && typeof word === 'string');

//       // Update the last message to remove loading state
//       setMessages((prevMessages) => {
//         const updatedMessages = [...prevMessages];
//         const lastIndex = updatedMessages.length - 1;
//         updatedMessages[lastIndex] = { ...updatedMessages[lastIndex], loading: false, result: '' };
//         return updatedMessages;
//       });

//       // Start typing animation
//       typeWords(words);
//     } catch (error) {
//       console.error('Error getting answer from chatbot:', error);
//       // Update the last message with error state
//       setMessages((prevMessages) => {
//         const updatedMessages = [...prevMessages];
//         const lastIndex = updatedMessages.length - 1;
//         updatedMessages[lastIndex] = { 
//           ...updatedMessages[lastIndex], 
//           loading: false, 
//           result: 'Error: Could not fetch answer. Please try again later.' 
//         };
//         return updatedMessages;
//       });
//     }
//   };

//   // Scroll to the bottom when messages change
//   useEffect(() => {
//     if (messagesEndRef.current) {
//       messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
//     }
//   }, [messages]);

//   return (
//     <Container>
//       <ChatbotContainer>
//         <h2 style={{ textAlign: 'center', marginBottom: '1rem' }}>Ask a Question</h2>
//         <MessageContainer>
//           {messages.map((message, index) => (
//             <div key={index}>
//               {/* User Message */}
//               {message.text && (
//                 <MessageBoxRight>
//                   <UserMessage>{message.text}</UserMessage>
//                 </MessageBoxRight>
//               )}
//               {/* Loading Animation */}
//               {message.loading && (
//                 <MessageBoxLeft>
//                   <l-bouncy size="45" speed="1.75" color="#fff"></l-bouncy>
//                 </MessageBoxLeft>
//               )}
//               {/* Bot Response */}
//               {!message.loading && message.result && (
//                 <MessageBoxLeft>
//                   <BotMessage>{message.result}</BotMessage>
//                 </MessageBoxLeft>
//               )}
//             </div>
//           ))}
//           <div ref={messagesEndRef} />
//         </MessageContainer>
//         <form onSubmit={handleQuestionSubmit}>
//           <Input
//             type="text"
//             value={question}
//             onChange={(e) => setQuestion(e.target.value)}
//             placeholder="Ask your question"
//             required
//           />
//           <Button type="submit">Get Answer</Button>
//         </form>
//       </ChatbotContainer>
//     </Container>
//   );
// }

// export default Chatbot;

