const API_URL = import.meta.env.VITE_API_URL

export async function apiFetch(endereco,options = {}){
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_URL}${endereco}`,{
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(token && {token}),
            ...options.headers,
        },

    })

    if (!response.ok) {
        throw new Error(`Erro ${response.status}`);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}