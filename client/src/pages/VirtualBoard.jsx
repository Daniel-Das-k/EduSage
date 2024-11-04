import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './VirtualBoard.css';

const VirtualFeed = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const [aiOutput, setAiOutput] = useState('');  // State for storing AI output

  useEffect(() => {
    const fetchVideoFeed = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/video_feed', {
          responseType: 'blob'
        });
        const videoBlob = new Blob([response.data], { type: 'video/mp4' });
        const videoObjectUrl = URL.createObjectURL(videoBlob);
        setVideoUrl(videoObjectUrl);
      } catch (error) {
        console.error('Error fetching video feed:', error);
      }
    };

    const fetchAiOutput = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_ai_output');
        setAiOutput(response.data.ai_output);
      } catch (error) {
        console.error('Error fetching AI output:', error);
      }
    };

    fetchVideoFeed();
    
    // Poll the AI output every 3 seconds
    const aiOutputInterval = setInterval(fetchAiOutput, 3000);

    return () => clearInterval(aiOutputInterval);  // Cleanup on unmount
  }, []);
console.log(aiOutput)
  return (
    <div >
        <h1>
            Image
        </h1>
        <div style={{borderRadius:"1px"}}>
        <img 
        className='daniel'
        src="http://127.0.0.1:5000/video_feed" 
        alt="Video Feed"
        
      />
        </div>
      
      <div className="ai-output">
        <h2 style={{color:"white"}}>AI Output:</h2>
        {aiOutput && (
            <>
            <p style={{color:"white"}}>{aiOutput}</p>
            </>
        )}
        
      </div>
    </div>
  );
};

export default VirtualFeed;


