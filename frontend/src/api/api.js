import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    return API.post("/upload", formData);
};

export const askQuestion = async (question) => {
    return API.post("/chat", {
        question
    });
};