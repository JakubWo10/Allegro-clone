import { Outlet, Navigate } from "react-router-dom";


const ProtectedRoutes = () => {
    const token = localStorage.getItem("token")

    if (!token)
    {
        return <Navigate to="/" replace/>
    }
    return <Outlet/>
}

export default ProtectedRoutes
