import Elektronika from "../assets/Elektronika.png"
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export interface Product {
    user_id: number;
    description: string;
    price: number;
    category: string;
}


interface ProductList {
    products: Product[]
    selected: string[]
    query: string;
    setNum: (number: number) => void
}





function Products ({products, selected, setNum, query}: ProductList) {

    const navigate = useNavigate()

    function naviageToDetailPage (user_id : number) {
        navigate(`/product/${user_id}`)


    }


    const filteredProducts = selected.length > 0 ? products.filter(item => selected.includes(item.category)) : products
    const twoTimesFiltered = query.length > 0 ? filteredProducts.filter(item => item.description.includes(query.toLocaleLowerCase())) : filteredProducts

     useEffect(() => {
        setNum(twoTimesFiltered.length);
    }, [twoTimesFiltered.length]);

   return (
        <div className="flex flex-row w-full h-full gap-3 flex-wrap justify-around py-2">
            {twoTimesFiltered.map((product, index) => {

                return (
                <div onClick = {() => naviageToDetailPage(product.user_id)} key={index} className="bg-white p-2 w-64 h-64 rounded-2xl shadow-lg border border-slate-100 flex flex-col justify-between hover:shadow-2xl transition-shadow cursor-pointer items-center">
                    <p className="text-gray-600 text-left">{product.description} - {product.category} </p>
                    <label>
                        <img src={Elektronika} className="w-40 h-40 flex cursor-pointer "/>
                    </label>
                    <p className="text-orange-500 font-bold mt-2">{product.price} PLN</p>
                </div>
            )})}
        </div>
    );


}




export default Products
