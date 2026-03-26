import Sport from "../assets/Sport.png"
import Moda from "../assets/Moda.png"
import AGD from "../assets/AGD.png"
import Elektronika from "../assets/Elektronika.png"
import Dom from "../assets/Dom.png"
import Obuwie from "../assets/Obuwie.png"
import { useState } from "react"

interface CategoriesProps {
    selected: string[];
    OnChange: (nSelected: string[]) => void;
}



function Categories ({ selected, OnChange }: CategoriesProps) {



    const [isOpen, setIsOpen] = useState(false);
    const CATEGORIES = [{Name: "Dom", src: Dom},
        {Name: "Sport", src: Sport},
        {Name: "Elektronika", src: Elektronika},
        {Name: "Moda", src: Moda},
        {Name: "Obuwie", src: Obuwie},
        {Name: "AGD", src: AGD}]

    function toggleonChange( category: string) {

        const newList = selected.includes(category) ? selected.filter(item => item !==category) : [...selected, category]

        OnChange(newList)

    }


    return (




        <div className="flex flex-col gap-2 bg-white gap-2 items-center">
            <button  className="flex items-center gap-2" onClick={() => setIsOpen(!isOpen)}>
                Wybierz kategorie
                <span className={`gap-2 inline-block transition-transform duration-300 ${isOpen ? 'rotate-180' : 'rotate-0'}`}>▼ </span>
            </button>
           {isOpen && (
                <div className="flex flex-wrap gap-3 justify-center">
                {CATEGORIES.map((category) => {
                const isSelected = selected.includes(category.Name);
                return (
                <label key={category.Name} className={`flex flex-col items-center justify-center cursor-pointer border-2 p-4 rounded-xl transition-all text-center font-semibold w-25 h-24
                    ${isSelected ?
                    'bg-blue-600 border-blue-600 text-white shadow-lg scale-95'
                    : 'bg-gray-100 border-transparent text-gray-600 hover:bg-gray-200'} ` }>
                    <input type="checkbox" onChange={() => toggleonChange(category.Name)} checked = {isSelected} className="hidden "/>
                <img src = {category.src} alt={category.Name} className={`w-6 h-6 object-contain justify-start cursor-pointer ${isSelected ? 'brightness-0 invert' : ''}`}/>
                    <span> {category.Name} </span>

                </label>
                )
            })}

                </div>


            )}

            </div>
        )




}

export default Categories
