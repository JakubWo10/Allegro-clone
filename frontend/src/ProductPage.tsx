import { useState } from "react";
import { useParams } from "react-router-dom";







function ProductPage ()
{

    const { id } = useParams()

    const [files, setFiles] = useState([])

    return (

        <>
        <div className="flex flex-col bg-gray-300 w-screen h-screen justify-center items-center"> 
                <div className="flex flex-col bg-white shadow-md w-[1200px] h-[800px]"> 
                    <input placeholder="Nazwa przedmiotu"/>
                    <input placeholder="Opis przedmiotu "/>
                    <h1> XDXDXD {id} </h1> 

                </div>
        
        </div>
        
        </>


    )
}




export default ProductPage
