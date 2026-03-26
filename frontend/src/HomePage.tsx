import './index.css'
import { useNavigate } from 'react-router-dom'
import { useContext, useEffect, useState } from 'react'
import SearchTile from './Components/SearchTile'
import Categories from './Components/Categories'
import { AuthContext } from './ContextAPI'
import Products from './Components/Products'
import { Product } from './Components/Products'

function HomePage(){
    const [query, setQuery] = useState("")
    const [selected, setSelected] = useState<string[]>([])
    const [number, setNumber] = useState<number>(0)
    const navigate = useNavigate()
    const { auth } = useContext(AuthContext);


    const ProductsList = [{user_id: 10, description: "dwadziescia", price: 20, category: "Elektronika"},
                            {user_id: 10, description: "dwa", price: 20, category: "Moda"},
                            {user_id: 10, description: "dwadziescia", price: 20, category: "Elektronika"},
                            {user_id: 10, description: "cztery", price: 20, category: "Obuwie"},
                            {user_id: 10, description: "das", price: 20, category: "Dom"},
                            {user_id: 10, description: "dwadziescia", price: 20, category: "AGD"},
                            {user_id: 10, description: "czx", price: 20, category: "Sport"},
                            {user_id: 10, description: "dwadziescia", price: 20, category: "Sport"},
                            {user_id: 10, description: "da", price: 20, category: "Sport"},
                             {user_id: 10, description: "dwapoiajdziescia", price: 20, category: "Sport"},
                            {user_id: 10, description: "xda", price: 20, category: "Sport"},
                            {user_id: 10, description: "hsd", price: 20, category: "Sport"},
                             {user_id: 10, description: "dwadziescia", price: 20, category: "Sport"},
                            {user_id: 10, description: "jrty", price: 20, category: "Sport"},
                            {user_id: 10, description: "dwadziescia", price: 20, category: "Sport"},
                             {user_id: 10, description: "wq", price: 20, category: "Sport"},
                            {user_id: 10, description: "as", price: 20, category: "Sport"},
                            {user_id: 10, description: "xc", price: 20, category: "Sport"}
    ]

    const [products, setProducts] = useState<Product[]>(ProductsList)





    console.log(query)


    return (
        <>
        <div className="flex flex-col h-screen w-full">
            <div className="flex bg-gradient-to-l from-yellow-400 to-green-400 w-full h-14 shadow-lg shadow-gray-700 flex-row gap-15 justify-between px-3">
                <div className='flex text-center gap-2'>
                    <p className="flex py-2 text-white font-bold text-2xl italic cursor-default">Sklepik</p>
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
            <div className= "flex flex-col lg:flex-row bg-white w-full h-full gap-4 p-3">
                <div className='flex flex-col bg-white w-full lg:w-1/4 h-auto gap-3 rounded-md shadow-2xl border border-slate-200'>
                <SearchTile input={query} onInputChange={setQuery}/>
                <Categories selected={selected} OnChange={setSelected}/>


                </div>
                  <div className='flex bg-white w-full lg:flex-1 h-screen rounded-lg shadow-xl border border-slate-200 flex-wrap overflow-y-auto'>
                  <div className='flex  text-slate-400 text-xs font-medium uppercase justify-end items-end w-full'>
                            Znaleziono: <span className="text-orange-500 font-bold">{number}</span>
                        </div>
                   <Products products={products} selected={selected} setNum={setNumber}  query={query} />


                </div>
                <div className='flex bg-white w-full lg:w-64 h-40 border border-slate-200'>

                </div>
            </div>
        </div>
        </>
    )
}



export default HomePage
