import { useState } from "react"
import { useNavigate } from "react-router-dom"







function RegisterPage() {
    const [name, setName] = useState("")
    const [password, setPassowrd] = useState("")
    const [repated_password, setRepeatedPassword] = useState("")
    const [email, setEmail] = useState("")
    const [error, setError] = useState<false | string>("")
    const [information, setInformation] = useState<false | string>(false)
    const navigate = useNavigate()


    async function registerFetch()
    {
        if (!name.trim() || !password.trim() || !repated_password.trim() || !email.trim() )
        {
            setName("")
            setPassowrd("")
            setRepeatedPassword("")
            setEmail("")

            setError("Wszyskie pola rejestracji musza byc wypełnione")
            setInformation(false)
            return
        }
        if( password !== repated_password)
        {
            setError("Dwa rozne hasla")
            return

        }
        try {
        const response = await fetch("http://127.0.0.1:8000/register",
            {
                method: "POST",
                headers: {"content-type": "application/json"},
                body:  JSON.stringify({
                    name: name,
                    password: password,
                    email: email
                })
            }
        )
        if (!response.ok)
        {
            const errorResponse = await response.json()
            const error_name = errorResponse.detail[0].msg

            setError(error_name)
            return
        }
        const data = await response.json()
        const information = data.detail
        setInformation(information)
        }
        catch(err: any) {
            setError(err.message || "Błąd połączenia z serwerem")
        }

        setName("")
        setPassowrd("")
        setRepeatedPassword("")
        setEmail("")
    }





    return (
        <>
            <div className="flex items-center justify-center bg-gray-200 w-screen h-screen">
                <div className="flex flex-col items-center justify-center w-[650px] h-[500px] shadow-md shadow-black bg-white rounded-xl gap-4">
                        <h1 className="flex items-start justify-start font-bold text-3xl font-sans antialiased lining-nums"> Zarejestruj sie </h1>
                    {error && <h1 className="flex items-center justify-center bg-red-500 px-6 py-3 min-w-[200px] max-w-[90%] tranistion-all text-center text-white rounded-xl"> {error} </h1>}
                    {information && <h1> {information} </h1>}
                    <input value = {name} onChange= {(e) => setName(e.target.value)} placeholder="nazwa" className="border-1 border-black rounded-md"/>
                    <input value = {email} onChange= {(e) => setEmail(e.target.value)} placeholder="email" className="border-1 border-black rounded-md"/>
                    <input type = "password"  placeholder= "haslo" value = {password} onChange={(e) => setPassowrd(e.target.value)} className="border-1 border-black rounded-md"/>
                    <input type = "password" value = {repated_password} onChange= {(e) => setRepeatedPassword(e.target.value)} placeholder="powtorz haslo" className="border-1 border-black rounded-md"/>


                    <button onClick={registerFetch} className="text-lg flex items-center justify-center border-yellow-300 border-3 text-green-300
                        bg-yellow-300 text-white rounded-xl w-35 h-15 cursor-pointer hover:bg-green-500 hover:border-green-500 transition-colors duration-100 active:scale-95 "> Zarejestruj sie </button>
                            <span> Masz juz konto?  </span>
                            <button className="text-lg flex items-center justify-center border-blue-500 border-3
                        bg-blue-500 text-white rounded-xl w-35 h-15 cursor-pointer hover:bg-green-500 hover:border-green-500 transition-colors duration-100 active:scale-95" onClick={() => (navigate("/login"))}> Zaloguj sie </button>

                </div>


            </div>
        </>


    )
}






export default RegisterPage
