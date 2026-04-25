import React from 'react';
import { motion } from 'framer-motion';

const Projects = () => {
  return (
    <section id="projects" className="projects">
      <motion.div 
        initial={{ opacity: 0, scale: 0.8 }}
        whileInView={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1 }}
      >
        <h2>My Projects</h2>
        <p>Project 1: Description</p>
        <p>Project 2: Description</p>
        <p>Project 3: Description</p>
      </motion.div>
    </section>
  );
};

export default Projects;