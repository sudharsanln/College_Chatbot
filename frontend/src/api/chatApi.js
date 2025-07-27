import axios from 'axios'

const BASE_URL = import.meta.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8085';

export const answerQuestion = async(query) => {
    const res = await axios.post(`${BASE_URL}/chat`,{query});
    return res.data.result
};

export const diveDeeper = async(previousAnswer) => {
    const res = await axios.post(`${BASE_URL}/dive_deeper`, previousAnswer);
    return res.data
};