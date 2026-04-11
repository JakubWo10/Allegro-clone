import './index.css'
import { useNavigate } from 'react-router-dom'
import { useContext, useEffect, useState } from 'react'
import SearchTile from './Components/SearchTile'
import Categories from './Components/Categories'
import { AuthContext } from './ContextAPI'
import Products from './Components/Products'
import { type Product } from './Components/Products'
import { preview } from 'vite'


interface User {
    name: string;
    email: string;
    image_source: string;

}


function HomePage(){
    const [query, setQuery] = useState("")
    const [selected, setSelected] = useState<string[]>([])
    const [number, setNumber] = useState<number>(0)
    const navigate = useNavigate()
    const { auth, setAuth } = useContext(AuthContext);
    const [debounce, setDebounce] = useState("")
    const [user, setUser] = useState<User>()
    const BASE_URL = "http://127.0.0.1:8000";
    const [currentPage, setCurrentPage] = useState(0)
    const [skip, setSkip] = useState(0)
    const [products, setProducts] = useState<Product[]>([])
    const [hasMore, setHasMore] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("")


      useEffect(() => {
        const fetchProdcuts = async () => {
            try
            {
                const response = await fetch(`http://127.0.0.1:8000/products?skip=${skip}`)

                const data = await response.json()
                if (!response.ok)
                {
                    setError(data.message)
                    return
                }
                setProducts(prev => {
                    if (skip === 0)
                    {
                        return data.products
                    }
                    return [...prev, ...data.products]
                })
                setHasMore(data.has_more)


            }
            catch (err)
            {
                console.log(err)
            }
        }
        fetchProdcuts()
      }, [skip])


      useEffect(() => {
        const token = localStorage.getItem("token");
        const fetchData = async () => {
        if (!token)
        {
            return;
        }
        const response = await fetch("http://127.0.0.1:8000/me",{
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
                }
        })
        if (!response.ok)
        {
            if (response.status === 401) {
            setAuth({
                name: null,
                token: null,
                image_url: null,
                email: null,
                user_id: null,

            })
            localStorage.clear()
        }
            return
        }
        const data: User = await response.json()
        setUser(data)
        setAuth({
            ...auth,
        image_url: `${BASE_URL}${data.image_source}`,
        })

            localStorage.setItem("image_source", `${BASE_URL}${data.image_source}`)
        }
        fetchData();
    },[])

    useEffect(() => {
        const handler = setTimeout(() => {
            setDebounce(query)
        }, 500)

        return () => { clearTimeout(handler) }
    }, [query])

    return (
        <>
        <div className="flex flex-col h-screen w-full">
            <div className= "flex flex-col lg:flex-row bg-white w-full h-full gap-4 p-3">
                <div className='flex flex-col bg-white w-full lg:w-1/4 h-auto gap-3 rounded-md shadow-2xl border border-slate-200'>
                <SearchTile input={query} onInputChange={setQuery}/>
                <Categories selected={selected} OnChange={setSelected}/>


                </div>
                  <div className='flex bg-white w-full lg:flex-1 h-screen rounded-lg shadow-xl border border-slate-200 flex-wrap overflow-y-auto justify-center'>
                  <div className='flex  text-slate-400 text-xs font-medium uppercase justify-end items-end w-full'>
                            Znaleziono: <span className="text-orange-500 font-bold">{number}</span>
                        </div>
                    <Products products={products} selected={selected} setNum={setNumber}  query={debounce} />


                   {hasMore && (
                    <div className='flex justify-center w-full py-6 mt-auto'>
                    <button  className= "flex items-center justify-center" onClick={() => setSkip(prev => prev + 12)}>
                        {loading ? "Ładowanie..." : "Pokaż więcej"}
                    </button>
                      </div>
                    )}
                    </div>

                <div className='flex bg-white w-full lg:w-64 h-40 border border-slate-200'>

                </div>
            </div>
        </div>
        </>
    )
}



export default HomePage
