import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

export default api;

// ===============================================
// DOCUMENTS
// ===============================================

export const getDocuments = () =>
    axios.get("http://127.0.0.1:8000/documents");

export const getActiveDocument = () =>
    axios.get("http://127.0.0.1:8000/documents/active");

export const setActiveDocument = (documentName) =>
    axios.post(
        `http://127.0.0.1:8000/documents/active/${encodeURIComponent(documentName)}`
    );