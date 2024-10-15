// src/components/TodoList.jsx
import React, { useState } from "react";
import styled, { keyframes } from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import { PlaceholdersAndVanishInput } from "../ui/placeholders-and-vanish-input.jsx";
import ProgressRing from "../ui/ProgressRing.jsx";

// Gradient Animation
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

// Styled components
const TodoContainer = styled.div`
  // background: linear-gradient(135deg, #3a5da8, #2a406c); /* Subtle dark blue gradient */
  background: linear-gradient(45deg, #004D4D, #009999);
  
  background-size: 200% 200%;
  animation: ${gradientAnimation} 15s ease infinite;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;  
  align-items: center;
  padding: 20px;
`;

const TodoTitle = styled(motion.h1)`
  font-size: 2.5rem;
  color: #fff;
  margin-bottom: 20px;
`;

const TodoInputContainer = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 20px;
`;

const AddButton = styled.button`
  padding: 5px;
  font-size: 1rem;
  background-color: #ffffff;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  color: #242424;
  width: 150px;
  height: 50px;
  margin-left: 1rem;

  &:hover {
    background-color: #242424;
    color: #fff;
  }
`;

const TaskList = styled.ul`
  list-style-type: none;
  padding: 0;
  width: 350px;
`;

const TaskItem = styled(motion.li)`
  background-color: rgba(255, 255, 255, 0.8);
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
  color: #242424;

  &.completed {
    background-color: rgba(144, 238, 144, 0.8); /* Light green background for completed tasks */
  }

  .task-text {
    text-decoration: ${(props) => (props.completed ? "line-through" : "none")};
    color: ${(props) => (props.completed ? "#888" : "#242424")};
  }

  &:hover {
    background-color: rgba(255, 255, 255, 1);
  }
`;

const TaskText = styled.span`
  font-size: 1rem;
  flex-grow: 1;
  margin-right: 10px;
`;

const DeleteButton = styled.button`
  background-color: transparent;
  border: none;
  font-size: 1.2rem;
  color: #e74c3c;
  cursor: pointer;
  transition: color 0.3s ease;

  &:hover {
    color: #c0392b;
  }
`;

const Checkbox = styled.input`
  margin-right: 10px;
  transform: scale(1.5);
  cursor: pointer;
`;

// Component logic
const TodoList = () => {
  const [tasks, setTasks] = useState([]);
  const [input, setInput] = useState("");

  const handleAddTask = () => {
    if (input.trim()) {
      setTasks([...tasks, { id: Date.now(), text: input, completed: false }]);
      setInput("");
    }
  };

  const handleDeleteTask = (id) => {
    setTasks(tasks.filter((task) => task.id !== id));
  };

  const handleToggleTask = (id) => {
    setTasks(
      tasks.map((task) =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );
  };

  // Calculate progress
  const completedTasks = tasks.filter((task) => task.completed).length;
  const progress = tasks.length ? completedTasks : 0; // Each task completed contributes to progress

  const placeholders = [
    "What's the first rule of Fight Club?",
    "Who is Tyler Durden?",
    "Where is Andrew Laeddis Hiding?",
    "Write a Javascript method to reverse a string",
    "How to assemble your own PC?",
  ];

  return (
    <TodoContainer>
      <div
        style={{
          display: "flex",
          gap: "20rem",
          width: "100%",
          marginTop: "1rem"
        }}
      >
        <div>
          <TodoTitle
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
            className="text-center mr-24"
          >
            To-Do List
          </TodoTitle>

          <TodoInputContainer>
            <PlaceholdersAndVanishInput
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholders={placeholders}
              onSubmit={handleAddTask}
            />
            <AddButton onClick={handleAddTask}>Add Task</AddButton>
          </TodoInputContainer>
          <TaskList>
            <AnimatePresence>
              {tasks.map((task) => (
                <TaskItem
                  key={task.id}
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 50 }}
                  className={task.completed ? "completed" : ""}
                  onClick={() => handleToggleTask(task.id)}
                >
                  <Checkbox
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => handleToggleTask(task.id)}
                  />
                  <TaskText className="task-text">{task.text}</TaskText>
                  <DeleteButton
                    onClick={(e) => {
                      e.stopPropagation(); // Prevent event propagation to TaskItem
                      handleDeleteTask(task.id);
                    }}
                  >
                    ×
                  </DeleteButton>
                </TaskItem>
              ))}
            </AnimatePresence>
          </TaskList>
        </div>

    <div style={{marginTop:"3rem"}}>
      <TodoTitle style={{marginLeft:"7.5rem"}}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        Progress Bar
      </TodoTitle>
      <ProgressRing size={500} progress={progress} strokeWidth={30} />
      </div>
      </div>
    </TodoContainer>
  );
};

export default TodoList;
