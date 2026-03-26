import { createContext, useState } from "react";
import { ReactNode } from "react";

interface authData {
    user_id: string | null;
    name: string | null;
    email: string | null;
    token: string | null;
    image_url: string | null;
}


interface AuthContextType {
    auth: authData
    setAuth: (auth: authData) => void
}

interface AuthProviderProps {
    children: ReactNode
}




export const AuthContext = createContext<AuthContextType>({
    auth: { user_id: null, name: null, email: null, token: null, image_url: null},
    setAuth: () => {}
})

export const AuthProvider = ({children}: AuthProviderProps) => {
    const [auth, setAuth] = useState(() => ({
        user_id: localStorage.getItem("user_id"),
        name: localStorage.getItem("name"),
        token: localStorage.getItem("token"),
        email: localStorage.getItem("email"),
        image_url: localStorage.getItem("image_url")

    }))

    return (
        <AuthContext.Provider value={{ auth, setAuth }}>
            {children}
        </AuthContext.Provider>

    )
}
