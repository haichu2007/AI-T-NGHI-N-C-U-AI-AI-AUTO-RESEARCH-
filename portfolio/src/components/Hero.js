import React from 'react';
import { motion } from 'framer-motion';

const Hero = () => {
  return (
    <section id="hero" className="hero">
      <motion.div 
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="hero-content"
      >
        <h1>Welcome to My Portfolio</h1>
        <p>A beautiful scrolling experience</p>
      </motion.div>
    </section>
  );
};

export default Hero;