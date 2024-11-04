// // import React, { useState } from 'react';
// // import styled from 'styled-components';
// // import { useNavigate } from 'react-router-dom';
// // import axios from 'axios';

// // const Container = styled.div`
// //   display: flex;
// //   justify-content: center;
// //   align-items: center;
// //   height: 100vh;
// //   width: 100%;
// // `;

// // const SubContainer = styled.div`
// //   background: #242424;
// //   min-height: 52vh;
// //   width: 30rem;
// //   border-radius: 2rem;
// // `;

// // const Input = styled.input`
// //   width: 70%;
// //   padding: 7px;
// //   margin: 1rem 0 1rem 0;
// //   border-bottom: 1px solid #fff;
// //   background: #242424;
// //   outline: none;
// // `;

// // const InputHolder = styled.div`
// //   display: flex;
// //   justify-content: center;
// //   align-items: center;
// //   flex-direction: column;
// // `;

// // const Button = styled.button`
// //   width: 70%;
// //   height: 50px;
// //   padding: 7px;
// //   margin: 2rem 0 0.5rem 0;
// //   border-radius: 29px;
// //   background: #fff;
// //   color: #242424;
// //   font-weight: bolder;
// //   font-size: 17px;
// //   transition: all 0.4s ease;
// //   &:active {
// //     transform: scale(0.9);
// //   }
// // `;

// // const Span = styled.span`
// //   padding: 0 0 4px 7px;
// //   text-decoration: underline;
// //   text-underline-offset: 4px;
// //   cursor: pointer;
// // `;

// // const Register = () => {
  
// //   const navigate = useNavigate();
// //   const [username, setUsername] = useState('');
// //   const [email, setEmail] = useState('');
// //   const [password, setPassword] = useState('');
// //   const [photo, setPhoto] = useState(null);
// //   const [errmsg, setErrmsg] = useState('');
// //   const [showerrmsg, setShowErrmsg] = useState(false);
// //   const [allerrmsg, setallErrmsg] = useState('');

// //   const handleKeyPress = (e) => {
// //     if (e.key === 'Enter') {
// //       handleRegister();
// //     }
// //   };

// //   const handleRegister = async () => {
// //     if (!username || !email || !password) {
// //       setShowErrmsg(true);
// //       setallErrmsg('Please fill in all fields');
// //       return;
// //     }

// //     const formData = new FormData();
// //     formData.append('username', username);
// //     formData.append('email', email);
// //     formData.append('password', password);
// //     if (photo) {
// //       formData.append('photo', photo);
// //     }

// //     try {
// //       const response = await axios.post('http://localhost:5000/user/signup', formData, {
// //         headers: {
// //           'Content-Type': 'multipart/form-data'
// //         }
// //       });
// //       if (response.data.success) {
// //         setUsername(response.data.username)
// //         setPhoto(response.data.photo)
// //         navigate('/');
// //       } else {
// //         setallErrmsg(response.data.message);
// //       }
// //     } catch (error) {
// //       console.error('Registration error:', error);
// //     }
// //   };

// //   return (
// //     <Container>
// //       <SubContainer>
// //         <p style={{ fontSize: '25px', fontWeight: 'bolder', textAlign: 'center', padding: '1rem 0' }}>
// //           Register
// //         </p>
// //         <InputHolder>
// //           <Input
// //             type="text"
// //             placeholder="Username"
// //             value={username}
// //             onChange={(e) => {
// //               setUsername(e.target.value);
// //               setErrmsg(false);
// //               setallErrmsg('');
// //             }}
// //             onKeyDown={handleKeyPress}
// //           />
// //           <Input
// //             type="text"
// //             placeholder="Email"
// //             value={email}
// //             onChange={(e) => {
// //               setEmail(e.target.value);
// //               setErrmsg(false);
// //               setallErrmsg('');
// //             }}
// //             onKeyDown={handleKeyPress}
// //           />
// //           <Input
// //             type="password"
// //             placeholder="Password"
// //             value={password}
// //             onChange={(e) => {
// //               setPassword(e.target.value);
// //               setErrmsg(false);
// //               setallErrmsg('');
// //             }}
// //             onKeyDown={handleKeyPress}
// //           />
// //           <Input
// //             type="file"
// //             accept="image/*"
// //             onChange={(e) => setPhoto(e.target.files[0])}
// //           />
// //           <Button onClick={handleRegister}>
// //             Register
// //           </Button>
// //           {allerrmsg && (
// //             <p style={{ margin: "1rem 0 0 0",color:"red" }}>{allerrmsg}</p>
// //           )}
// //           <p style={{ padding: "1.5rem" }}>
// //             Already have an account? <Span onClick={() => navigate('/')}>Login</Span>
// //           </p>
// //         </InputHolder>
// //       </SubContainer>
// //     </Container>
// //   );
// // };

