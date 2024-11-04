import React, { useContext, useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Context } from '../context/Context';
import { FaCamera } from "react-icons/fa";
import { FaPencilAlt } from "react-icons/fa";
import { FaFile } from "react-icons/fa";
import { MdFileUpload } from "react-icons/md";
import Js from '../assets/javascript.png';

import C from '../assets/C_Logo.png'
import python from '../assets/python.png';
import html from '../assets/html.png';
import Modal from '../ui/Modal';
// import { AnimatedBeam } from '../ui/AnimatedBeam.jsx';
// import { AnimatedBeam } from '../ui/Animation.jsx';
const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  // padding:2rem;
  // padding-left:5rem;
  // padding-top:1rem;
  height: 100vh;
  width: 100%;
  // background: linear-gradient(120deg, #1E3A5F, #2B4A77); 
  // background: linear-gradient(45deg, #004D4D, #009999);
   background:#000;
  //  gap:3rem;
  
`;

const SubContainer = styled.div`
    // background: linear-gradient(45deg, #004D4D, #009999);
    background:#000;
 /* Semi-transparent white */
  backdrop-filter: blur(10px); /* Frosted glass effect */
  border: 1px solid #fff;
   /* Light border for glass effect */ 
  min-height: 50vh;
  // padding:2rem;
  width: 30rem;
  
  border-radius: 2rem;
  // box-shadow: 0 0 9px 1px #fff;
  -webkit-backdrop-filter: blur(10px); /* Support for Safari */
