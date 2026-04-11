import { useContext } from "react"
import { useNavigate } from "react-router-dom"
import { AuthContext } from "../ContextAPI"






function Navbar() {

    const navigate = useNavigate()

    const { auth } = useContext(AuthContext)

    return (

        <div className="w-full h-14 z-50 overflow-x-hidden">
            <div className="flex bg-gradient-to-l from-yellow-400 to-green-400 w-full h-14  shadow-gray-700 flex-row gap-15 justify-between px-3">
                <div className='flex text-center gap-2'>
                    <p className="flex py-2 text-white font-bold text-2xl italic cursor-default cursor-pointer" onClick={() => navigate("/")}>Sklepik</p>
                </div>
                <div className='flex flex-row flex-start  '>
                    <button className="h-full px-4 text-white font-bold uppercase text-xs tracking-wider transition-all duration-50 hover:text-black hover:bg-indigo-900/10 hover:border-b-4 hover:border-green-500 hover:text-white  "> Puste pole </button>
                    <button className="h-full px-4 text-white font-bold uppercase text-xs tracking-wider transition-all duration-50 hover:text-black hover:bg-indigo-900/10 hover:border-b-4 hover:border-green-500 hover:text-white "> wiadomosci </button>
                    <button className="h-full px-4 text-white font-bold uppercase text-xs tracking-wider transition-all duration-50 hover:text-black hover:bg-indigo-900/10 hover:border-b-4 hover:border-green-500 hover:text-white " > Koszyk </button>
                    {auth.token ?
                    <button onClick={() => navigate("/Profil")} className="h-full px-4 text-white font-bold uppercase text-xs tracking-wider transition-all
                    duration-50 hover:text-black hover:bg-indigo-900/10 hover:border-b-4 hover:border-green-500 hover:text-white "> Profil </button>:
                    <button onClick = {() => navigate("/login")} className="h-full px-4 text-white font-bold uppercase text-xs tracking-wider transition-all
                     duration-50 hover:text-black hover:bg-indigo-900/10 hover:border-b-4 hover:border-green-500 hover:text-white "> Zaloguj sie</button>
                    }
                </div>
            </div>
        </div>
    )
}

export default Navbar