// // export default Register;
// import React, { useContext, useState, useEffect } from 'react';
// import styled from 'styled-components';
// import { useNavigate } from 'react-router-dom';
// import axios from 'axios';
// import { Context } from '../context/Context';

// const Container = styled.div`
//   display: flex;
//   justify-content: center;
//   align-items: center;
//   height: 100vh;
//   width: 100%;
//   background:#242424
// `;

// const SubContainer = styled.div`
//   background: #242424;
//   min-height: 52vh;
//   width: 30rem;
//   border-radius: 2rem;
//   background: linear-gradient(135deg, #3a5da8, #2a406c);
//   `;


// const Input = styled.input`
//   width: 70%;
//   padding: 7px;
//   margin: 1rem 0 1rem 0;
//   border-bottom: 1px solid #fff;
//   background: linear-gradient(135deg, #3a5da8, #2a406c);
//   outline: none;
// `;

// const InputHolder = styled.div`
//   display: flex;
//   justify-content: center;
//   align-items: center;
//   flex-direction: column;
// `;

// const Button = styled.button`
//   width: 70%;
//   height: 50px;
//   padding: 7px;
//   margin: 2rem 0 0.5rem 0;
//   border-radius: 29px;
//   background: #fff;
//   color: #242424;
//   font-weight: bolder;
//   font-size: 17px;
//   transition: all 0.4s ease;
//   &:active {
//     transform: scale(0.9);
//   }
// `;

// const Span = styled.span`
//   padding: 0 0 4px 7px;
//   text-decoration: underline;
//   text-underline-offset: 4px;
//   cursor: pointer;
// `;

// const ImgPreview = styled.img`
//   width: 100px;
//   height: 100px;
//   border-radius: 50%;
//   margin-top: 1rem;
// `;

// const Register = () => {
//   const navigate = useNavigate();
//   const [username, setUsername] = useState('');
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//    //const [photo, setPhoto] = useState(null);
//   const [errmsg, setErrmsg] = useState('');
//   const [showerrmsg, setShowErrmsg] = useState(false);
//   const [allerrmsg, setallErrmsg] = useState('');
//   const [photo, setPhoto] = useState(null);
//   const [photoPreview, setPhotoPreview] = useState(null);

//   useEffect(() => {
//     if (photo) {
//       const reader = new FileReader();
//       reader.onloadend = () => {
//         setPhotoPreview(reader.result);
//       };
//       reader.readAsDataURL(photo);
//     } else {
//       setPhotoPreview(null);
//     }
//   }, [photo]);

//   const handleKeyPress = (e) => {
//     if (e.key === 'Enter') {
//       handleRegister();
//     }
//   };

//   const handleRegister = async () => {
//     if (!username || !email || !password) {
//       setShowErrmsg(true);
//       setAllErrmsg('Please fill in all fields');
//       return;
//     }

//     const formData = new FormData();
//     formData.append('username', username);
//     formData.append('email', email);
//     formData.append('password', password);
//     if (photo) {
//       formData.append('photo', photo);
//     }

//     try {
//       const response = await axios.post('http://localhost:5000/user/signup', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data'
//         }
//       });
//       if (response.data.success) {
//         setUsername(response.data.username);
//         navigate('/');
//       } else {
//         setallErrmsg(response.data.message);
//       }
//     } catch (error) {
//       console.error('Registration error:', error);
//     }
//   };

