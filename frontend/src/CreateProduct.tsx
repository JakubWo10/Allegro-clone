import Select from "react-select/base"

import MasterTier from "./assets/mastertier.png"
import { useContext, useState } from "react"
import { AuthContext } from "./ContextAPI"


function CreateProduct () {

    const { auth } = useContext(AuthContext)
    const  token  = auth.token

    const [category, setCategory] = useState<string>("")
    const [file, setFile] = useState<File | null>(null)
    const [description, setDescription] = useState<string>("")
    const [price, setPrice] = useState<number | "">("")
    const [quantity, setQuantity] = useState<number | "">("")
    const [name, setName] = useState("")
    const [message, setMessage] = useState("")

    const [preview, setPreview] = useState("")



    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0 )
        {
            const selectedFile = e.target.files[0]
            setFile(e.target.files[0])

            const imagePreview = URL.createObjectURL(selectedFile)

            setPreview(imagePreview)

        }
    }

    const handlePreview = () => {
        setPreview("")
    }


    async function  sendProductData ()
    {
        console.log("KLIKNIETO")
        if (!file)
        {
            return
        }
        if (!category.trim() || !description.trim() || !name.trim() || ( quantity !== "" && quantity < 1)  || (price !== "" && price < 0) )
        {
            return
        }

        const formData = new FormData();
        formData.append("file", file)
        formData.append("category", category)
        formData.append("description", description)
        formData.append("price", String(price))
        formData.append("quantity", String(quantity))
        formData.append("name", name)

        try {

            const response = await fetch(`http://127.0.0.1:8000/product/create`, {
            method: "POST",
            headers: {"Authorization": `Bearer ${token}`},
            body: formData

        })

        if (!response.ok)
        {
            console.log(response)
            return
        }
        const data = await response.json()

        setMessage(data.Message)



        }
       catch (err) {
        console.log(err)
        return

       }




    }


    return (

        <div className="flex flex-row justify-center items-center h-screen w-screen bg-gray-300">
                <div className="flex flex-col bg-white w-[1200px] h-[800px] shadow-md border-slate-200 rounded-lg overflow-hidden">
                    <div className="w-full h-32 bg-gradient-to-l from-yellow-400 to-green-400">
                        <label className="flex w-40 h-40 mt-13 ml-10 block">
                            <img  src={MasterTier} className="w-full h-full rounded-full border-8 border-white object-cover" />
                        </label>
                    </div>
                    <div className="flex flex-row w-full h-full mt-24">
                        <div className="flex flex-col flex-1 px-10 gap-4">
                            <div>

                                <p className="flex font-semibold text-gray-600">Podaj cenę</p>
                                <div className="flex flex-row items-center">
                                <input value={price} onChange={(e) => setPrice(Number(e.target.value))} type="number"  placeholder="0.00 zł" className="focus-within:border-green-400 w-full border p-2 rounded-md bg-gray-50 focus:bg-white transition-all outline-none border-gray-200 focus:border-green-400" />
                                <span className="text-gray-500 font-medium pb-0.5">zł</span>
                                </div>

                                </div>
                                <div>
                                <p className="font-semibold text-gray-600">Tytuł produktu</p>
                                <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Nazwa przedmiotu" className="w-full border p-2 rounded-md bg-gray-50 focus:bg-white outline-none border-gray-200 focus:border-green-400" />
                                </div>
                                <div>
                                <p className="font-semibold text-gray-600">Ilosc produktu</p>
                                <input value={quantity} onChange = {(e) => setQuantity(Number(e.target.value))}  type="number" placeholder="Ilosc" className="w-full border p-2 rounded-md bg-gray-50 focus:bg-white outline-none border-gray-200 focus:border-green-400" />
                                </div>
                                <div>
                                <p className="font-semibold text-gray-600">Kategoria produktu</p>
                                <select value={category} onChange={(e) => setCategory(e.target.value)} className="w-full border p-2 rounded-md bg-gray-50 focus:bg-white outline-none border-gray-200 focus:border-green-400">
                                    <option value ="">-- WYBIERZ OPCJE --</option>
                                    <option value="Elektronika"> Elektronika </option>
                                    <option value="AGD"> AGD </option>
                                    <option value="Dom"> Dom </option>
                                    <option value="Sport"> Sport </option>
                                    <option value="Obuwie"> Obuwie </option>
                                </select>
                                </div>

                                <div className="flex flex-col h-full mb-10">
                                <p className="font-semibold text-gray-600">Podaj opis</p>
                                <textarea value = {description} onChange={(e) => setDescription(e.target.value)} placeholder="Opis..." className="flex-1 w-full border p-4 rounded-md bg-gray-50 focus:bg-white outline-none border-gray-200 focus:border-green-400 resize-none" />
                                </div>
                            </div>

                            <div className="flex-1 flex-row ">
                                <div className="flex flex-col flex-1 items-center justify-start pr-10">
                                        <p className="font-semibold text-gray-600 mb-4 w-40 text-left">Dodaj zdjęcie</p>
                                        <label className="group bg-gray-100 border-gray-400 hover:bg-gray-200 rounded-2xl cursor-pointer transition-all flex flex-col w-40 h-40 items-center justify-center border-dashed border-2 hover:border-gray-700">
                                        <span className="text-gray-600 font-black text-8xl group-hover:scale-110 group-hover:text-gray-400 transition-transform">+</span>
                                        <span className="text-gray-400 group-hover:text-gray-800 font-medium transition-colors">Dodaj zdjęcie</span>
                                        <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
                                        </label>
                                        <p className="text-xs text-gray-400 mt-4 text-center">To zdjęcie będzie wyświetlane jako główne na aukcji.</p>

                                    </div>
                                    <div className="group flex flex-col justify-center items-center mr-10 gap-5">
                                        <button onClick={sendProductData}  className="flex w-[260px] h-[40px] justify-center  bg-gradient-to-r from-yellow-400 to-green-400 py-2 rounded-xl text-white font-bold hover:scale-105 transition-transform"> Dodaj produkt </button>
                                        <button onClick={handlePreview}  className="flex w-[260px] h-[40px] justify-center  bg-gradient-to-r from-yellow-400 to-green-400 py-2 rounded-xl text-white font-bold hover:scale-105 transition-transform"> usun zdjecie </button>
                                    </div>
                                    {preview && (
                                    <div className="flex items-center justify-center flex-col mt-3  w-full ">
                                        <p className="text-sm text-gray-500 ">Podgląd zdjęcia</p>
                                        <img
                                            src={preview}
                                            className="border-4 border-gray-200 w-50 h-50 object-cover rounded-xl shadow-sm"
                                        />
                                    </div>


                                   ) }


                            </div>

                        </div>

                    </div>
            </div>

    )
}



export default CreateProduct
