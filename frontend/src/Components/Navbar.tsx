
import { useNavigate } from "react-router-dom"






function Navbar() {

    const navigate = useNavigate()

    return (

        <div className="flex flex-col h-screen w-full">
            <div className="flex bg-gradient-to-l from-yellow-400 to-green-400 w-full h-14 shadow-lg shadow-gray-700 flex-row gap-15 justify-between px-3">
                <div className='flex text-center gap-2'>
                    <p className="flex py-2 text-white font-bold text-2xl italic cursor-default">Sklepik</p>
                </div>
                <div className='flex flex-row flex-start  '>
                    <button className="h-full px-4 text-white font-bold uppercase text-xs tracking-wider transition-all duration-50 hover:text-black hover:bg-indigo-900/10 hover:border-b-4 hover:border-green-500 hover:text-white  "> Puste pole </button>
                    <button className="h-full px-4 text-white font-bold uppercase text-xs tracking-wider transition-all duration-50 hover:text-black hover:bg-indigo-900/10 hover:border-b-4 hover:border-green-500 hover:text-white "> wiadomosci </button>
                    <button className="h-full px-4 text-white font-bold uppercase text-xs tracking-wider transition-all duration-50 hover:text-black hover:bg-indigo-900/10 hover:border-b-4 hover:border-green-500 hover:text-white " > Koszyk </button>
                    {true ?
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
