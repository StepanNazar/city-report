import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import USER_INFO from './Store/store';

// Створення інстансу класу USER_INFO
const USER = new USER_INFO();

// Створення контексту
export const UserContext = React.createContext(); 

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <UserContext.Provider value={{ USER }}>
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </UserContext.Provider>
);


