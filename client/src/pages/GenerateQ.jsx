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
  justify-content: end;
  margin-top:1rem;
  height:80vh;
  
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
const ResponseSection = styled.div`
  margin-top: 40px;
  padding: 20px;
  background-color: #111;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.4);
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
const TextArea = styled.textarea`
  background-color: #333;
  color: #fff;
  border: 1px solid #fff;
  padding: 10px;
  width: 80%;
  margin-top: 10px;
  resize: none;
  height: 80px;
  &:focus {
    outline: none;
    border-color: #00ff00;
  }
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
  background: linear-gradient(45deg, #004D4D, #009999);
  // background:#000;
  height:100vh; 
  font-family:Neue;
  
`;

const SubContainer = styled.div`
  display: flex;
  gap: 1.5rem;
  // background: linear-gradient(120deg, #1E3A5F, #2B4A77); 
  background: linear-gradient(45deg, #004D4D, #009999);
  // background: #000;
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
  border:1px solid #fff;
 
`;

const SecondContainer = styled.div`
  width: 50%;
  height: 85vh;
 
  border-radius: 12px;
  // background: linear-gradient(135deg, #3a5da8, #2a406c);
  // background: linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  padding: 1rem;
  border:1px solid #fff;
//   display: flex;
//   flex-direction: column;
  justify-content: center;
  align-items: end;
  color: #fff;
  font-size: 1.2rem;
    
`;

const Container3 = styled.div`
//   display: flex;
//   justify-content: center;
//   padding: 2rem;
  
  
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
const QuestionText = styled.p`
  font-size: 1.2rem;
  margin-bottom: 10px;
  animation: ${fadeIn} 0.5s ease-in-out;
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
const QuestionList = styled.ul`
  list-style-type: none;
  padding: 0;
  
  overflow:scroll;
  max-height:81vh;
  overflow-x: hidden;

  text-align: left;
  width: 100%;
`;

const QuestionItem = styled.li`
//   margin-bottom: 20px;
  padding: 20px;
  background-color: #000;
  border-radius: 10px;
//   box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
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
const Button = styled.button`
  background-color: #fff;
  color: #000;
  border: none;
  padding: 10px 20px;
  margin-top: 20px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background-color 0.3s ease;
  &:hover {
    background-color: #444;
    color: #fff;
  }
`;
const PDFViewer = styled.iframe`
  width: 100%;
  height: 100%;
  border: none;
`;

const TypingText = styled.div`
  color: #fff;
  font-size: 16px;
`;

const GenerateQ = () => {
    const [pdfFile, setPdfFile] = useState(null); 
    const [pdfUrl, setPdfUrl] = useState(null); 
    const [numDetailedQuestions, setNumDetailedQuestions] = useState(0);
    const [numSmallQuestions, setNumSmallQuestions] = useState(0);
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [response, setResponse] = useState('');  
  
    const [loading, setLoading] = useState(false)
    const handleFileChange = (event) => {
      setPdfFile(event.target.files[0]);
      const file = event.target.files[0];
      setPdfFile(file);
      if (file) {
        setPdfUrl(URL.createObjectURL(file)); // Create a URL for the PDF
      }
    };
  
    const handleGenerateQuestions = async () => {
      
      if (!pdfFile) {
        alert("Please upload a PDF file.");
        return;
      }
  
      const formData = new FormData();
      formData.append('pdf_file', pdfFile);
      formData.append('num_detailed_questions', numDetailedQuestions);
      formData.append('num_small_questions', numSmallQuestions);
      
      try {
        setLoading(true);
        const response = await axios.post('http://127.0.0.1:5000/generate_questions', formData);
        if (response.data.status === 'success') {
          setQuestions(response.data.questions);
          setLoading(false)
        } else {
          alert('Failed to generate questions');
        }
      } catch (error) {
        alert('Error generating questions: ' + error.message);
      }
    };
  
    const handleSubmitAnswer = async (questionNumber) => {
      const answer = answers[questionNumber];
      if (!answer) {
        alert("Please provide an answer before submitting.");
        return;
      }
  
      try {
        const response = await axios.post('http://127.0.0.1:5000/submit_answer', {
          question_number: questionNumber,
          answer: answer,
        });
        if (response.data.status === 'success') {
          setResponse(response.data.response);
        } else {
          alert('Failed to evaluate answer');
        }
      } catch (error) {
        alert('Error submitting answer:', error.message);
      }
    };
  
  return (
    <Container>
      <SubContainer>
        <FirstContainer>
        <Container2>
        {pdfUrl && (
          <PDFViewer src={pdfUrl} />
        )}
        
        
      {/* <Title>pdf Generator</Title> */}
      <div style={{display:"flex",justifyContent:"space-between",textAlign:"center",alignContent:"center",placeContent:"center"}}>
      {/* <Input
        style={{ width: "500px",border:"1px solid rgba(255, 255, 255, 0.2)"
  , color: "#fff" }}
        type="text"
        placeholder="Enter YouTube URL"
        value={youtubeUrl}
        onChange={(e) => setYoutubeUrl(e.target.value)}
      /> */}
      <Input style={{ width: "200px",border:"1px solid rgba(255, 255, 255, 0.2)"
  , color: "#fff" ,marginLeft:"-8px"}} type="file" accept=".pdf" onChange={handleFileChange} />
      {/* <Button2 onClick={handleTranslate} disabled={isLoading}> */}
        {/* {isLoading ? "Processing..." : "Translate GenerateQ"} */}
        {/* <CiSearch onClick={handleTranslate} style={{ display: "flex",cursor:"pointer", justifyContent: "center", alignItems: "center", width: "70px", height: "35px", marginLeft: "-1.5rem",marginTop:"2.3rem" }} /> */}
      {/* </Button2> */}
      <div >

      <Input
      style={{ width: "100px",border:"1px solid rgba(255, 255, 255, 0.2)"
        , color: "#fff" }} 
          type="number"
          value={numDetailedQuestions}
          onChange={(e) => setNumDetailedQuestions(e.target.value)}
        />
        <p className='-mt-[1rem] font-bold'>Detail</p>
      </div>
         <div>

        <Input
        style={{ width: "100px",border:"1px solid rgba(255, 255, 255, 0.2)"
            , color: "#fff" }} 
          type="number"
          value={numSmallQuestions}
          onChange={(e) => setNumSmallQuestions(e.target.value)}
        />
        <p className='-mt-[1rem] font-bold'>Small</p>
         </div>
       
      <button style={{ width: "200px",border:"1px solid rgba(255, 255, 255, 0.2)",height:"50px"
            , color: "#000",placeContent:"center",alignItems:"center",textAlign:"center",marginTop:"2.5rem" }} className="bg-white text-black text-xl font-bold rounded-3xl py-2" onClick={handleGenerateQuestions} >Generate Questions</button>

      </div>
      
        
    </Container2>

        </FirstContainer>
        <SecondContainer>
        {loading ? <>
                  <div className='flex flex-col items-center justify-end h-[40vh]'>
                  <l-bouncy    
                    size="45"
                    speed="1.75"
                    color="#fff"
                  ></l-bouncy>
                  <h1>Processing</h1>

                  </div>
      </>:<>
      {questions.length > 0 && (
        <div>
          {/* <h2>Generated Questions</h2> */}
          <QuestionList>
            {questions.map((q, index) => (
              <QuestionItem key={index}>
                <QuestionText>{q.number}. {q.question} ({q.marks} marks)</QuestionText>
                <TextArea
                  value={answers[q.number] || ''}
                  onChange={(e) => setAnswers({ ...answers, [q.number]: e.target.value })}
                  placeholder="Enter your answer here"
                />
                <Button onClick={() => handleSubmitAnswer(q.number)}>Submit Answer</Button>
              </QuestionItem>
            ))}
             <MessageContainer>
         {response && (
        <ResponseSection>
          <h2>Teacher's Feedback</h2>
          <p>{response}</p>
        </ResponseSection>
      )}
        </MessageContainer>
          </QuestionList>
          
        </div>
      )}</>}
        <Container3>
        {/* <ChatbotContainer> */}
        {/* <Title>Ask any Question</Title> */}
        
        {/* <form onSubmit={handleQuestionSubmit}> */}
          {/* <Input3
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask your question"
            required
          />
          <div style={{display:"flex",width:"100%",justifyContent:"center"}}><Button3 type="submit">Get Answer</Button3></div> */}
          {/* <Input
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
        </form> */}
      {/* </ChatbotContainer> */}
    </Container3>
       </SecondContainer>
    </SubContainer>
    </Container>
  );
}

export default GenerateQ;

// import React, { useState } from 'react';
// import axios from 'axios';
// import styled, { keyframes } from 'styled-components';
// import 'ldrs/bouncy';
// // Styled Components
// const Container = styled.div`
//   text-align: center;
//   background-color: #000;
//   color: #fff;
//   min-height: 100vh;
//   display: flex;
//   flex-direction: column;
//   align-items: center;
//   padding: 40px 20px;
// `;

// const Heading = styled.h1`
//   font-size: 2.5rem;
//   margin-bottom: 20px;
//   animation: fadeIn 1s ease-in-out;
// `;

// const Label = styled.label`
//   font-size: 1.2rem;
//   margin-bottom: 10px;
//   display: block;
// `;

// const Input = styled.input`
//   background-color: #333;
//   color: #fff;
//   border: 1px solid #fff;
//   padding: 10px;
//   margin-bottom: 20px;
//   width: 300px;
//   &:focus {
//     outline: none;
//     border-color: #00ff00;
//   }
// `;



// const Button = styled.button`
//   background-color: #fff;
//   color: #000;
//   border: none;
//   padding: 10px 20px;
//   margin-top: 20px;
//   cursor: pointer;
//   font-size: 1.2rem;
//   transition: background-color 0.3s ease;
//   &:hover {
//     background-color: #444;
//     color: #fff;
//   }
// `;





// const fadeIn = keyframes`
//   from {
//     opacity: 0;
//     transform: translateY(-20px);
//   }
//   to {
//     opacity: 1;
//     transform: translateY(0);
//   }
// `;



// function GenerateQ() {
//   const [pdfFile, setPdfFile] = useState(null); 
//   const [numDetailedQuestions, setNumDetailedQuestions] = useState(0);
//   const [numSmallQuestions, setNumSmallQuestions] = useState(0);
//   const [questions, setQuestions] = useState([]);
//   const [answers, setAnswers] = useState({});
//   const [response, setResponse] = useState('');  

//   const [loading, setLoading] = useState(false)
//   const handleFileChange = (event) => {
//     setPdfFile(event.target.files[0]);
//   };

//   const handleGenerateQuestions = async () => {
    
//     if (!pdfFile) {
//       alert("Please upload a PDF file.");
//       return;
//     }

//     const formData = new FormData();
//     formData.append('pdf_file', pdfFile);
//     formData.append('num_detailed_questions', numDetailedQuestions);
//     formData.append('num_small_questions', numSmallQuestions);
    
//     try {
//       setLoading(true);
//       const response = await axios.post('http://127.0.0.1:5000/generate_questions', formData);
//       if (response.data.status === 'success') {
//         setQuestions(response.data.questions);
//         setLoading(false)
//       } else {
//         alert('Failed to generate questions');
//       }
//     } catch (error) {
//       alert('Error generating questions: ' + error.message);
//     }
//   };

//   const handleSubmitAnswer = async (questionNumber) => {
//     const answer = answers[questionNumber];
//     if (!answer) {
//       alert("Please provide an answer before submitting.");
//       return;
//     }

//     try {
//       const response = await axios.post('http://127.0.0.1:5000/submit_answer', {
//         question_number: questionNumber,
//         answer: answer,
//       });
//       if (response.data.status === 'success') {
//         setResponse(response.data.response);
//       } else {
//         alert('Failed to evaluate answer');
//       }
//     } catch (error) {
//       alert('Error submitting answer:', error.message);
//     }
//   };

//   return (
//     <Container>
//       <Heading>PDF Question Generator</Heading>

//       <div>
//         <Label>Upload PDF File:</Label>
//         <Input type="file" accept=".pdf" onChange={handleFileChange} />
//       </div>

//       <div>
//         <Label>Number of Detailed Questions:</Label>
//         <Input
//           type="number"
//           value={numDetailedQuestions}
//           onChange={(e) => setNumDetailedQuestions(e.target.value)}
//         />
//       </div>

//       <div>
//         <Label>Number of Small Questions:</Label>
//         <Input
//           type="number"
//           value={numSmallQuestions}
//           onChange={(e) => setNumSmallQuestions(e.target.value)}
//         />
//       </div>

//       <Button onClick={handleGenerateQuestions} className='mb-[1rem]'>Generate Questions</Button>
//       {loading && (
//               <>
//                <l-bouncy
//                     size="45"
//                     speed="1.75"
//                     color="#fff"
//                   ></l-bouncy>
//               </>
//             )}
//       {questions.length > 0 && (
//         <div>
//           <h2>Generated Questions</h2>
//           <QuestionList>
//             {questions.map((q, index) => (
//               <QuestionItem key={index}>
//                 <QuestionText>{q.number}. {q.question} ({q.marks} marks)</QuestionText>
//                 <TextArea
//                   value={answers[q.number] || ''}
//                   onChange={(e) => setAnswers({ ...answers, [q.number]: e.target.value })}
//                   placeholder="Enter your answer here"
//                 />
//                 <Button onClick={() => handleSubmitAnswer(q.number)}>Submit Answer</Button>
//               </QuestionItem>
//             ))}
//           </QuestionList>
//         </div>
//       )}

//       {response && (
//         <ResponseSection>
//           <h2>Teacher's Feedback</h2>
//           <p>{response}</p>
//         </ResponseSection>
//       )}
//     </Container>
//   );


// export default GenerateQ;
