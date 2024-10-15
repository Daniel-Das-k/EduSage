import React, { createContext, useState, useEffect } from 'react';
import run from '../config/gemini';

export const Context = createContext();

const ContextProvider = (props) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [visible, setVisible] = useState(true);
  const [resultContainer, setResultContainer] = useState([]);
  const [newPage, setNewPage] = useState(true);
  const [loading, setLoading] = useState(false);
  const [prevPrompts, setPrevPrompts] = useState([]);
  const [history, setHistory] = useState(true);
  const [username, setUsername] = useState(() => localStorage.getItem('username') || '');
  const [photo, setPhoto] = useState(() => localStorage.getItem('photo') || '');

  const generate = async (prompt) => {
    const response = await run(prompt);
    return response;
  };

  useEffect(() => {
    if (username) {
      localStorage.setItem('username', username);
    } else {
      localStorage.removeItem('username');
    }
  }, [username]);

  useEffect(() => {
    if (photo) {
      localStorage.setItem('photo', photo);
    } else {
      localStorage.removeItem('photo');
    }
  }, [photo]);
  
  // useEffect(()=>{
  //   if(prevPrompts){
  //     localStorage.setItem('prompts',prevPrompts)
  //   }
  //   else{
  //     localStorage.removeItem('prompts');
  //   }
  // },[prevPrompts])
  const contextValue = {
    input,
    messages,
    setInput,
    setMessages,
    visible,
    setVisible,
    generate,
    resultContainer,
    setResultContainer,
    loading,
    setLoading,
    newPage,
    setNewPage,
    prevPrompts,
    setPrevPrompts,
    history,
    setHistory,
    username,
    setUsername,
    photo,
    setPhoto,
  };

  return (
    <Context.Provider value={contextValue}>
      {props.children}
    </Context.Provider>
  );
};

export default ContextProvider;
