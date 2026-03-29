import React, { useContext, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './ContextAPI';


interface User {
    id: number;
    name: string;
    email: string;
    image_source: string;

}


function ProfilPage() {

    const navigate = useNavigate()
    const { auth } = useContext(AuthContext)

    useEffect(() => {
        const fetchData = async () => {
            const response = fetch("http://127.0.0.1:8000/me")
        }
    })



    return (
      <div className='flex bg-gray-100 w-screen h-screen justify-center items-center'>
    <div className='flex flex-col bg-white w-[1200px] h-[800px] shadow-xl rounded-xl overflow-hidden'>
        <div className='flex items-center bg-gradient-to-l from-yellow-400 to-green-400 w-full h-[200px]' >
            <h1 className='flex text-white text-4xl font-bold '> Dodaj swoje zdjecie</h1>
            </div>

        <div className='flex flex-row items-end px-10 -mt-20 space-x-6'>
            <label className='cursor-pointer w-40 h-40 rounded-full border-8 border-white shadow-lg overflow-hidden shrink-0 bg-white relative z-10'>
                <input type='file' accept="image/*" className="hidden"/>
                <img  className='w-full h-full object-cover'/>
            </label>
            <h1 className='text-3xl font-bold pb-4 text-gray-800'>
                Witaj, <span className='text-orange-500'>{auth.name}</span>
            </h1>
        </div>
        <div className='flex p-10 flex-1'>
            <div className='flex flex-col gap-2 mt-10'>
                <button
                    onClick={() => navigate("/CreateProduct")}
                    className='mt-3 bg-green-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md active:scale-90'>
                    Dodaj produkt
                </button>

                <button
                    className='mt-3 bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md active:scale-90'>
                    Edytuj swoje dane
                </button>
                <button
                    className='mt-3 bg-green-500 hover:bg-red-600 text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md active:scale-90'>
                    Wyloguj sie
                </button>
                <button
                    className='mt-3 bg-green-500 hover:bg-yellow-300 hover:shadow-[0_0_15px_rgba(255,255,0.9),0_0_15px_rgba(255,255,0.9),0_0_15px_rgba(255,255,0.9)]  text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md active:scale-90'>
                   Uzytkownik premium
                </button>
                <button
                    className='mt-3 bg-green-500 hover:bg-green-800 tranistion-all text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md active:scale-90'>
                   Zmien zdjecie
                </button>
            </div>
        </div>
    </div>
</div>


    )



}




export default ProfilPage
