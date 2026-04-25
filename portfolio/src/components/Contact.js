import React from 'react';
import { motion } from 'framer-motion';

const Contact = () => {
  return (
    <section id="contact" className="contact">
      <motion.div 
        initial={{ opacity: 0, x: 50 }}
        whileInView={{ opacity: 1, x: 0 }}
        transition={{ duration: 1 }}
      >
        <h2>Contact Me</h2>
        <p>Email: your.email@example.com</p>
        <p>Phone: +123 456 7890</p>
      </motion.div>
    </section>
  );
};

export default Contact;