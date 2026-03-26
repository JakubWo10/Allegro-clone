import './index.css';
import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import HomePage from './HomePage'
import ProtectedRoutes from './ProtectedRoutes'
import { AuthProvider } from './ContextAPI'
import RegisterPage from './RegisterPage';
import LoginPage from './LoginPage';
import { GoogleOAuthProvider } from '@react-oauth/google';
import ProfilPage from './ProfilPage';
import ProductPage from './ProductPage';
import CreateProduct from './CreateProduct';

function App() {

  return (
    <Router>
      <GoogleOAuthProvider clientId=''>
    <AuthProvider>
      <Routes>
        <Route path="/register" element={<RegisterPage/>} />
        <Route path="/login" element={<LoginPage/>} />
        <Route path="/" element={<HomePage/>} />
        <Route path="/product/:id" element={<ProductPage/>} />
        <Route element={<ProtectedRoutes/>}>
          <Route path="/Profil" element={<ProfilPage/>} />
          <Route path="/CreateProduct" element={<CreateProduct/>} />

        </Route>
      </Routes>

   </AuthProvider>
   </GoogleOAuthProvider>
   </Router>
  )
}

export default App
