import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import Input from '../ui/Input';
import { CiSearch } from "react-icons/ci";
import { FaUpload } from 'react-icons/fa';
import fblogo from '../assets/fb.png';
import linklogo from '../assets/linkedin.png';
import insta from '../assets/insta.png';
import twitter from '../assets/twitter.jpg'; 
import email from '../assets/email.png';
import yt from '../assets/youtube.png';
import { FaMicrophone } from "react-icons/fa";
import 'ldrs/bouncy';

const Container = styled.div`
  padding: 3rem 2rem 0 2rem;
  // background: linear-gradient(120deg, #1E3A5F, #2B4A77);
    // background: linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  height:100vh; 
  font-family: Neue;
`;

const SubContainer = styled.div`
  display: flex;
  gap: 1.5rem;
  // background: linear-gradient(120deg, #1E3A5F, #2B4A77);
    // background: linear-gradient(45deg, #004D4D, #009999);
  
`;

const FirstContainer = styled.div`
  display: flex;
  width: 50%;
  height: 85vh;
  border-radius: 12px;
  // background: linear-gradient(135deg, #3a5da8, #2a406c);
    // background: linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  padding: 0rem;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  border:1px solid rgba(255, 255, 255, 0.2);
  // box-shadow:0 0 4px 1px #fff;
`;

const SecondContainer = styled.div`
  width: 50%;
  height: 85vh;
  // box-shadow:0 0 4px 1px #fff;
  border-radius: 12px;
  // background: linear-gradient(135deg, #3a5da8, #2a406c);
    // background: linear-gradient(45deg, #004D4D, #009999);
 border:1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 1.2rem;
`;

const NestedContainer = styled.div`
  margin-top:3rem;
  height: 60vh;
  width: 300px;
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const Img = styled.img`
  width: 50px;
  height: 50px;
`;

const Button = styled.button`
  padding: 10px;
  text-align: center;
  color: #000;
  background: #fff;
  border-radius: 17px;
  width: 100%;
  margin-left: 1rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s linear; 
  margin-left: 2rem;
  text-transform: uppercase;
  &:hover {
    background: #000;
    color: #fff;
    border:1px solid rgba(255, 255, 255, 0.2);
  }
`;

const InputContainer = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 1rem;
`;

