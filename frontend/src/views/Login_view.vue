<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const senha = ref('')
const router = useRouter()

function entrar(){
    router.push('/vault')
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
    
    .container{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background-color: rgb(30, 126, 209);
    }
    h1{
        margin-bottom: 40px;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-weight: 300;
    }
    #entrar{
        margin-top: 15px;
        background-color: aliceblue;
        border: 0;
        padding: 10px;
        border-radius: 10px;
        cursor: pointer;
    }

    #input{
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        border-radius: 3px;
        border: 0;
        padding: 2px;
    }
</style>