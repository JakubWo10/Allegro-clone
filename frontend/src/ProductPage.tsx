import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AGD from './assets/AGD.png';


interface UserProduct {
    proudct_id: number;
    name: string;
    price: number;
    description: string;
    owner_id: number;
    category: string;
    main_image: string;
    quantity: number;
    owner_name: string;
    owner_image: string;
}


function ProductPage ()
{



    const { id } = useParams()
    const navigate = useNavigate()
    const [files, setFiles] = useState([])
    const [page, setPageName] = useState("Dane")
    const [count, setCount] = useState(1)
    const [product, setProduct] = useState<UserProduct | null>(null)

    useEffect(() => {
        const fetchadata = async () => {
            const response = await fetch(`http://127.0.0.1:8000/product/${id}`)

            const data = await response.json()
            if (!response.ok)
            {
                navigate("/")
                return
            }
            console.log(data)
            setProduct(data)
            console.log(product)
        }
        fetchadata();

    },[id, navigate])

    if (!product) {
        return <div className="loading">Ładowanie danych...</div>;
    }
   return (

    <div className="flex flex-row bg-gray-100 min-h-screen w-full pt-3 gap-2 p-2">
        <div className="flex-1 border-2 border-green-300 bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="flex flex-col w-full h-full">
                <div className="flex flex-1 border-b-2 border-red-500 flex-col p-6">
                    <div className="flex items-center justify-center flex-col gap-4">
                        <h2 className="text-xl font-black text-gray-800 text-center tracking-tight">
                            OPIS PRODUKTU KTÓRY BĘDZIE NORMALNIE POTEM
                        </h2>
                        <div className="bg-gray-50 p-4 rounded-lg w-full flex justify-center h-full">
                            <img src={`http://127.0.0.1:8000${product.main_image}`} className="object-contain max-h-64 drop-shadow-md" alt="Produkt"/>
                        </div>
                        <div className="flex flex-col items-start justify-start w-full">
                            <h1>
                                Uzytkownik premium:
                            </h1>
                              <h1>
                                Ilosc transakcji uzytkownika
                            </h1>
                              <h1>
                                Ocena uzytkownika:
                            </h1>
                        </div>
                    </div>

                    <div className="flex flex-row justify-start w-full h-full mt-6">
                        <div className="flex flex-col justify-end items-start gap-1">
                            <span className="text-xs uppercase font-bold text-gray-400">Produkt wystawiony przez:</span>
                            <div className="flex flex-row items-center gap-3 bg-gray-50 p-2 pr-4 rounded-full border border-gray-100">
                                <div className="w-10 h-10 rounded-full border-2 border-white shadow-sm overflow-hidden cursor-pointer">
                                    <img src={`http://127.0.0.1:8000${product.owner_image}`} className="w-full h-full object-cover" alt="Avatar"/>
                                </div>
                                <h1 className="cursor-pointer font-bold text-gray-700 hover:text-blue-600 transition-colors">
                                    {product.owner_name}
                                </h1>
                            </div>
                        </div>
                    </div>
                </div>


                <div className="flex flex-1 border-purple-500 flex-col bg-white">
                    <div className="flex flex-1 justify-start flex-col items-center p-6">
                    <div className="flex flex-row gap-4">
                        <h1 className="text-xl font-bold mb-6 border-purple-500 pb-1 px-4 cursor-pointer hover:border-b-5 transition-all duration-100" onClick={() => setPageName("Dane")}>
                            Dane o produkcie

                        </h1>
                         <h1 className="text-xl font-bold mb-6 border-purple-500 pb-1 px-4 cursor-pointer hover:border-b-5 transition-all duration-100" onClick={() => setPageName("Opis")}>
                           Opis produktu
                        </h1>
                         <h1 className="text-xl font-bold mb-6 border-purple-500 pb-1 px-4 cursor-pointer hover:border-b-5 transition-all duration-100" onClick={() => setPageName("Komentarze")}>
                            Komentarze
                        </h1>
                    </div>
                        {page === "Dane" &&
                         <div className="flex w-full bg-purple-50 p-6 rounded-xl border-l-5 border-r-5 border-purple-400 flex-col gap-3">
                            <h5 className="flex items-center gap-2 font-medium text-gray-700">
                                <span className="w-2 h-2 bg-purple-400 rounded-full"></span> Nazwa produktu: {product.name}
                            </h5>
                            <h5 className="flex items-center gap-2 font-medium text-gray-700">
                                <span className="w-2 h-2 bg-purple-400 rounded-full"></span> Dostępna ilość: {product.quantity}
                            </h5>
                            <h5 className="flex items-center gap-2 font-medium text-gray-700">
                                <span className="w-2 h-2 bg-purple-400 rounded-full"></span> Date: 11.04.2026
                            </h5>
                              <h5 className="flex items-center gap-2 font-medium text-gray-700">
                                <span className="w-2 h-2 bg-purple-400 rounded-full"></span> Kategoria: {product.category}
                            </h5>
                        </div>
                        }
                        {page === "Opis" &&
                        <div className="flex w-full bg-purple-50 p-6 rounded-xl border-l-5 border-r-5 border-green-400 flex-col gap-3">

                            <text> {product.description} </text>

                        </div>

                        }

                        {page === "Komentarze" &&
                        <div className="flex flex-col w-full gap-5">
                            <button className="rounded-xl bg-gray-50 font-bold hover:bg-purple-500 active:scale-95 transition-all duration-200 hover:text-lg"> Dodaj komentarz</button>
                            <div className="flex w-full bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex-row gap-4 items-start transition-hover hover:shadow-md">
                                <div className="w-10 h-10 rounded-full border flex-shrink-0 flex items-center justify-center font-bold">
                                    <img src={AGD} />
                                </div>
                                <div className="flex flex-col flex-1">
                                    <div className="flex justify-between items-center ">
                                        <h1 className="font-bold text-gray-900 text-sm">Nazwa użytkownika</h1>
                                        <span className="text-xs text-gray-400">12.04.2026</span>
                                    </div>
                                    <div>
                                        <span> tresc wiadomosci</span>
                                    </div>

                                </div>
                             </div>
                              <div className="flex w-full bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex-row gap-4 items-start transition-hover hover:shadow-md">
                                <div className="w-10 h-10 rounded-full border flex-shrink-0 flex items-center justify-center font-bold">
                                    <img src={AGD} />
                                </div>
                                <div className="flex flex-col flex-1">
                                    <div className="flex justify-between items-center ">
                                        <h1 className="font-bold text-gray-900 text-sm">Nazwa użytkownika</h1>
                                        <span className="text-xs text-gray-400">12.04.2026</span>
                                    </div>
                                    <div>
                                        <span> tresc wiadomosci</span>
                                    </div>

                                </div>
                             </div>
                              <div className="flex w-full bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex-row gap-4 items-start transition-hover hover:shadow-md">
                                <div className="w-10 h-10 rounded-full border flex-shrink-0 flex items-center justify-center font-bold">
                                    <img src={AGD} />
                                </div>
                                <div className="flex flex-col flex-1">
                                    <div className="flex justify-between items-center ">
                                        <h1 className="font-bold text-gray-900 text-sm">Nazwa użytkownika</h1>
                                        <span className="text-xs text-gray-400">12.04.2026</span>
                                    </div>
                                    <div>
                                        <span> tresc wiadomosci</span>
                                    </div>

                                </div>
                             </div>
                        </div>
                        }

                    </div>
                </div>
            </div>
        </div>


        <div className="flex-1 border-2 border-blue-500 bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-800">Informacje od sprzedawcy</h2>
            <div className="flex w-full bg-purple-50 p-6 rounded-xl border-l-5 border-r-5 border-green-400 flex-col gap-3">
                        <h2> np czemu sprzdaje, </h2>
                  </div>
            <div className="flex flex-col mt-4 h-40 rounded-lg ">
                <h1> 399,99 PLN</h1>
                <div className="flex flex-row">
                    <button className="w-8 h-8 flex items-center justify-center rounded-md bg-white text-gray-600 hover:bg-orange-400 hover:text-white transition-colors duration-200 font-bold shadow-sm">-</button>
                    <div className="px-4 min-w-[3rem] text-center font-bold text-gray-800">
                        {count}
                    </div>
                    <button className="w-8 h-8 flex items-center justify-center rounded-md bg-white text-gray-600 hover:bg-orange-400 hover:text-white transition-colors duration-200 font-bold shadow-sm">+</button>
                </div>

            </div>
        </div>
    </div>
);
}




export default ProductPage
