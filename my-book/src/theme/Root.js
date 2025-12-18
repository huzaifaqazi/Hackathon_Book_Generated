import React from 'react';
import OriginalRoot from '@docusaurus/theme-classic/lib/theme/Root';
import Chatbot from '../components/Chatbot';

function Root(props) {
  return (
    <>
      <OriginalRoot {...props} />
      <Chatbot />
    </>
  );
}

export default Root;
