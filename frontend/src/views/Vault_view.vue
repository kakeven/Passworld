<script setup>
    import { apiFetch } from '@/js/fetch';
    import { ref,computed } from 'vue';
    import { onUnmounted,onMounted } from 'vue';
    import { reactive } from 'vue'   
    import { useToast } from "vue-toastification";
    import Swal from 'sweetalert2'
    import olho_fechado from '@/assets/olho-fechado.svg'
    import olho_aberto from '@/assets/olho-aberto.svg'
    import router from '@/router';
   
    const toast = useToast();
    const senha_visivel = ref(false)
    
    
    
    function verificar_token(){
        const token = localStorage.getItem("token")
        if(!token){
            localStorage.removeItem("token")
            router.push("/")
            return false
        }
        return true
    }
    
    const config_visivel = ref(false)
    const config_senha = reactive({
    tamanho: 16,
    letras: true,
    numeros: true,
    especiais: true,
    })

    async function gerar_senha() {
        const params = new URLSearchParams ({
            tamanho: config_senha.tamanho,
            letras: config_senha.letras ? 1 : 0,
            numeros: config_senha.numeros ? 1 : 0,
            especiais: config_senha.especiais ? 1 : 0,
        })
        const res = await apiFetch(`/generate?${params}`)
        console.log(params)
        console.log(res)
        modal_senha.value = res.password
    }

    const buscar = ref('');
    const credenciais = ref([]);
    
    onMounted(async () => {
    if(!verificar_token()){return}
    window.addEventListener('click', fechar_menu)
        try {
            credenciais.value = await apiFetch("/entries")
        } catch (erro) {
            console.error(erro)
        }
    })
   
    

    const menuX = ref(0);
    const menuY = ref(0);
    const menu_visivel = ref(false);
    const credencial_selecionada = ref(null);
    
    const modal_visivel = ref(false);
    const modal_senha = ref('')
    const modal_login = ref('')
    const modal_servico = ref('')
    
    const editando = ref(false)

    const busca_resultado = computed(()=>{
        return credenciais.value.filter(b=>b.service.toLowerCase().includes(buscar.value.toLowerCase()))
    })
    
    async function excluir_credencial(entry_id){
        const result = await Swal.fire({
        title: "Excluir credencial?",
        text: "Essa ação não pode ser desfeita.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Excluir",
        cancelButtonText: "Cancelar",
        background: '#1e293b',
        color: '#f8fafc',
    })

    if (result.isConfirmed) {
        apiFetch(`/entries/delete/${entry_id}`, { method: "DELETE" })
        credenciais.value = credenciais.value.filter(c => c.id != entry_id)
        toast.success("Credencial excluída")
    }
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
    

    onUnmounted(()=>{
        window.removeEventListener('click',fechar_menu)
        verificar_token()
    })

    function copiar_senha(){
        navigator.clipboard.writeText(credencial_selecionada.value.password)
        toast.info("Senha copiada")
    }

    function resetar_modal(){
        modal_servico.value = ''
        modal_login.value = ''
        modal_senha.value = ''
    }

    async function salvar_credencial(entry_id=null){
        if (!editando.value){
            const res = await  apiFetch("/create_entry",{
                method:"POST",
                body: JSON.stringify ({
                    "service": modal_servico.value,
                    "login": modal_login.value,
                    "password": modal_senha.value,
                })
            })
            const {id} = await res
            credenciais.value.push({
                id,
                service: modal_servico.value,
                login: modal_login.value,
                password: modal_senha.value,
            })
            fechar_modal()
        }else{
            apiFetch(`/update_entry/${entry_id}`,{
                method: "PATCH",
                body: JSON.stringify({
                    "service": modal_servico.value,
                    "login": modal_login.value,
                    "password": modal_senha.value,
                })
            })
            
            credencial_selecionada.value.service = modal_servico.value
            credencial_selecionada.value.login = modal_login.value
            credencial_selecionada.value.password = modal_senha.value
            fechar_modal()
            editando.value = false
        }
       
    }

    function editar_credencial(){
        editando.value = true
        modal_servico.value = credencial_selecionada.value.service
        modal_login.value = credencial_selecionada.value.login
        modal_senha.value = credencial_selecionada.value.password
        abrir_modal()
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
            <p>{{ credencial.service }}</p>
            <p>{{ credencial.login }}</p>
        </div>
        <div class="menu-contexto"  v-if="menu_visivel" :style="{top: menuY + 'px', left:menuX + 'px' }" @click.stop>
            <p @click="(e)=>{editar_credencial();fechar_menu()}">Editar</p>
            <p @click="(e)=>{excluir_credencial(credencial_selecionada.id); fechar_menu()}">Excluir</p>
            <p @click="(e)=>{copiar_senha();fechar_menu()}">Copiar senha</p>
        </div>
    
        
    </main>
    
    <div class="overlay" v-if="modal_visivel" @click="fechar_modal">
        <div class="modal" @click.stop>
            <label for="">Site/Serviço</label>
            <input type="text" v-model="modal_servico">

            <label for="">Login</label>
            <input type="text" v-model="modal_login">

            <label for="">Senha</label>
            <div class="input-senha">
                <input :type="senha_visivel ? 'text' : 'password'" v-model="modal_senha">
                <span @click="senha_visivel = !senha_visivel">
                    <img v-if="senha_visivel" :src="olho_fechado">
                    <img v-else :src="olho_aberto">
                </span>
            </div>  

            <button class="btn-gerador" @click="config_visivel = !config_visivel"> Gerar senha </button>
            <div class="config-senha"v-if="config_visivel">
                <div class="config-linha-tamanho">
                    <input type="range" min="6" max="32" v-model="config_senha.tamanho">
                    <span>{{ config_senha.tamanho }} dígitos</span>
                </div>
                <label><input type="checkbox" v-model="config_senha.letras">Letras</label>
                <label><input type="checkbox" v-model="config_senha.numeros">números</label>
                <label><input type="checkbox" v-model="config_senha.especiais">Caracteres especiais</label>
                <button class="btn-gerar" @click="gerar_senha">Gerar</button>
            </div>

            <button class="btn-salvar" @click="salvar_credencial(credencial_selecionada?.id)"> Salvar </button>

            <button class="btn-cancelar" @click="fechar_modal"> Cancelar </button>
        </div>

    </div>

</template>

<style scoped>

.input-senha {
    position: relative;
}

.input-senha input {
    padding-right: 40px; /* espaço pro ícone */
}

.input-senha img {
    width: 20px;
    height: 20px;
}

.input-senha span {
    position: absolute;
    right: 12px;
    top: 55%;
    transform: translateY(-50%);
    cursor: pointer;
    font-size: 1rem;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  animation: fadeIn 0.2s ease;
}

.modal {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 24px;
  padding: 32px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(59, 130, 246, 0.3);
  animation: slideUp 0.3s ease;
}

.modal label {
  display: block;
  color: #94a3b8;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 6px;
  margin-top: 18px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.modal label:first-of-type {
  margin-top: 0;
}

.modal input {
  width: 100%;
  padding: 12px 16px;
  background: #0f172a;
  border: 1.5px solid #334155;
  border-radius: 12px;
  color: #f8fafc;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  outline: none;
}

.modal input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal input::placeholder {
  color: #475569;
}

.modal button {
  margin-top: 24px;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-salvar {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    margin:10px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-cancelar {
    background: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
}

/* Animações */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsivo */
@media (max-width: 640px) {
  .modal {
    padding: 24px;
    margin: 16px;
    width: calc(100% - 32px);
  }
  
  .modal button {
    width: 100%;
    margin-bottom: 12px;
  }
  
  .modal button:first-of-type {
    margin-right: 0;
  }
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

/* Painel gerador de senha */
.config-senha {
    margin-top: 16px;
    padding: 16px;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

/* Range slider */
.config-senha input[type="range"] {
    appearance: none;
    -webkit-appearance: none;
    width: 100%;
    height: 4px;
    background: #334155;
    border-radius: 4px;
    outline: none;
    border: none;
    padding: 0;
    margin: 0;
}

.config-senha input[type="range"]::-webkit-slider-thumb {
    appearance: none;
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    background: #3b82f6;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
}

.config-senha input[type="range"]::-webkit-slider-thumb:hover {
    transform: scale(1.2);
    background: #2563eb;
}

/* Linha do tamanho */
.config-linha-tamanho {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.config-linha-tamanho span {
    color: #3b82f6;
    font-weight: 700;
    font-size: 0.9rem;
    min-width: 64px;
    text-align: right;
}

/* Checkboxes */
.config-senha label {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #cbd5e1;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    text-transform: none;
    margin: 0;
    letter-spacing: 0;
}

.config-senha input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: #3b82f6;
    cursor: pointer;
    border-radius: 4px;
    padding: 0;
    margin: 0;
}

/* Botão gerar */
.btn-gerar {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    margin-top: 4px !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
}

.btn-gerar:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4) !important;
}

/* Botão abrir gerador */
.btn-gerador {
    background: #1e293b !important;
    color: #6366f1 !important;
    border: 1px solid #6366f1 !important;
    margin-top: 16px !important;
}

.btn-gerador:hover {
    background: #6366f1 !important;
    color: white !important;
}
</style>