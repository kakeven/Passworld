<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { apiFetch } from "@/js/fetch";
const senha = ref('')
const router = useRouter()

async function entrar() {
    try {
        const resposta = await apiFetch("/unlock", {
            method: "POST",
            body: JSON.stringify({
                password: senha.value
            })
        });

        if (resposta.token) {
            localStorage.setItem("token", resposta.token)
            router.push("/vault")
        }
    } catch (erro) {
        console.error(erro);
        alert("Senha inválida");
    }
}
</script>

<template>
    <div class="container">
        <h1>Passworld</h1>
        <input id="input" v-model="senha"
                type="password"
                placeholder="Senha mestra"/>
        <button id="entrar" @click="entrar">Entrar</button>
    </div>
</template>

<style scoped>
    
    .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: #020617;
}

h1 {
    margin-bottom: 32px;
    color: #f8fafc;
    font-size: 2rem;
    font-weight: 600;
    font-family: Inter, Arial, sans-serif;
}

#input {
    width: 320px;
    padding: 12px 16px;
    margin-bottom: 12px;

    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;

    color: white;
    font-size: 1rem;
    outline: none;
}

#input:focus {
    border-color: #3b82f6;
}

#input::placeholder {
    color: #94a3b8;
}

#entrar {
    width: 320px;
    padding: 12px;

    background: #2563eb;
    color: white;

    border: none;
    border-radius: 12px;

    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;

    transition: all 0.2s ease;
}

#entrar:hover {
    background: #1d4ed8;
    transform: translateY(-2px);
}

#entrar:active {
    transform: translateY(0);
}
</style>