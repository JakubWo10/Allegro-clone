import './index.css';
import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import HomePage from './HomePage'
import ProtectedRoutes from './ProtectedRoutes'
import { AuthProvider } from './ContextAPI'
import RegisterPage from './RegisterPage';
import LoginPage from './LoginPage';
import ProfilPage from './ProfilPage';
import ProductPage from './ProductPage';
import CreateProduct from './CreateProduct';
import Navbar from './Components/Navbar';

function App() {

  return (
    <Router>
    <AuthProvider>
      <Navbar/>
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
    </Router>
  )
}

export default App
