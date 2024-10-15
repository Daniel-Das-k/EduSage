import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
`;

const Input = styled.input`
  padding: 10px;
  font-size: 16px;
  margin-bottom: 20px;
  width: 300px;
`;

const Button = styled.button`
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
`;

const ImageContainer = styled.div`
  margin-top: 20px;
`;

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  const handleGenerate = async () => {
    try {
      const response = await axios.post('http://localhost:5000/generate-image', { prompt }, {
        responseType: 'blob', // Important for handling binary data
      });

      const imageBlob = response.data;
      const imageObjectURL = URL.createObjectURL(imageBlob);
      setImageUrl(imageObjectURL);
    } catch (error) {
      console.error('Error generating image:', error);
    }
  };

  return (
    <Container>
      <h1>Image Generator</h1>
      <Input
        type="text"
        placeholder="Enter prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <Button onClick={handleGenerate}>Generate Image</Button>
      {imageUrl && (
        <ImageContainer>
          <img src={imageUrl} alt="Generated" />
        </ImageContainer>
      )}
    </Container>
  );
};

export default App;
