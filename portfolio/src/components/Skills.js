import React from 'react';
import { motion } from 'framer-motion';

const Skills = () => {
  return (
    <section id="skills" className="skills">
      <motion.div 
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        <h2>Skills</h2>
        <ul>
          <li>React</li>
          <li>JavaScript</li>
          <li>CSS</li>
          <li>HTML</li>
        </ul>
      </motion.div>
    </section>
  );
};

export default Skills;