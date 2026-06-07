<script setup>
    import { ref,computed } from 'vue';
    import { onUnmounted,onMounted } from 'vue';
    const buscar = ref('');
    const credenciais = ref([
    { id: 1, servico: 'GitHub', usuario: 'kaua@email.com', senha: '123456' },
    { id: 2, servico: 'Gmail', usuario: 'kaua@gmail.com', senha: 'abcdef' },
    { id: 3, servico: 'discord', usuario: 'kaua@gmail.com', senha: 'abcdef' },
    { id: 4, servico: 'nexus', usuario: 'kaua@gmail.com', senha: 'abcdef' },
    ])
    
    const menuX = ref(0);
    const menuY = ref(0);
    const menu_visivel = ref(false);
    const credencial_selecionada = ref(null);
    
    const modal_visivel = ref(false);
    const modal_senha = ref('')
    const modal_login = ref('')
    const modal_servico = ref('')
    
    const busca_resultado = computed(()=>{
        return credenciais.value.filter(b=>b.servico.toLowerCase().includes(buscar.value.toLowerCase()))
    })
    
    function excluir_credencial(){
        return credenciais.value = credenciais.value.filter(c => c.id !== credencial_selecionada.value.id)
    }

    function abrir_menu(e,credencial){
        e.preventDefault()
        menuX.value = e.clientX
        menuY.value = e.clientY
        menu_visivel.value = true
        credencial_selecionada.value = credencial
    }

    function fechar_menu(){
        menu_visivel.value = false
    }

    function abrir_modal(){
        modal_visivel.value = true
        console.log("abriu")
    }

    function fechar_modal(){
        modal_visivel.value = false
        resetar_modal()
    }
    onMounted (()=>{
        window.addEventListener('click',fechar_menu)
    })

    onUnmounted(()=>{
        window.removeEventListener('click',fechar_menu)
    })

    function copiar_senha(){
        navigator.clipboard.writeText(credencial_selecionada.value.senha)
    }

    function resetar_modal(){
        modal_servico.value = ''
        modal_login.value = ''
        modal_senha.value = ''
    }

    function salvar_credencial(){
        credenciais.value.push({
        id: credenciais.value.length + 1,
        servico: modal_servico.value,
        usuario: modal_login.value,
        senha: modal_senha.value
         })
        fechar_modal()
    }

</script>

<template>
    <header>
        <h4 id="titulo">Passworld</h4>
        <input type="search" v-model="buscar" id="busca" placeholder="Buscar">
        <button type="button" id="botao" @click="abrir_modal">Nova credencial</button>
    </header>
    <main>
        <div class="card" v-for="credencial in busca_resultado" :key="credencial.id" @contextmenu="(e)=>abrir_menu(e,credencial)" >
            <p>{{ credencial.servico }}</p>
            <p>{{ credencial.usuario }}</p>
        </div>
        <div class="menu-contexto"  v-if="menu_visivel" :style="{top: menuY + 'px', left:menuX + 'px' }" @click.stop>
            <p>Editar</p>
            <p @click="excluir_credencial">Excluir</p>
            <p @click="copiar_senha">Copiar senha</p>
        </div>
    
        
    </main>
    
    <div class="overlay" v-if="modal_visivel" @click="fechar_modal">
        <div class="modal" @click.stop>
            <label for="">Site/Serviço</label>
            <input type="text" v-model="modal_servico">

            <label for="">Login</label>
            <input type="text" v-model="modal_login">

            <label for="">Senha</label>
            <input type="password" v-model="modal_senha">
        
            <button @click="salvar_credencial">
                Salvar
            </button>

            <button @click="fechar_modal">
                Cancelar
            </button>
        </div>

    </div>

</template>

<style scoped>

    .overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

* {
    box-sizing: border-box;
}

main {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    padding: 24px;
}

.card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 18px;
    transition: all 0.2s ease;
    cursor: pointer;
}

.card:hover {
    transform: translateY(-4px);
    border-color: #3b82f6;
    box-shadow: 0 10px 20px rgba(0,0,0,0.25);
}

.card p:first-child {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
}

.card p:last-child {
    color: #94a3b8;
}

header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 24px;
    background: #0f172a;
    border-bottom: 1px solid #1e293b;
}

#titulo {
    margin: 0;
    color: white;
    font-size: 1.4rem;
    font-weight: 600;
}

#busca {
    flex: 1;
    border: 1px solid #334155;
    background: #1e293b;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    outline: none;
}

#busca:focus {
    border-color: #3b82f6;
}

#busca::placeholder {
    color: #94a3b8;
}

#botao {
    border: none;
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
}

#botao:hover {
    background: #1d4ed8;
    transform: translateY(-2px);
}

:global(body) {
    margin: 0;
    background: #020617;
    font-family: Inter, Arial, sans-serif;
}


.menu-contexto {
  position: fixed;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 8px 0;
  z-index: 1000;
}

.menu-contexto p {
  padding: 8px 16px;
  color: #f8fafc;
  cursor: pointer;
  margin: 0;
}

.menu-contexto p:hover {
  background: #334155;
}

</style>