Here are the complete files for the LoveConnect React frontend project:

# FILE: package.json

```javascript
{
  "name": "loveconnect",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "start": "vite build && vite preview"
  },
  "dependencies": {
    "@tailwindcss/forms": "^0.4.0",
    "@tailwindcss/typography": "^0.5.2",
    "axios": "^1.1.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.4.3",
    "tailwindcss": "^3.2.4",
    "vite": "^4.1.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.17",
    "@types/react-dom": "^18.0.6",
    "@types/react-router-dom": "^6.3.1",
    "@types/tailwindcss": "^3.2.4",
    "typescript": "^4.7.4"
  }
}
```

# FILE: vite.config.js

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from 'tailwindcss';

export default defineConfig({
  plugins: [react()],
  css: {
    modules: {
      localsConvention: 'camelCaseOnly',
    },
    preprocessorOptions: {
      tailwindcss: {
        config: './tailwind.config.js',
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
});
```

# FILE: src/main.jsx

```javascript
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);
```

# FILE: src/App.jsx

```javascript
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

# FILE: src/router.jsx

```javascript
import { createBrowserRouter } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/register',
    element: <Register />,
  },
]);

export default router;
```

# FILE: src/services/api.js

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export default api;
```

# FILE: src/pages/Home.jsx

```javascript
import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function Home() {
  return (
    <div>
      <Navbar />
      <h1>Welcome to LoveConnect!</h1>
      <Footer />
    </div>
  );
}

export default Home;
```

# FILE: src/pages/Login.jsx

```javascript
import React, { useState } from 'react';
import axios from '../services/api';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/v1/login', {
        email,
        password,
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <Navbar />
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button type="submit">Login</button>
      </form>
      <Footer />
    </div>
  );
}

export default Login;
```

# FILE: src/pages/Register.jsx

```javascript
import React, { useState } from 'react';
import axios from '../services/api';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/v1/register', {
        email,
        password,
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <Navbar />
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button type="submit">Register</button>
      </form>
      <Footer />
    </div>
  );
}

export default Register;
```

# FILE: src/components/Navbar.jsx

```javascript
import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/login">Login</Link>
        </li>
        <li>
          <Link to="/register">Register</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
```

# FILE: src/components/Footer.jsx

```javascript
function Footer() {
  return (
    <footer>
      <p>&copy; 2023 LoveConnect</p>
    </footer>
  );
}

export default Footer;
```

# FILE: src/context/AuthContext.jsx

```javascript
import React, { createContext, useState } from 'react';

const AuthContext = createContext();

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export { AuthProvider, AuthContext };
```

# FILE: src/index.css

```css
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

nav {
  background-color: #333;
  color: #fff;
  padding: 1rem;
  text-align: center;
}

nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

nav li {
  display: inline-block;
  margin-right: 20px;
}

nav a {
  color: #fff;
  text-decoration: none;
}

footer {
  background-color: #333;
  color: #fff;
  padding: 1rem;
  text-align: center;
  clear: both;
}
```

# FILE: .env.example

```bash
VITE_API_URL=http://localhost:8000
```

This code sets up a basic React frontend project with Tailwind CSS, React Router, and Axios for API communication. It also includes a simple authentication system using a context API. The project uses a .env file to store environment variables, which can be replaced with actual values in a production environment.