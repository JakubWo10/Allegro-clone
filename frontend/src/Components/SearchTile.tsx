
interface SearchTileProps {
    input: string;
    onInputChange: (value: string) => void
}



function SearchTile ({input, onInputChange} : SearchTileProps) {


    return (
        <>
        <div className="flex flex-col py-7 w-full px-2 ">
        <h1> Wyszukaj to czego szukasz</h1>
            <input value={input} onChange={(e) => onInputChange(e.target.value)} placeholder="Wyszukaj"  className="w-full h-7 bg-white rounded-md shadow-md shadow-gray-500"/>
        </div>
        </>

    )




}

export default SearchTile