const FileUploadIcon = styled(FaUpload)`
  font-size: 24px;
  margin-right: 10px;
  cursor: pointer;
`;
const P=styled.p`
height:40vh;
overflow-y:scroll;
// overflow:hidden;

`
const Sample=styled.div`
margin-top:-3rem;
height:100%;
width:100%;

`
const P2=styled.p`

overflow-y:scroll;


`
const MicIcon = styled(FaMicrophone)`
  font-size: ${(props) => (props.active ? '34px' : '28px')};
  color: ${(props) => (props.active ? 'yellow' : 'inherit')};
  cursor: pointer;
  transition: all 0.3s ease;
`;
const Automation = () => {
  const [recognition, setRecognition] = useState(null);
  const [content, setContent] = useState('');
  const [generatedContent, setGeneratedContent] = useState('');
  const [visible, setVisible] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [twitterConnected, setTwitterConnected] = useState(false);
  const [linkedinConnected, setLinkedinConnected] = useState(false);
  const [linkedinContent, setLinkedinContent] = useState('');
  const [twitterContent, setTwitterContent] = useState('');
  const [currentUser, setCurrentUser] = useState(null);
  const [youtubeConnected, setYoutubeConnected] = useState(false);
  const [facebookContent, setFacebookContent] = useState('');
  const [facebookConnected, setFacebookConnected] = useState(false);
  const [isMicActive, setIsMicActive] = useState(false);

  useEffect(() => {
    // Check if Facebook access token exists
    const checkFacebookAccess = async () => {
      try {
        const response = await axios.get('http://localhost:5000/check_facebook_access');
        if (response.data.connected) {
          setFacebookConnected(true);
        }
      } catch (error) {
        console.error('Error checking Facebook access:', error);
      }
    };

    checkFacebookAccess();
  }, []);


  useEffect(() => {
    fetch('/discord/user')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setCurrentUser(data.current_user);
        }
      });
  }, []);
  useEffect(() => {
    // Check if YouTube access token exists
    const checkYouTubeAccessToken = async () => {
      try {
        const youtubeResponse = await axios.get('http://localhost:5000/check_youtube_access');
        setYoutubeConnected(youtubeResponse.data.connected);
      } catch (error) {
        console.error('Error checking YouTube access token:', error);
      }
    };

    checkYouTubeAccessToken();
  }, []);
  useEffect(() => {
    // Check if Twitter access token exists
    const checkTwitterAccess = async () => {
      try {
        const response = await axios.get('http://localhost:5000/check_twitter_access');
        if (response.data.connected) {
          setTwitterConnected(true);
        }
      } catch (error) {
        console.error('Error checking Twitter access:', error);
      }
    };

    checkTwitterAccess();
  }, []);
  const initSpeechRecognition = () => {
    if (!recognition) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        const recognitionInstance = new SpeechRecognition();

        recognitionInstance.continuous = false;
        recognitionInstance.interimResults = false;
        recognitionInstance.lang = 'ta-IN';

        recognitionInstance.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          setContent(transcript);
        };

        recognitionInstance.onerror = (event) => {
          console.error('Speech recognition error', event.error);
        };
        recognitionInstance.onstart = () => setIsMicActive(true); // Set microphone active state
        recognitionInstance.onend = () => setIsMicActive(false);
        setRecognition(recognitionInstance);
      } else {
        console.error('Speech Recognition API not supported in this browser.');
      }
    }
  };

  useEffect(() => {
    initSpeechRecognition();
  }, []); // Initialize on component mount

  const handleVoiceInput = () => {
    if (recognition) {
      recognition.start();
    }
  };
  const handleGenerateContent = async (e) => {
    e.preventDefault();
    setLoading(true)
    if (content.includes('Twitter')) {
      try {
        const response = await axios.post('http://localhost:5000/generate_tweet', {
          text: content
        });
        setTwitterContent(response.data.tweet);
      } catch (error) {
        console.error('Error generating tweet:', error.response ? error.response.data : error.message);
        
      }
    } else if (content.includes('linkedin')) {
      try {
        const formData = new FormData();
        formData.append('content', content);
        if (image) {
            formData.append('image', image);
        }

        const response = await axios.post('http://localhost:5000/generate_linkedin_content', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });

        if (response.data.error) {
            console.error(response.data.error);
            alert('An error occurred while generating content.');
        } else {
            setLinkedinContent({
                content: response.data.content,
                imageUrl: response.data.image_url // Assuming this is the URL of the uploaded image
            });
        }
    } catch (error) {
        console.error('Error generating content:', error);
        alert('An error occurred while generating content.');
    }
} else if (content.includes('youtube')) {
  try {
    const formData = new FormData();
    formData.append('content', content);
    if (image) {
      formData.append('file', image);
    }

    const response = await axios.post('http://localhost:5000/youtube_upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    if (response.data.message) {
      setSuccess('Video uploaded successfully!');
      setGeneratedContent(response.data.message);
    } else {
      setError('An error occurred while uploading the video.');
    }
  } catch (error) {
    console.error('Error uploading video:', error);
    setError('An error occurred while uploading the video.');
  } finally {
    setLoading(false);
  }
} else if (content.includes('facebook')) {
  try {
    const response = await axios.post('http://localhost:5000/generate_facebook_content', {
      text: content
    });
    setFacebookContent(response.data.content);
  } catch (error) {
    console.error('Error generating Facebook content:', error.response ? error.response.data : error.message);
    
  }
}
setLoading(false);
  };


  const handlePostContent = async () => {
    if (content.includes('Twitter')) {
      if (!twitterContent) {
        alert('No tweet content to post.');
        return;
      }

      try {
        const response = await axios.post('http://localhost:5000/post_tweet', {
          tweet: twitterContent
        });

        if (response.data.success) {
          alert(response.data.message || 'Tweet posted successfully!');
        } else {
          alert('An error occurred while posting the tweet.');
        }
      } catch (error) {
        console.error('Error posting tweet:', error.response ? error.response.data : error.message);
        alert('An error occurred while posting the tweet. Please check the console for details.');
      }
    } else if (content.includes('linkedin')) {
      if (!linkedinContent) {
        alert('No LinkedIn content to post.');
        return;
      }

      try {
        const formData = new FormData();
          
        formData.append('content',linkedinContent.content



          );
        if (image) {
            formData.append('image', image);
        }

        const response = await axios.post('http://localhost:5000/post_linkedin', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });

        if (response.data.success) {
            alert('Content posted successfully!');
        } else {
            alert('Failed to post content.');
        }
    } catch (error) {
        console.error('Error posting content:', error);
        alert('An error occurred while posting content.');
    }
  } else if (content.includes("facebook")) {
    if (!facebookContent) {
      alert('No LinkedIn content to post.');
      return;
    }
    try {
      const response = await axios.post('http://localhost:5000/post_facebook', {
        content: facebookContent
      });

      if (response.data.success) {
        alert(response.data.message || 'Content posted successfully!');
      } else {
        alert(response.data.message || 'An error occurred while posting the content.');
      }
    } catch (error) {
      console.error('Error posting content:', error.response ? error.response.data : error.message);
      alert('An error occurred while posting the content. Please check the console for details.');
    }}
  };
  const handleFacebookConnect = () => {
    window.location.href = 'http://localhost:5000/facebook/connect';
  };

  const handleYouTubeConnect = async () => {
    try {
      const response = await axios.get('http://localhost:5000/youtube/connect');
      if (response.data.success) {
        alert(response.data.message);
      } else {
        alert('YouTube connection failed: ' + response.data.message);
      }
    } catch (error) {
      console.error('Error connecting to YouTube:', error);
      alert('An error occurred while connecting to YouTube. Please check the console for details.');
    }
  };
  const handleTwitterConnect = () => {
    window.location.href = 'http://localhost:5000/start_twitter_oauth';
  };

  const handleLinkedInConnect = () => {
    window.location.href = 'http://localhost:5000/linkedin/login';
  };
  
  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };
  const handleDiscordConnect = async () => {
    window.location.href = 'http://localhost:5000/discord/connect'
    try {
      const response = await axios.get("/discord/connect");
      if (response.data.success) {
        console.log("Discord connected successfully!");
      } else {
        console.error("Failed to connect to Discord:", response.data.message);
      }
    } catch (error) {
      console.error("Error during Discord connection:", error);
    }
  };

  return (
    <Container>
      <SubContainer>
        <FirstContainer>
          {visible ? (
            <NestedContainer>
              <div style={{display:"flex", justifyContent: "space-between" }}>
                <Img src={linklogo} />
                <Button onClick={handleLinkedInConnect}>Connect</Button>
              </div>
              <div style={{display:"flex", justifyContent: "space-between" }}>
                <Img src={twitter} />
                <Button onClick={handleTwitterConnect}>
                  {twitterConnected ? 'Connected' : 'Connect'}
                </Button>
              </div>
              {/* <div style={{ display: "flex", justifyContent: "space-between", marginTop: "-1rem" }}>
                <Img style={{ width: "100px", height: "100px", marginLeft: "-1.5rem" }} src={insta} />
                <div style={{ width: "100%" }}>
                  <Button style={{ width: "194px", marginLeft: "0.2rem", marginTop: "1.4rem", height: "7vh" }}>Connect</Button>
                </div>
              </div> */}
               <div style={{ display: "flex", justifyContent: "space-between", marginTop: "0rem" }}>
                <Img src={fblogo} />
                <Button>Connect</Button>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", marginTop: "0rem" }}>
                <Img src={email} />
                <Button onClick={handleDiscordConnect}>Connect</Button>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", marginTop: "0.5rem" }}>
                <Img src={yt} />
                <Button onClick={handleYouTubeConnect}>Connect</Button>
              </div>
             
            </NestedContainer>
          ) : (
            <div>{content && content}</div>
          )}
          <form onSubmit={handleGenerateContent}>
            <InputContainer>
              <FileUploadIcon onClick={() => document.getElementById('file-upload').click()} />
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                style={{ display: 'none' }}
                id="file-upload"
              />
              <Input
                style={{ width: "500px", background: "#000", color: "#fff" }}
                placeholder="Ask Anything"
                name="automater"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                type="text"
              />
              
              <button type="submit">
                <CiSearch style={{ display: "flex", justifyContent: "center", alignItems: "center", width: "70px", height: "30px", marginLeft: "-5rem" }} />
              </button>
              <MicIcon 
                active={isMicActive} 
                onClick={handleVoiceInput} 
              />
            </InputContainer>
          </form>
        </FirstContainer>
        <SecondContainer>
          <div>
            {loading ? (
              <>
               <l-bouncy
                    size="45"
                    speed="1.75"
                    color="#fff"
                  ></l-bouncy>
              </>
            ):(
              <>
                {twitterContent && !linkedinContent && !facebookContent && (
            <>
              <Sample>
                <P2>{twitterContent}</P2>
              </Sample>
             
              <div style={{display:"flex",width:"100%",justifyContent:"end"}}>
              <Button style={{marginLeft:"-0.3rem",width:"200px"}}onClick={handlePostContent}>Post</Button>
              <Button style={{marginLeft:"-0.3rem",width:"200px"}}onClick={handleNarrateContent}>Narrate</Button>
              </div>
             </>
           )}
           {linkedinContent && (
            <><Sample>
              <P>{linkedinContent.content}</P>
            </Sample>
             
            {linkedinContent.imageUrl && (<>
              <div style={{display:"flex",width:"100%",marginTop:"-4rem",justifyContent:"center"}}>
              <Img style={{width:"150px",height:"150px"}} src={linkedinContent.imageUrl} alt="Generated" />
              </div>
            </>
              
            )}
            <div style={{display:"flex",width:"100%",justifyContent:"end"}}>
            <Button style={{marginLeft:"-0.3rem",width:"200px"}}onClick={handlePostContent}>Post</Button>
            <Button style={{marginLeft:"-0.3rem",width:"200px"}}onClick={handleNarrateContent}>Narrate</Button>
            </div>
        </> )}

                {facebookContent && !linkedinContent && !twitterContent && (
                  <>
                    <Sample>
                      <P>{facebookContent}</P>
                    </Sample>
                    <div style={{display:"flex",width:"100%",justifyContent:"end"}}>
                      <Button style={{marginLeft:"-0.3rem",width:"200px"}} onClick={handlePostContent}>Post</Button>
                      <Button style={{marginLeft:"-0.3rem",width:"200px"}}onClick={handleNarrateContent}>Narrate</Button>
                    </div>
                  </>
                )}

              </>
            )
          }
        </div>
       </SecondContainer>
    </SubContainer>
    </Container>
  );
}

export default Automation;