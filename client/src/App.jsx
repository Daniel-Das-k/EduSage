import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import styled from 'styled-components'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import Automation from './subpages/Automation'
import Summarization from './subpages/Summarization'
import CheckList from './subpages/CheckList.jsx'
// import Email from './subpages/Email.jsx';
import TextSum from './subpages/TextSum.jsx'
import Image from './subpages/Image.jsx'
import TodoList from './subpages/To-Do-List.jsx'
import Video from './pages/Video.jsx'
import Learning from './pages/Learning'
import Flutter from './subpages/Flutter.jsx'

const App = () => {

  return (<>
   <BrowserRouter>
   <Routes>
    <Route index element={<Login/>}/>
    <Route path='/Register' element={<Register/>}/>
    <Route path='/Home' element={<Home/>}/>
    <Route path='/Automation' element={<Automation/>}/>
    <Route path='/Youtube Summarizer' element={<Summarization/>}/>
    <Route path='/Translator' element={<Video/>}/>
    {/* <Route path='/Email' element={<Email/>}/> */}
    <Route path='/Text' element={<TextSum/>}/>
    <Route path='/image' element={<Image/>}/>
    <Route path='/ToDoList' element={<TodoList/>}/>
    <Route path='/Video' element={<Video/>}/>
    <Route path='/Learning' element={<Learning/>}/>
    <Route path='/flutter' element={<Flutter/>}/>
    
    </Routes>
    </BrowserRouter>
  </>
   
  )
}

export default App

