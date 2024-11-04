// src/ui/ProgressRing.jsx
import React from 'react';
import styled from 'styled-components';
import { useSpring, animated } from '@react-spring/web';

const Circle = styled(animated.circle)`
  fill: none;
  stroke-width: ${(props) => props.strokeWidth || 20}; // Allow dynamic stroke width
`;

const SvgWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: ${(props) => props.size || '150px'}; // Allow dynamic size
  height: ${(props) => props.size || '150px'}; // Allow dynamic size
`;

const PercentageText = styled.text`
  font-size: ${(props) => props.fontSize || '1.5rem'};
  fill: #4a90e2; // Color of the percentage text
  dominant-baseline: middle;
  text-anchor: middle;
`;

const ProgressRing = ({ progress, size = 150, strokeWidth = 20 }) => {
  const radius = (size - strokeWidth) / 2; // Adjust radius based on size and strokeWidth
  const circumference = 2 * Math.PI * radius;

  // Calculate progress in percentage, making sure it does not exceed 100
  const progressPercentage = Math.min(progress * 7, 100); // Multiply by 7 and cap at 100%

  const animationProps = useSpring({
    strokeDashoffset: circumference - (progressPercentage / 100) * circumference,
    config: { duration: 1000 },
  });

  return (
    <SvgWrapper size={size}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <Circle
          stroke="#e6e6e6" // Background color of the ring
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
        />
        <Circle
          style={{ strokeDasharray: circumference, strokeDashoffset: animationProps.strokeDashoffset }}
          stroke="#4a90e2" // Progress color
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
        />
        <PercentageText
          x={size / 2}
          y={size / 2}
          fontSize={(size / 6) + 'px'} // Adjust font size dynamically
        >
          {Math.round(progressPercentage)}%
        </PercentageText>
      </svg>
    </SvgWrapper>
  );
};

export default ProgressRing;
