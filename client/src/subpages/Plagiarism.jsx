import React, { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';


const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
`;

const TextArea = styled.textarea`
  width: 100%;
  max-width: 500px;
  height: 100px;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
  color:black;
`;

const Button = styled.button`
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 1rem;
`;

const Result = styled.pre`

  margin-top: 2rem;
  font-size: 1.2rem;
  color: #fff;
`;

const Plagiarism = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);

  const handleClassify = async () => {
    console.log('Button clicked, starting classification...'); // Add this line
    try {
      const response = await axios.post('http://localhost:5000/plagiarism', { text });
      console.log('Response received:', response.data); // Add this line
      setResult(response.data.result);
    } catch (error) {
      console.error('Error classifying text:', error);
    }
  };
  return (
    <Container>
      <h1>Text Classification</h1>
      <TextArea
        placeholder="Enter text to classify"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <Button onClick={handleClassify}>Classify</Button>
      {result && (
        <Result>
          <h2>Classification Result:</h2>
          {result.map((res, index) => (
            <div key={index}>{res.label}: {res.score.toFixed(4)}</div>
          ))}
        </Result>
      )}
    </Container>
  );
};

export default Plagiarism;
// import React, { useState } from 'react';
// import axios from 'axios';

// const Plagiarism = () => {
//   const [content, setContent] = useState('');
//   const [file, setFile] = useState(null);
//   const [message, setMessage] = useState('');

//   const handleFileChange = (event) => {
//     setFile(event.target.files[0]);
//   };

//   const handleContentChange = (event) => {
//     setContent(event.target.value);
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
    
//     const formData = new FormData();
//     formData.append('content', content);
//     formData.append('file', file);

//     try {
//       const response = await axios.post('http://127.0.0.1:5000/youtube_upload', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       });
//       setMessage(response.data.message);
//     } catch (error) {
//       console.error('Error uploading video:', error);
//       setMessage('Failed to upload video.');
//     }
//   };

//   return (
//     <div>
//       <h1>Upload Video</h1>
//       <form onSubmit={handleSubmit}>
//         <div>
//           <label htmlFor="content">Video Content:</label>
//           <input
//             type="text"
//             id="content"
//             value={content}
//             onChange={handleContentChange}
//             required
//           />
//         </div>
//         <div>
//           <label htmlFor="file">Video File:</label>
//           <input
//             type="file"
//             id="file"
//             onChange={handleFileChange}
//             required
//           />
//         </div>
//         <button type="submit">Upload</button>
//       </form>
//       {message && <p>{message}</p>}
//     </div>
//   );
// };

// export default Plagiarism;