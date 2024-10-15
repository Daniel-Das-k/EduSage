import React from 'react';
import styled, { keyframes } from 'styled-components';
import { Content } from './Home';
import flutter from '../assets/flutter.jpg'
import block from '../assets/block.jpeg';
import django from '../assets/django.jpg';
import ProgressRing from '../ui/ProgressRing';
import { useNavigate } from 'react-router-dom';
// Define keyframes for the gradient animation
const gradientAnimation = keyframes`
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
`;

// Create a styled div for the gradient background
const Container = styled.div`
  height: 100vh;
  display: flex;
  padding:1rem;
//   background: linear-gradient(45deg, #000000, #0000FF);
//   background: linear-gradient(45deg, #009999, #004D4D);
//   background: linear-gradient(45deg, #000000, #ffffff);
  // background: linear-gradient(135deg, #3a5da8, #2a406c); 
  background: linear-gradient(45deg, #004D4D, #009999);
  
 


  background-size: 200% 200%;
  animation: ${gradientAnimation} 5s ease infinite;
`;
const H1=styled.h1`
color: white;
  font-weight: bold;
  letter-spacing:2px;
  font-size: 1.2rem;
  
`
const LearningContainer=styled.div`
margin-top:1rem;
display: flex;
gap:2rem;
// justify-content: space-between;
width:98vw;
`
// const CourseContainer=styled.div`
// border:1px solid #009999;
// width:350px;
// padding:1rem;
// display:flex;
// flex-direction: column;
// justify-content: space-between;
// border-radius:10px;
// background: linear-gradient(45deg, #4682b4, #1e3a8a);


// margin-bottom:1rem;
// box-sizing: border-box;
// // box-shadow:0 0 10px 1px #fff;
// &:hover{
//   box-shadow:0 0 10px 1px #fff;
//   transition: box-shadow 0.5s ease;}
// cursor:pointer;
//   `
const CourseContainer = styled.div`
  border: 1px solid rgba(255, 255, 255, 0.2); /* Subtle border */
  width: 350px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 10px;
//  border:1px solid #fff;

  background: rgba(255, 255, 255, 0.1); /* Semi-transparent background */
  backdrop-filter: blur(10px); /* Blur effect for glass effect */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  margin-bottom: 1rem;
  box-sizing: border-box;
  
  /* Gradient border to match glass effect */
//   background: linear-gradient(45deg, rgba(70, 130, 180, 0.5), rgba(30, 58, 138, 0.5));
  
  /* Hover effect */
  &:hover {
    box-shadow: 0 0 15px 2px rgba(255, 255, 255, 0.6); /* Soft white glow on hover */
    transition: box-shadow 0.5s ease;
  }
  cursor: pointer;
`;


const SubH1=styled.h1`
font-size:1rem;
font-weight:450;
margin:1rem 0;
; 

`
const Img=styled.img`
border-radius:10px;
width:400px;
height:200px;
`
const P=styled.p`
margin-bottom:0.5rem;
font-size:15px;
font-weight:300;
`
const H2=styled.h2`
font-size:23px;
`
const CategoriesContainer=styled.div`


`
// const SubCategoryContainer=styled.div`
// margin-top:1rem;
// display:flex;
// flex-direction:row;
// justify-content:space-between;
// padding:0.5rem 1rem;
// border-radius:10px;
// // background:#33B2B2;
//  border:1px solid #fff;
// margin-bottom:1rem;
// box-sizing: border-box;
// width:350px;
// &:hover{
//   box-shadow:0 0 10px 1px #fff;
//   transition: box-shadow 0.5s ease;}
// cursor:pointer;
// `
const SubCategoryContainer = styled.div`
  margin-top: 1rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1); /* Semi-transparent background */
  backdrop-filter: blur(10px); /* Blur effect for glass effect */
  border: 1px solid rgba(255, 255, 255, 0.2); /* Subtle border */
  margin-bottom: 1rem;
  box-sizing: border-box;
  width: 350px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */

  &:hover {
    box-shadow: 0 0 15px 2px rgba(255, 255, 255, 0.6); /* Soft white glow on hover */
    transition: box-shadow 0.5s ease;
  }

  cursor: pointer;
`;

const ProgressContainer=styled.div`

`
const Course = ({title,count})=>{
    return (
        <SubCategoryContainer>
            <SubH1>{title}</SubH1>
            <SubH1>-</SubH1>
            <SubH1>{count} courses</SubH1>
            
        </SubCategoryContainer>
    )
}
export const ContentContainer = ({style,img,title,description,instructorName,name})=>{
    const navigate=useNavigate();
    return(

        <CourseContainer onClick={()=>navigate(`/${name}`)}>
            <Img style={style} src={img}/>
            <SubH1>{title}</SubH1>
            <P>{description}</P>
            {/* <H2>Instructor :</H2>
            <P> {instructorName}</P> */}
    </CourseContainer>
    )
    
}
const Learning = () => {
    const navigate=useNavigate();
  return (
    <Container>
    <div>
      <H1>Popular Courses</H1>
      <LearningContainer>
        <ContentContainer 
        name={"flutter"}
        img={flutter}
        title={"Flutter & Dart - The Complete Guide"} 
        description={"Master Flutter and Dart to build cross-platform mobile apps, covering UI design and performance optimization"} 
        instructorName={"Maximillian Schwarmilliar"}/>
        <ContentContainer 
        name={"django"}
        img={django}
        title={"Mastering Django for Web Development"}
        description={"Master Django for web development, authentication and deployment for building dynamicwebsites"}
        // instructorName={"Jose Portilla"}
        />
        
        <ContentContainer
        name={"block"}
        
        img={block}
        title={"Blockchain Development on Ethereum"}
        description={"Master blockchain development on Ethereum, covering smart contracts, Solidity on Ethereum network."}
        // instructorName={"Stephen Grider"}
        />
        <ContentContainer 
         
        img={flutter}
        title={"Flutter & Dart - The Complete Guide"} 
        description={"Master Flutter and Dart to build cross-platform mobile apps, covering UI design and performance optimization"} 
        instructorName={"Maximillian Schwarmilliar"}/>
        
        
      </LearningContainer>
      <CategoriesContainer>
        <H1>Categories for Learning</H1>
        <div style={{display:"flex",gap:"2rem"}}>
        <Course title={"Mobile Development"} count="15"/>
        <Course title={"Web Development"} count="20"/>
        <Course  title={"BlockChain"} count="10"/>
        <Course title={"Machine Learning"} count="12"/>
        
        
        </div>
        
      </CategoriesContainer>
      <ProgressContainer>
        <H1>My Learning Progress</H1>
        <div style={{display:"flex",alignItems:"center",gap:"2rem",marginLeft:"0.3rem"}}>
            <P style={{fontWeight:"450"}}>Flutter & Dart - The Complete Guide</P>
            <ProgressRing size={100} progress={12} strokeWidth={15} />
            <P style={{fontWeight:"450"}}> Mastering Django for Web Development</P>
            <ProgressRing size={100} progress={10} strokeWidth={15} />
            <P style={{fontWeight:"450"}}> Blockchain Development on Ethereum</P>
            <ProgressRing size={100} progress={9} strokeWidth={15} />
        </div>
        {/* <ProgressRing size={100} progress={11} strokeWidth={15} />
        <ProgressRing size={100} progress={11} strokeWidth={15} />
        <ProgressRing size={100} progress={11} strokeWidth={15} />
        <ProgressRing size={100} progress={11} strokeWidth={15} /> */}
      </ProgressContainer>
    </div>
    </Container>
  );
};

export default Learning;
