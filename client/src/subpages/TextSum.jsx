// import React, { useState } from 'react';
// import axios from 'axios';
// import styled from 'styled-components';

// const Container = styled.div`
//   display: flex;
//   flex-direction: column;
//   align-items: center;
//   padding: 20px;
//   font-family: Arial, sans-serif;
// `;

// const Title = styled.h1`
//   font-size: 24px;
//   color: #fff;
//   margin-bottom: 20px;
// `;

// const Form = styled.form`
//   display: flex;
//   flex-direction: column;
//   align-items: center;
//   width: 100%;
// `;

// const TextArea = styled.textarea`
//   width: 60%;
//   height: 150px;
//   padding: 10px;
//   border-radius: 5px;
//   border: 1px solid #ccc;
//   font-size: 16px;
//   margin-bottom: 20px;
//   resize: none;
//   color:black;
// `;

// const Button = styled.button`
//   padding: 10px 20px;
//   font-size: 16px;
//   background-color: #4CAF50;
//   color: white;
//   border: none;
//   border-radius: 5px;
//   cursor: pointer;

//   &:hover {
//     background-color: #45a049;
//   }
// `;

// const SummaryContainer = styled.div`
//   margin-top: 20px;
//   width: 60%;
//   background-color: #f9f9f9;
//   padding: 20px;
//   border-radius: 5px;
//   box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
// `;

// const SummaryTitle = styled.h2`
//   font-size: 20px;
//   color: #333;
//   margin-bottom: 10px;
// `;

// const SummaryText = styled.p`
//   font-size: 16px;
//   color: #666;
// `;

// function TextSum() {
//   const [text, setText] = useState('');
//   const [summary, setSummary] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await axios.post('http://127.0.0.1:5000/summarize_text', { text });
//       setSummary(response.data.summary);
//     } catch (error) {
//       console.error('Error generating summary:', error);
//     }
//   };

//   return (
//     <Container>
//       <Title>Text Summarization</Title>
//       <Form onSubmit={handleSubmit}>
//         <TextArea
//           name="text"
//           placeholder="Enter text to summarize..."
//           value={text}
//           onChange={(e) => setText(e.target.value)}
//         ></TextArea>
//         <Button type="submit">Generate Summary</Button>
//       </Form>

//       {summary && (
//         <SummaryContainer>
//           <SummaryTitle>Summary:</SummaryTitle>
//           <SummaryText>{summary}</SummaryText>
//         </SummaryContainer>
//       )}
//     </Container>
//   );
// }

// export default TextSum;
import React, { useState } from 'react';
import { FaUpload, FaTimes } from 'react-icons/fa'; // Import FaTimes for close icon
import '@react-pdf-viewer/core/lib/styles/index.css';
import styled from 'styled-components';

const P = styled.p`
    background: white;
    color: black;
    border: 1px solid #fff;
    border-bottom: 3px solid #333;
    padding: 1rem;
    margin: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

const CloseButton = styled.button`
    background: none;
    border: none;
    color: red;
    cursor: pointer;
    font-size: 16px;
    margin-left: 10px;
`;

const FileInfo = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px 0;
    font-size: 16px;
`;

const PDFUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [pdfUrl, setPdfUrl] = useState('');
    const [inputText, setInputText] = useState(''); // To store the input text
    const [displayTexts, setDisplayTexts] = useState([]); // To store all entered texts

    // Handle file selection
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
    };

    // Handle text input change
    const handleInputChange = (event) => {
        setInputText(event.target.value);
    };

    // Handle file upload
    const handleUpload = async () => {
        if (!selectedFile) {
            alert("Please select a PDF file first!");
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setPdfUrl(`http://localhost:5000${data.filePath}`);
            } else {
                console.error("Failed to upload PDF");
            }
        } catch (error) {
            console.error("Error uploading PDF", error);
        }
    };

    // Handle button click
    const handleButtonClick = () => {
        if (inputText.trim() === '') {
            alert("Please enter some text.");
            return;
        }

        setDisplayTexts((prevTexts) => [...prevTexts, inputText]); // Append new text to displayTexts
        setInputText(''); // Clear the input field
        handleUpload(); // Call the file upload function
    };

    // Handle text removal
    const handleRemoveText = (index) => {
        setDisplayTexts((prevTexts) => prevTexts.filter((_, i) => i !== index));
    };

    return (
        <div style={{ display: "flex", maxWidth: '600px', flexDirection: "column", margin: '0 auto', padding: '20px', textAlign: 'center' }}>
            <h2>Upload and Automate PDF</h2>
            <div style={{ marginBottom: '20px' }}>
                <label htmlFor="file-upload" style={{ cursor: 'pointer', display: 'block', margin: '0 auto', fontSize: '24px' }}>
                    <FaUpload />
                </label>
                <input
                    type="file"
                    id="file-upload"
                    style={{ display: 'none' }}
                    accept="application/pdf"
                    onChange={handleFileChange}
                />
                {selectedFile && (
                    <FileInfo>
                        <FaUpload style={{ marginRight: '8px' }} />
                        <span>{selectedFile.name}</span>
                    </FileInfo>
                )}
            </div>
            <input
                type="text"
                value={inputText}
                onChange={handleInputChange}
                placeholder="Type your text here..."
                style={{
                    width: '100%',
                    padding: '10px',
                    border: '1px solid #ccc',
                    borderRadius: '4px',
                    marginBottom: '20px',
                    textAlign: 'center',
                    color: "black"
                }}
            />
            <button
                onClick={handleButtonClick}
                style={{
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '4px',
                    backgroundColor: '#007bff',
                    color: '#fff',
                    fontSize: '16px',
                    cursor: 'pointer'
                }}
            >
                Automate
            </button>
            {displayTexts.length > 0 && (
                <div style={{ marginTop: '20px' }}>
                    <p>Texts Entered</p>
                    {displayTexts.map((text, index) => (
                        <P key={index}>
                            {text}
                            <CloseButton onClick={() => handleRemoveText(index)}>
                                <FaTimes />
                            </CloseButton>
                        </P>
                    ))}
                </div>
            )}
            {pdfUrl && (
                <div style={{ marginTop: '20px' }}>
                    <p>Uploaded PDF available at:</p>
                    <a href={pdfUrl} target="_blank" rel="noopener noreferrer" style={{ color: '#007bff' }}>
                        {pdfUrl}
                    </a>
                </div>
            )}
        </div>
    );
};

export default PDFUpload;

// test.jsx
// import React from 'react';
// import { MouseEnterProvider } from '../ui/3d-card.jsx';
// import { CardContainer, CardBody, CardItem } from '../ui/3d-card.jsx';

// export function TextSum() {
//   return (
//     <MouseEnterProvider>
//       <CardContainer className="inter-var">
//         <CardBody className="bg-gray-50 relative group/card  dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1] dark:bg-black dark:border-white/[0.2] border-black/[0.1] w-auto sm:w-[30rem] h-auto rounded-xl p-6 border  ">
//           <CardItem
//             translateZ="50"
//             className="text-xl font-bold text-neutral-600 dark:text-white"
//           >
//             Make things float in air
//           </CardItem>
//           <CardItem
//             as="p"
//             translateZ="60"
//             className="text-neutral-500 text-sm max-w-sm mt-2 dark:text-neutral-300"
//           >
//             Hover over this card to unleash the power of CSS perspective
//           </CardItem>
//           <CardItem translateZ="100" className="w-full mt-4">
//             <img
//               src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2560&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
//               height="1000"
//               width="1000"
//               className="h-60 w-full object-cover rounded-xl group-hover/card:shadow-xl"
//               alt="thumbnail"
//             />
//           </CardItem>
//           <div className="flex justify-between items-center mt-20">
//             <CardItem
//               translateZ={20}
//               as="a"
//               href="https://twitter.com/mannupaaji" 
//               target="_blank"
//               className="px-4 py-2 rounded-xl text-xs font-normal dark:text-white"
//             >
//               Try now →
//             </CardItem>
//             <CardItem
//               translateZ={20}
//               as="button"
//               className="px-4 py-2 rounded-xl bg-black dark:bg-white dark:text-black text-white text-xs font-bold"
//             >
//               Sign up
//             </CardItem>
//           </div>
//         </CardBody>
//       </CardContainer>
//     </MouseEnterProvider>
//   );
// }
