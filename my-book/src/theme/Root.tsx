import React, { useEffect, useState } from 'react';
import OriginalRoot from '@theme-original/Root';
import Chatbot from '../components/Chatbot';

export default function Root(props: any): JSX.Element {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <>
      <OriginalRoot {...props} />
      {mounted && <Chatbot />}
    </>
  );
}
