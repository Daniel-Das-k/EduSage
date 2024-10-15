import React from 'react'
import { useContext } from 'react';
import styled from 'styled-components'
import { Context } from '../context/Context';
const InputBox = styled.input`
  padding: 1rem;
  width: 50%;
  border-radius: 30px;
  margin: 2rem 1rem;
  // background: linear-gradient(45deg, #004D4D, #009999);
  background:#000;
  border:1px solid rgba(255, 255, 255, 0.2);
  outline:none;
  
  
  
  
`;

const Input = ({type,placeholder,name,style,value,onChange,onKeyPress,className}) => {
  return (
    <InputBox
        type={type}
        placeholder={placeholder}
        name={name}
        value={value}
        onChange={onChange}
        onKeyPress={onKeyPress}
        style={style}
        className={className}
         
          />
  )
}

export default Input;
