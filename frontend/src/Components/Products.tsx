import Elektronika from "../assets/Elektronika.png"
import { useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";

export interface Product {
    product_id: number;
    name: string;
    owner_id: number;
    description: string;
    price: number;
    category: string;
    main_image: string;
    quantity: number;
}


interface ProductList {
    products: Product[]
    selected: string[]
    query: string;
    setNum: (number: number) => void
}





function Products ({products, selected, setNum, query}: ProductList) {

    const navigate = useNavigate()

    function naviageToDetailPage (product_id : number) {
        navigate(`/product/${product_id}`)
    }

    const filteredProducts = useMemo(() => {
        const result = selected.length > 0 ? products.filter(item => selected.includes(item.category)) : products

        return query.length > 0 ? result.filter(item => item.name.includes(query.toLocaleLowerCase())) : result

    }, [query, products, selected])

    useEffect(() => {
        setNum(filteredProducts.length)
    }, [filteredProducts])



   return (
        <div className="flex flex-row w-full h-full gap-3 flex-wrap justify-around py-2">
            {filteredProducts.map((product, index) => {

                return (
                <div onClick = {() => naviageToDetailPage(product.product_id)} key={index} className="bg-white p-2 w-64 h-64 rounded-2xl shadow-lg border border-slate-100 flex flex-col justify-between hover:shadow-2xl transition-shadow cursor-pointer items-center">
                    <p className="text-gray-600 text-left">{product.name} - {product.category} </p>
                    <label>
                        <img src={`http://127.0.0.1:8000${product.main_image}`} className="w-40 h-40 flex cursor-pointer "/>
                    </label>
                    <p className="text-orange-500 font-bold mt-2">{product.price} PLN</p>
                </div>
            )})}
        </div>
    );


}




export default Products
