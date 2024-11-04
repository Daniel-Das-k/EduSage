import React from 'react';
import ReactPlayer from 'react-player/youtube';
import styled from 'styled-components';

const VideoContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  // padding:2rem;  
  height: 100vh;
  // background: linear-gradient(135deg, #3a5da8, #2a406c); 

 /* Green and white gradient */
`;

const Flutter = () => {
  return (
    <VideoContainer>
      <ReactPlayer
        url='https://www.youtube.com/watch?v=CzRQ9mnmh44'
        controls={true}
        width='100%'
        height='100%'
        muted={false}
      />
    </VideoContainer>
  );
};

export default Flutter;
