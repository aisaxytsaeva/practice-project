import React from "react";
// import { useEffect, useState } from 'react';
// import { Button } from "flowbite-react";


function App() {
  // const [vacancyName, setVacancyName] = useState('')

  return (
    <div className='w-[700px] h-[400px] m-auto mt-[20px] border-4 border-black rounded-xl'>
      <div className='flex align-center flex-col w-[554px] m-auto'>
      <h2 className='text-[48px] text-center pt-[30px]'>Job Connect</h2>
      <input className="focus:outline-none text-[20px] text-black opacity-[60%] w-full mt-[50px] border-b-4 border-black" type="text" placeholder = "Напишите навзвание нужной Вам вакансии">
      </input>
      <button  className="text-[30px] text-center w-[296px] h-[50px] border-black border-4 rounded-xl mt-[70px] ml-[110px] py-0 hover:border-gray-300 hover:text-gray-300">
        Искать!</button>
      </div>
    </div>
  );
}

export default App;