//   return (
//     <Container>
//       <SubContainer>
//         <p style={{ fontSize: '25px', fontWeight: 'bolder', textAlign: 'center', padding: '1rem 0' }}>
//           Register
//         </p>
//         <InputHolder>
//           <Input
//             type="text"
//             placeholder="Username"
//             value={username}
//             onChange={(e) => {
//               setUsername(e.target.value);
//               setErrmsg(false);
//               setAllErrmsg('');
//             }}
//             onKeyDown={handleKeyPress}
//           />
//           <Input
//             type="text"
//             placeholder="Email"
//             value={email}
//             onChange={(e) => {
//               setEmail(e.target.value);
//               setErrmsg(false);
//               setAllErrmsg('');
//             }}
//             onKeyDown={handleKeyPress}
//           />
//           <Input
//             type="password"
//             placeholder="Password"
//             value={password}
//             onChange={(e) => {
//               setPassword(e.target.value);
//               setErrmsg(false);
//               setAllErrmsg('');
//             }}
//             onKeyDown={handleKeyPress}
//           />
//           <Input
//             type="file"
//             accept="image/*"
//             onChange={(e) => setPhoto(e.target.files[0])}
//           />
//           {photoPreview && <ImgPreview src={photoPreview} alt="Profile Preview" />}
//           <Button onClick={handleRegister}>
//             Register
//           </Button>
//           {allerrmsg && (
//             <p style={{ margin: "1rem 0 0 0" ,color:"red"}}>{allerrmsg}</p>
//           )}
//           <p style={{ padding: "1.5rem" }}>
//             Already have an account? <Span onClick={() => navigate('/')}>Login</Span>
//           </p>
//         </InputHolder>
//       </SubContainer>
//     </Container>
//   );
// };

// export default Register;
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  background: #000;
`;

const SubContainer = styled.div`
  background: #000;
  backdrop-filter: blur(10px); 
  border: 1px solid #fff;
  min-height: 50vh;
  width: 30rem;
  border-radius: 2rem;
`;

const Input = styled.input`
  width: 70%;
  padding: 7px;
  margin: 1rem 0;
  background: #000;
  outline: none;
`;

const InputHolder = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`;

const Button = styled.button`
  width: 70%;
  height: 60px;
  padding: 10px;
  margin: 1rem 0;
  border-radius: 29px;
  background: #fff;
  color: #000;
  font-weight: bolder;
  font-size: 20px;
  transition: all 0.4s ease;
  &:active {
    transform: scale(0.9);
  }
`;

const Span = styled.span`
  padding: 0 0 4px 7px;
  text-decoration: underline;
  text-underline-offset: 4px;
  cursor: pointer;
`;

const ImgPreview = styled.img`
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-top: 1rem;
`;

const Register = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errmsg, setErrmsg] = useState('');
  const [showerrmsg, setShowErrmsg] = useState(false);
  const [allerrmsg, setallErrmsg] = useState('');
  const [photo, setPhoto] = useState(null);
  const [photoPreview, setPhotoPreview] = useState(null);

  useEffect(() => {
    if (photo) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result);
      };
      reader.readAsDataURL(photo);
    } else {
      setPhotoPreview(null);
    }
  }, [photo]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleRegister();
    }
  };

  const handleRegister = async () => {
    if (!username || !email || !password) {
      setShowErrmsg(true);
      setallErrmsg('Please fill in all fields');
      return;
    }

    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password', password);
    if (photo) {
      formData.append('photo', photo);
    }

    try {
      const response = await axios.post('http://localhost:5000/user/signup', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      if (response.data.success) {
        setUsername(response.data.username);
        navigate('/');
      } else {
        setallErrmsg(response.data.message);
      }
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  return (
    <Container style={{ fontFamily: "Neue" }}>
      <SubContainer>
        <p style={{ fontSize: '40px', fontWeight: 'bolder', textAlign: 'center', padding: '1rem 0' }}>
          Register
        </p>
        <InputHolder>
          <Input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              setErrmsg(false);
              setallErrmsg('');
            }}
            onKeyDown={handleKeyPress}
          />
          <Input
            type="text"
            placeholder="Email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setErrmsg(false);
              setallErrmsg('');
            }}
            onKeyDown={handleKeyPress}
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setErrmsg(false);
              setallErrmsg('');
            }}
            onKeyDown={handleKeyPress}
          />
          <Input
            type="file"
            accept="image/*"
            onChange={(e) => setPhoto(e.target.files[0])}
          />
          {photoPreview && <ImgPreview src={photoPreview} alt="Profile Preview" />}
          <Button onClick={handleRegister}>
            Register
          </Button>
          {allerrmsg && (
            <p style={{ margin: "1rem 0 0 0", color: "red" }}>{allerrmsg}</p>
          )}
          <p style={{ padding: "1.5rem" }} className='text-xl'>
            Already have an account? <Span onClick={() => navigate('/')}>Login</Span>
          </p>
        </InputHolder>
      </SubContainer>
    </Container>
  );
};

export default Register;
