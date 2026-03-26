import { useContext, useState } from "react"
import { useNavigate } from "react-router-dom"

import { GoogleLogin } from '@react-oauth/google';
import { AuthContext } from "./ContextAPI";





function LoginPage() {
    const [name, setName] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState<false | string>("")
    const [information, setInformation] = useState<false | string>(false)
    const navigate = useNavigate()

    const {auth, setAuth} = useContext(AuthContext)

    async function loginFetch()
    {
        if (!name.trim() || !password.trim() )
        {
            setName("")
            setPassword("")
            setError("Wszyskie pola musza byc wypełnione")
            setInformation(false)
            return
        }

      const form_data = new URLSearchParams()


      try {
        form_data.append("username", name)
        form_data.append("password", password)
        const response = await fetch("http://127.0.0.1:8000/login",
            {
                method: "POST",
                headers: {"content-type": "application/x-www-form-urlencoded"},
                body:  form_data
            }
        )
        const data = await response.json()
        if (!response.ok) {
            throw new Error(data.detail || "Błędny login lub hasło");
        }

        const information = data.detail
        setInformation(information)
        setError(false)
        localStorage.setItem("token",data.access_token)
        localStorage.setItem("name", name)

        setAuth({
            user_id: data.user_id,
            token: data.access_token,
            name: localStorage.getItem("name"),
            email: data.user_email,
            image_url: data.image_source
        })

        navigate("/")
        } catch(err: any) {
            setError(err.message || "Wystąpił błąd")
        }
    }



    return (
        <>
            <div className="flex items-center justify-center bg-gray-200 w-screen h-screen">
                <div className="flex flex-col items-center justify-center w-[650px] h-[500px] shadow-md shadow-black bg-white rounded-xl gap-4">
                        <h1 className="flex items-start justify-start font-bold text-3xl font-sans antialiased lining-nums"> Zaloguj sie </h1>
                    {error && <h1 className="flex items-center justify-center bg-red-500 px-6 py-3 min-w-[200px] max-w-[90%] tranistion-all text-center text-white rounded-xl"> {error} </h1>}
                    {information && <h1> {information} </h1>}
                    <input value = {name} onChange= {(e) => setName(e.target.value)} placeholder="nazwa" className="border-1 border-black rounded-md"/>
                    <input type = "password" value = {password} onChange= {(e) => setPassword(e.target.value)} placeholder="haslo" className="border-1 border-black rounded-md"/>



                    <button onClick={loginFetch} className="text-lg flex items-center justify-center border-yellow-300 border-3 text-green-300
                        bg-yellow-300 text-white rounded-xl w-35 h-15 cursor-pointer hover:bg-green-500 hover:border-green-500 transition-colors duration-100 active:scale-95 "> Zaloguj  </button>
                            <span> Nie masz konta?  </span>
                            <button className="text-lg flex items-center justify-center border-blue-500 border-3
                        bg-blue-500 text-white rounded-xl w-35 h-15 cursor-pointer hover:bg-green-500 hover:border-green-500 transition-colors duration-100 active:scale-95" onClick={() => (navigate("/register"))}> Zarejestruj sie </button>

                        <button className="text-lg flex items-center justify-center border-blue-500 border-3
                        bg-blue-500 text-white rounded-xl w-35 h-15 cursor-pointer hover:bg-green-500 hover:border-green-500 transition-colors duration-100 active:scale-95" onClick={() => (navigate("/"))}> Strona głowna </button>

                </div>


            </div>
        </>


    )
}






export default LoginPage
