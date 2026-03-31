import React, { useContext, useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './ContextAPI';
import { json } from 'stream/consumers';
import { userInfo } from 'os';
import { User } from 'lucide-react';





function ProfilPage() {


    const navigate = useNavigate()

    const { auth, setAuth } = useContext(AuthContext)
    const [image_source, setImagelink] = useState("")
    const [file, setFile] = useState<File | null>(null)
    const [preview, setPreview] = useState("")
    const [message, setMessage] = useState("")
    function logout()
    {

        setAuth({
            user_id: null,
            token: null,
            email: null,
            name: null,
            image_url: null
        })

        localStorage.removeItem("token")
        localStorage.removeItem("name")
        localStorage.clear()

        navigate("/")
    }
    useEffect(() => {
        const image_link = localStorage.getItem("image_source")
        if (image_link)
        {
            setImagelink(image_link)

        }
    })

    function handlePreview(e: React.ChangeEvent<HTMLInputElement>) {

        if (e.target.files && e.target.files.length > 0)
        {
            const selectedFile = e.target.files[0]
            setFile(selectedFile)

            const urlObject = URL.createObjectURL(selectedFile)
            setPreview(urlObject)
        }


    }


    async function setProfilePicture()
    {
        if (!file)
        {
            return
        }
        const data = new FormData()
        data.append("file", file)
        const user_id = localStorage.getItem("user_id")
        if (!user_id)
        {
            localStorage.clear()
            navigate("/")
            return
        }


        try {


        const response = await fetch(`http://127.0.0.1:8000/${user_id}/profile/image`,
            {
                method: "PATCH",
                headers: {"Authorization": `Bearer ${auth.token}`},
                body: data
            }
        )
            const backendResponse = await response.json()

            if(!response.ok)
            {
                console.log(response)
                return
            }

            setMessage(backendResponse.Message)
        }



        catch(err)
        {
            console.log(err)
        }

    }





    return (
      <div className='flex bg-gray-100 w-screen h-screen justify-center items-center'>
    <div className='flex flex-col bg-white w-[1200px] h-[800px] shadow-xl rounded-xl overflow-hidden'>
        <div className='flex items-center bg-gradient-to-l from-yellow-400 to-green-400 w-full h-[200px]' >
            </div>

        <div className='flex flex-row items-end px-10 -mt-20 space-x-6'>
            <label className='cursor-pointer w-40 h-40 rounded-full border-8 border-white shadow-lg overflow-hidden shrink-0 bg-white relative z-10'>
                <input type='file' accept="image/*" className="hidden" onChange={handlePreview}/>
                <img  src = {image_source} className='w-full h-full object-cover'/>
            </label>
            {preview && (
                <div className='flex justify-end items-end'>
                 <label className='cursor-pointer w-40 h-40 rounded-full border-8 border-white shadow-lg overflow-hidden shrink-0 bg-white relative z-10'>
                <input type='file' accept="image/*" className="hidden"/>
                <img  src = {preview} className='w-full h-full object-cover'/>
                </label>
                </div>
            )}
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
                <button onClick={logout}
                    className='mt-3 bg-green-500 hover:bg-red-600 text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md active:scale-90'>
                    Wyloguj sie
                </button>
                <button
                    className='mt-3 bg-green-500 hover:bg-yellow-300 hover:shadow-[0_0_15px_rgba(255,255,0.9),0_0_15px_rgba(255,255,0.9),0_0_15px_rgba(255,255,0.9)]  text-white font-bold py-3 px-6 rounded-lg transition-all shadow-md active:scale-90'>
                   Uzytkownik premium
                </button>
                <button onClick={setProfilePicture}
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
