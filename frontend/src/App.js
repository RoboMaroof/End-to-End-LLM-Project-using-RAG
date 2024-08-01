import React, { useState } from 'react';
import DocumentUpload from './components/DocumentUpload';
import SearchInput from './components/SearchInput';
import SearchResult from './components/SearchResult';

const App = () => {
  const [result, setResult] = useState('');

  const handleSearch = async (query) => {
    const response = await fetch(`/search?query=${query}`);
    const data = await response.json();
    setResult(data.summary);
  };

  return (
    <div>
      <h1>Document Search and Summarization</h1>
      <DocumentUpload />
      <SearchInput onSearch={handleSearch} />
      <SearchResult result={result} />
    </div>
  );
};

export default App;