`;


const Input = styled.input`
  width: 70%;
  padding: 7px;
  margin: 1rem 0 1rem 0;
  // background: rgba(255, 255, 255, 0.1); /* Semi-transparent white */
  outline: none;
  // background: linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  
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
  margin: 1rem 0 0.5rem 0;
  border-radius: 29px;
  background: linear-gradient(45deg, #004D4D, #009999);
  background:#fff;
  
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

const Button3=styled.button`
  width: 70%;
  height: 60px;
  padding: 10px;
  margin: 2rem 0 0.5rem 0;
  border-radius: 29px;
  // background: linear-gradient(45deg, #004D4D, #009999);
  background:#fff;
  border:1px solid #009999;
  
  font-weight: bolder;
  font-size: 17px;
  transition: all 0.4s ease;
  &:active {
    transform: scale(0.9);
  }
`;
  
const Login = () => {
  const {photo,setPhoto}=useContext(Context)
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errmsg, setErrmsg] = useState('');
  const [showerrmsg, setShowErrmsg] = useState(false);
  const [allerrmsg, setallErrmsg] = useState('');
  const {setUsername}=useContext(Context)
  const [open, setOpen] = useState(false)

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleLogin();
    }
  };

  const handleLogin = async () => {
    if (!email || !password) {
      setShowErrmsg(true);
      setallErrmsg('Please fill in all fields');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/user/login', { email, password });
      if (response.data.success) {
        setUsername(response.data.username);
        setPhoto(response.data.photo);
        navigate('/Home');
      } else {
        setallErrmsg(response.data.message);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <Container style={{fontFamily:"Neue"}} >
      {/* <AnimatedBeam /> */}
      <SubContainer >
        <p className="" style={{ fontSize: '40px', fontWeight: 'bolder', textAlign: 'center', padding: '1rem 0' }}>
          Login
        </p>
        <div className='bg-black flex flex-col items-center p-[1rem] gap-2 rounded-full'>
          <input
          className='w-full text-xl text-center bg-black py-3 px-5 outline-none border-t-[1px]'
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
          {!email && (
            <p style={{ textAlign: "left", width: "70%", padding: "0" }}>{errmsg}</p>
          )}
          <input
            className='w-full text-xl text-center bg-black py-3 px-5 outline-none border-b-[1px]'
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
          {!password && (
            <p style={{ textAlign: "left", width: "70%", padding: "0" }}>{errmsg}</p>
          )}
          
          <Button  onClick={handleLogin}>
            Login
          </Button>
          
          
          {allerrmsg && (
            <p style={{ margin: "1rem 0 0 0",color:"red" }}>{allerrmsg}</p>
          )}
          <p style={{ padding: "1.5rem" }} className='text-xl'>
            Don't have an account? <Span onClick={() => navigate('/Register')}>Register</Span>
          </p>
        </div>
         {/* <h1 className='text-black text-3xl text-center'>Questions</h1>
        <div>
          <p className='text-black mt-8 ' style={{color:"#009999"}}>You are tasked with building a recommendation system for an e-commerce platform serving millions of users. Explain the machine learning approach you would use, such as collaborative filtering or content-based filtering, and why it’s appropriate. Provide a short Python code to implement a basic collaborative filtering model using user-item data. How would you handle cold-start issues for new users and products? Additionally, describe how you would ensure scalability for real-time recommendations across millions of users with low latency, and explain how you would evaluate the system’s performance and fairness</p>
          <textarea style={{height:"41vh"}}className='border-black w-full mt-4 p-2 text-black shadow-md rounded-xl shadow-black' placeholder='Enter Your Answer here'></textarea>
        </div> 
         {/* <div>
          <p className='text-black mt-5' style={{color:"#009999"}}>2. If a webpage is loading slowly, what steps would you take to identify and resolve the issue?</p>
          <textarea className='border-black w-full border-2 text-black mt-4 h-24 p-2 shadow-md rounded-xl shadow-black'  placeholder='Enter Your Answer here'></textarea>
        </div>
        <div>
          <p className='text-black mt-5' style={{color:"#009999"}}>3. Can you describe a time when you had to refactor or optimize a piece of code? What was the issue, and what specific steps did you take to improve the code?</p>
          <textarea className='border-black w-full border-2 mt-4 text-black h-24 p-2 shadow-md rounded-xl shadow-black'  placeholder='Enter Your Answer here'></textarea>
        </div> */}
        </SubContainer>
        {/* <SubContainer>
          {/* <h1 className='text-3xl text-center'>Prove your Coding Skills</h1>
          <p className='mt-8' style={{color:"#009999"}}>Implement a debounce function in JavaScript. This function should limit the rate at which a specified callback function is executed. The debounce function should take two arguments: a callback function and a delay in milliseconds. It should ensure that the callback is invoked only after a specified period of inactivity, i.e., the function should not be called if another event occurs within the delay period.</p> */}
          {/* <textarea style={{height:"77vh"}}className='border-black w-full mt-2 p-2 text-black shadow-md rounded-xl shadow-black' placeholder='Enter Your Code here'/> */}
          {/* <button onClick={() => setOpen(true)} className='w-48 mt-4 p-2 text-center text-white font-bold  rounded-xl' style={{background:"#009999",marginLeft:"24rem"}}>Next</button> */} 
      {/* </SubContainer> */} 
      {/* <Modal open={open}  onClose={() => setOpen(false)}>
        <div className="text-center w-96 flex-col justify-center items-center"> */}
          {/* <Trash size={56} className="mx-auto text-red-500" /> */}
          {/* <div className="mx-auto my-4 w-full">
            <h3 className="text-3xl font-black my-4 text-gray-800">Quick Question</h3>
            <p className="text-XL text-gray-500">
            Given the user-item interaction matrix in the code, explain how the cosine similarity is used to make recommendations. Also, how would you modify the code to recommend the top 3 items for 'user2'?
            </p>
            <textarea className='border-black w-full h-32 mt-4 p-2 text-black shadow-md rounded-xl shadow-black' placeholder='Enter Your Answer here'></textarea>
            <button onClick={() => setOpen(true)} className='w-48 mt-4 p-2 -mr- text-center text-white font-bold  rounded-xl' style={{background:"#009999"}}>Done</button>
            
          </div>
          <div className="flex gap-4">
            <button className="btn btn-danger w-full">Delete</button>
            <button
              className="btn btn-light w-full"
              onClick={() => setOpen(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      </Modal>
      <div >
      <img src={Js} className='w-24 h-16  mt-5 -ml-8'/>
      <img src={python} className='w-16 h-16  mt-5 -ml-8'/>
      <img src={html} className='w-16 h-16  mt-5 -ml-8'/>
      <img src={C} className='w-16 h-16 mt-5 -ml-8'/>
      </div> */}
      

    </Container>
  );
};

export default Login;



      

{/* <h1 className='text-green-500 text-3xl' style={{color:"#009999"}}>
          Your Journey Begins <span className='text-black'>Here</span>
        </h1>
        <p className='text-green-500 mt-6 text-xl' style={{color:"#009999"}}>Getting to know you better helps us match you with the right oppurtunities</p>
        <div className='ml-12'><Button className='flex items-center gap-3 text-xl '>{<FaCamera size={25} className='ml-11' />}Import from Linkedin</Button></div>
        <div className='flex items-center mt-6 '>
          <p className='border-b-2 text-black border-black w-48'></p>
          <h1 className='text-black px-3'>OR</h1>
          <p className='border-b-2 text-black border-black w-48'></p>
        </div>
        <div className='ml-12'><Button className='flex items-center gap-3 text-xl '>{<FaPencilAlt size={25} className='ml-11' />}Upload Manually</Button></div>
        <div className='flex items-center mt-6 '>
          <p className='border-b-2 text-black border-black w-48'></p>
          <h1 className='text-black px-3'>OR</h1>
          <p className='border-b-2 text-black border-black w-48'></p>
        </div>
        <div className='flex gap-5 -ml-9'>
          <Button3 className='flex items-center gap-2 text-xl border-black text-black'>{<FaFile color="#009999"size={25} className='ml-11' />}Select File</Button3>
          <Button className='flex items-center gap-2 text-xl '>{<MdFileUpload size={25} className='ml-11' />}Upload File</Button>
          
        </div> */}

// import React, { useState } from 'react';
// import { ChevronLeft, ChevronRight, MessageCircle, Bell, Upload, Search, Settings, HelpCircle } from 'lucide-react';

// const wireframes = [
//   {
//     title: "Login Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <h2 className="text-xl font-bold mb-4 text-center">ERP Chatbot Login</h2>
//         <input className="block w-full mb-2 p-2 border rounded" placeholder="Username" />
//         <input className="block w-full mb-2 p-2 border rounded" type="password" placeholder="Password" />
//         <input className="block w-full mb-2 p-2 border rounded" placeholder="2FA Email Code" />
//         <button className="w-full bg-blue-500 text-white p-2 rounded mb-2">Log In</button>
//         <div className="flex justify-between">
//           <a href="#" className="text-blue-500">Forgot Password?</a>
//           <a href="#" className="text-blue-500">Need Help?</a>
//         </div>
//       </div>
//     )
//   },
//   {
//     title: "Dashboard Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <div className="flex justify-between items-center mb-4">
//           <h2 className="text-xl font-bold">Dashboard</h2>
//           <div className="flex space-x-2">
//             <Bell size={24} />
//             <Settings size={24} />
//           </div>
//         </div>
//         <div className="grid grid-cols-3 gap-4 mb-4">
//           <div className="border p-2 bg-white rounded">
//             <h3 className="font-bold">IT Tickets</h3>
//             <p className="text-2xl text-center">3 Pending</p>
//           </div>
//           <div className="border p-2 bg-white rounded">
//             <h3 className="font-bold">Leave Balance</h3>
//             <p className="text-2xl text-center">12 Days</p>
//           </div>
//           <div className="border p-2 bg-white rounded">
//             <h3 className="font-bold">Payroll</h3>
//             <p className="text-2xl text-center">Due in 5 days</p>
//           </div>
//         </div>
//         <button className="w-full bg-green-500 text-white p-4 rounded mb-4 flex items-center justify-center">
//           <MessageCircle size={24} className="mr-2" />
//           Open Chatbot
//         </button>
//         <div className="border p-2 bg-white rounded">
//           <h3 className="font-bold mb-2">Notifications</h3>
//           <ul className="list-disc pl-5">
//             <li>New company policy update</li>
//             <li>IT maintenance scheduled</li>
//             <li>Team meeting at 3 PM</li>
//           </ul>
//         </div>
//       </div>
//     )
//   },
//   {
//     title: "Chatbot Interface Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <h2 className="text-xl font-bold mb-4 text-center">ERP Chatbot</h2>
//         <div className="border bg-white p-2 h-48 mb-4 overflow-y-auto">
//           <div className="mb-2 text-right"><span className="bg-blue-100 p-1 rounded">User: I need to check my leave balance</span></div>
//           <div className="mb-2"><span className="bg-gray-100 p-1 rounded">Chatbot: Certainly! Your current leave balance is 12 days. Would you like to apply for leave or see your leave history?</span></div>
//         </div>
//         <div className="flex mb-2">
//           <input className="flex-grow p-2 border rounded-l" placeholder="Type your message..." />
//           <button className="bg-blue-500 text-white p-2 rounded-r">Send</button>
//         </div>
//         <div className="grid grid-cols-3 gap-2 mb-2">
//           <button className="bg-gray-300 p-2 rounded flex items-center justify-center">
//             <Upload size={16} className="mr-1" /> Upload File
//           </button>
//           <button className="bg-gray-300 p-2 rounded">Apply for Leave</button>
//           <button className="bg-gray-300 p-2 rounded">IT Support</button>
//         </div>
//       </div>
//     )
//   },
//   {
//     title: "HR Queries Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <h2 className="text-xl font-bold mb-4">HR Queries</h2>
//         <div className="flex mb-4">
//           <button className="bg-blue-500 text-white p-2 rounded-l flex-grow">Leave Policies</button>
//           <button className="bg-gray-300 p-2 flex-grow">Payroll</button>
//           <button className="bg-gray-300 p-2 rounded-r flex-grow">Benefits</button>
//         </div>
//         <div className="border bg-white p-2 h-40 mb-4 overflow-y-auto">
//           <h3 className="font-bold mb-2">Leave Policies</h3>
//           <p>Annual Leave: 20 days per year</p>
//           <p>Sick Leave: 10 days per year</p>
//           <p>Maternity Leave: 12 weeks paid</p>
//           <p>Paternity Leave: 2 weeks paid</p>
//         </div>
//         <button className="w-full bg-green-500 text-white p-2 rounded">Submit a Request</button>
//       </div>
//     )
//   },
//   {
//     title: "IT Support Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <h2 className="text-xl font-bold mb-4">IT Support</h2>
//         <div className="mb-4">
//           <h3 className="font-bold mb-2">Common Issues</h3>
//           <ul className="list-disc pl-5">
//             <li><a href="#" className="text-blue-500">Password Reset</a></li>
//             <li><a href="#" className="text-blue-500">Software Installation Guide</a></li>
//             <li><a href="#" className="text-blue-500">Network Connectivity Troubleshooting</a></li>
//           </ul>
//         </div>
//         <div className="border bg-white p-2 mb-4">
//           <h3 className="font-bold mb-2">Submit New Ticket</h3>
//           <input className="w-full mb-2 p-2 border rounded" placeholder="Issue Title" />
//           <textarea className="w-full mb-2 p-2 border rounded" placeholder="Describe your issue..."></textarea>
//           <button className="bg-blue-500 text-white p-2 rounded">Submit Ticket</button>
//         </div>
//         <div className="border bg-white p-2">
//           <h3 className="font-bold mb-2">Your Tickets</h3>
//           <p>Ticket #1234: Software Installation - In Progress</p>
//           <p>Ticket #5678: Network Issue - Resolved</p>
//         </div>
//       </div>
//     )
//   },
//   {
//     title: "Document Processing Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <h2 className="text-xl font-bold mb-4">Document Processing</h2>
//         <div className="border-dashed border-2 border-gray-300 p-4 mb-4 text-center">
//           <Upload size={48} className="mx-auto mb-2" />
//           <p>Drag and drop files here or click to upload</p>
//         </div>
//         <div className="mb-4">
//           <div className="mb-2">Processing: AnnualReport.pdf</div>
//           <div className="w-full bg-gray-200 rounded-full h-2.5">
//             <div className="bg-blue-600 h-2.5 rounded-full" style={{width: '45%'}}></div>
//           </div>
//         </div>
//         <div className="border bg-white p-2">
//           <h3 className="font-bold mb-2">Results</h3>
//           <p><strong>Summary:</strong> This document contains the annual financial report for FY 2023, highlighting key performance indicators and growth strategies.</p>
//           <p><strong>Keywords:</strong> Revenue growth, market expansion, digital transformation, sustainability initiatives</p>
//         </div>
//       </div>
//     )
//   },
//   {
//     title: "Settings Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <h2 className="text-xl font-bold mb-4">Settings</h2>
//         <div className="mb-4">
//           <h3 className="font-bold mb-2">Language Preferences</h3>
//           <select className="w-full p-2 border rounded">
//             <option>English</option>
//             <option>Spanish</option>
//             <option>French</option>
//             <option>German</option>
//           </select>
//         </div>
//         <div className="mb-4">
//           <h3 className="font-bold mb-2">Notification Settings</h3>
//           <label className="flex items-center mb-2">
//             <input type="checkbox" className="mr-2" checked /> Email Notifications
//           </label>
//           <label className="flex items-center mb-2">
//             <input type="checkbox" className="mr-2" /> Push Notifications
//           </label>
//           <label className="flex items-center">
//             <input type="checkbox" className="mr-2" checked /> SMS Notifications
//           </label>
//         </div>
//         <div>
//           <h3 className="font-bold mb-2">Two-Factor Authentication</h3>
//           <button className="bg-blue-500 text-white p-2 rounded">Manage 2FA Settings</button>
//         </div>
//       </div>
//     )
//   },
//   {
//     title: "Feedback and Support Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <h2 className="text-xl font-bold mb-4">Feedback and Support</h2>
//         <div className="mb-4">
//           <h3 className="font-bold mb-2">Rate Your Experience</h3>
//           <div className="flex justify-between mb-2">
//             {[1, 2, 3, 4, 5].map(n => (
//               <button key={n} className="bg-yellow-400 text-white w-10 h-10 rounded-full">{n}</button>
//             ))}
//           </div>
//           <textarea className="w-full mb-2 p-2 border rounded" placeholder="Your feedback..."></textarea>
//           <button className="bg-blue-500 text-white p-2 rounded">Submit Feedback</button>
//         </div>
//         <div>
//           <h3 className="font-bold mb-2">Support Options</h3>
//           <p className="mb-1"><strong>Email:</strong> support@erpchatbot.com</p>
//           <p className="mb-1"><strong>Phone:</strong> 1-800-ERP-CHAT</p>
//           <button className="bg-green-500 text-white p-2 rounded mt-2 flex items-center justify-center">
//             <MessageCircle size={20} className="mr-2" /> Start Live Chat
//           </button>
//         </div>
//       </div>
//     )
//   },
//   {
//     title: "Admin Dashboard Screen",
//     content: (
//       <div className="border p-4 bg-gray-100 rounded-lg">
//         <h2 className="text-xl font-bold mb-4">Admin Dashboard</h2>
//         <div className="grid grid-cols-2 gap-4 mb-4">
//           <div className="border p-2 bg-white rounded">
//             <h3 className="font-bold">Total Users</h3>
//             <p className="text-2xl text-center">1,234</p>
//           </div>
//           <div className="border p-2 bg-white rounded">
//             <h3 className="font-bold">Active Sessions</h3>
//             <p className="text-2xl text-center">78</p>
//           </div>
//         </div>
//         <div className="border p-2 bg-white rounded mb-4">
//           <h3 className="font-bold mb-2">Chatbot Performance</h3>
//           <p>Avg. Response Time: 1.5s</p>
//           <p>Query Resolution Rate: 85%</p>
//         </div>
//         <div className="flex justify-between">
//           <button className="bg-blue-500 text-white p-2 rounded flex items-center">
//             <Search size={20} className="mr-2" /> View Logs
//           </button>
//           <button className="bg-green-500 text-white p-2 rounded flex items-center">
//             <Settings size={20} className="mr-2" /> System Settings
//           </button>
//         </div>
//       </div>
//     )
//   }
// ];

// const WireframeViewer = () => {
//   const [currentIndex, setCurrentIndex] = useState(0);

//   const nextWireframe = () => {
//     setCurrentIndex((prevIndex) => (prevIndex + 1) % wireframes.length);
//   };

//   const prevWireframe = () => {
//     setCurrentIndex((prevIndex) => (prevIndex - 1 + wireframes.length) % wireframes.length);
//   };

//   return (
//     <div className="max-w-lg mx-auto">
//       <h1 className="text-2xl font-bold mb-4 text-center">ERP Chatbot Wireframes</h1>
//       <div className="mb-4">
//         <h2 className="text-xl font-semibold mb-2">{wireframes[currentIndex].title}</h2>
//         {wireframes[currentIndex].content}
//       </div>
//       <div className="flex justify-between">
//         <button onClick={prevWireframe} className="bg-blue-500 text-white p-2 rounded flex items-center">
//           <ChevronLeft size={20} /> Previous
//         </button>
//         <button onClick={nextWireframe} className="bg-blue-500 text-white p-2 rounded flex items-center">
//           Next <ChevronRight size={20} />
//         </button>
//       </div>
//     </div>
//   );
// };

// export default WireframeViewer;