/*------------------Atendente------------------*/
const socket = io(URL_WEBSOCKET);

let queue = [];
let currentCustomer = null;

// Funcoes assincronas para a API

// Retorna a fila completa em espera
async function fetchQueue() {
    try{
        const response = await fetch(API_URL_FLASK);
        if (!response.ok){
            throw new error(`Erro de rede: ${response.status}'`);
        }
        queue = await response.json()
    }catch (error){
        console.error("Falha ao requisitar a fila :", error);
    }
}

// Deleta um cliente
async function del_client(ticket_id) {
    try{
        const response = await fetch(`${API_URL_NODE}/remover/${ticket_id}`, {method: 'POST'});
        if (!response){
            throw new Error(`Erro de rede ao remover cliente : ${ticket_id}`)
        }
        const result = await response.json();
    }catch (error){
        console.error("Falha ao remover: ", error);
    }
}

// Chamar o proximo da fila
async function call_client(clienteSelecionado) {
    try{
        const response = await fetch(`${API_URL_NODE}/chamar/${clienteSelecionado.id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                guiche_id: APP_DATA.guiche_id,
                guiche_nome: APP_DATA.guiche_nome
            })
        });

        // Verificacao do status da resposta da requisicao
        if (!response.ok){
            throw new Error(`Erro de rede ao chamar cliente : ${ticket_id}`)
        }

        // Se a requisição correr bem, a mudança é feita na fila local
        currentCustomer = clienteSelecionado;

        queue = queue.filter(c => c.id !== clienteSelecionado);

        // Renderizacao da interface novamente, pois a requisicao e atualizacao local foi feita com sucesso
        renderizarClienteEmAtendimento();
        renderizarFilas();
        atualizarContagemDaFila();

        // Chama o proximo cliente
        alert(`CLiente ${clienteSelecionado.numero} chamado para atendimento!`);
    }catch (error){
        console.error("Falha ao chamar cliente: ", error);
        alert("Falha ao chamar cliente. Tente novamente");
    }
}

// Envio diretamente para o flask
async function verificar_cliente_em_atendimento() {
    try{
        const response = await fetch(`${API_URL_FLASK}/em-atendimento`);
        if (!response.ok){
            throw new Error(`Erro de rede, nao foi possivel pegar o cliente em atendimento: ${response.status}`);
        }

        const customer = await response.json();
        if (customer.id){
            currentCustomer = customer;
        }else{
            currentCustomer = null;
        }
    }catch (error){
        console.error("Error: erro ao carregar cliente em atendimento : ", error);
    }
}

// Atualiza o relógio em tempo real
function atualizarTempo() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('pt-BR');
    document.getElementById('current-time').textContent = timeString;
}

// Atualiza o contador da fila (total de clientes aguardando)
function atualizarContagemDaFila() {
    document.getElementById('queue-count').textContent = queue.length;
}

// Renderiza o cliente em atendimento
function renderizarClienteEmAtendimento() {
    const container = document.getElementById('current-customer');
    
    if (!currentCustomer) {
        container.className = 'current-customer';
        container.innerHTML = `
            <div class="empty-state">
                <h3>Nenhum cliente em atendimento</h3>
                <p>Chame o próximo da fila para iniciar</p>
            </div>
        `;
        return;
    }

    container.className = 'current-customer active';
    container.innerHTML = `
        <h3>Em Atendimento</h3>
        ${currentCustomer.tipo === "PRIORITARIO" ? '<span class="badge">Prioridade</span>' : '<span class="badge-normal">Normal</span>'}
        <div class="customer-info">
            <div class="customer-number">${currentCustomer.numero}</div>
        </div>
        <button class="btn btn-success" onclick="finalizarAtendimento()">Finalizar Atendimento</button>
    `;
}

function renderizarFila(fila, elementId, tipoFila) {
    const container = document.getElementById(elementId);
    // Encontra o elemento que realmente contém a lista da fila
    const filaLista = container.querySelector('.fila-lista'); 

    if (fila.length === 0) {
        filaLista.innerHTML = `
            <div class="empty-state">
                <p>Aguardando novos clientes</p>
            </div>
        `;
        return;
    }

    filaLista.innerHTML = fila.map((customer, index) => `
        <div class="queue-item ${index === 0 ? 'next-customer' : ''} ${customer.tipo === "PRIORITARIO" ? 'priority' : ''}">
            <div>
                <strong>${customer.numero}</strong>
                ${customer.tipo === "PRIORITARIO" ? '<span class="badge">Prioridade</span>' : '<span class="badge-normal">Normal</span>'}
            </div>
            <div class="container-botoes-atendimento">
                <button class="funcao-btn-atendimento" style="background-color: #28a755ff;" onclick="chamarCliente('${tipoFila}', ${index})">Chamar</button>
                <button class="funcao-btn-atendimento" style="background-color: rgba(255, 0, 0, 1);" onclick="removerClienteDaFila(${customer.id}, '${customer.numero}')">Remover</button>
            </div>
        </div>
    `).join('');
    
}

// Função para separar as filas
function getFilasSeparadas() {
    const prioritarios = queue.filter(c => c.tipo === "PRIORITARIO");
    const normais = queue.filter(c => c.tipo === "NORMAL");
    return { prioritarios, normais };
}

// Função que chama um cliente específico da fila
function chamarCliente(tipoFila, index = 0) {
    const { prioritarios, normais } = getFilasSeparadas();
    const fila = tipoFila === "PRIORITARIO" ? prioritarios : normais;

    if (fila.length === 0 || currentCustomer) {
        alert(currentCustomer ? 'Finalize o atendimento atual primeiro' : `Fila ${tipoFila} vazia`);
        return;
    }

    const clienteSelecionado = fila[index];

    if (confirm(`Deseja atender ${clienteSelecionado.numero}?`)) {
        // Somente chama a funcao responsavel pela modificacao local e remota da fila
        call_client(clienteSelecionado)

    }
}

// Remove cliente da fila de espera
function removerClienteDaFila(id_cliente, senha_cliente) {
    if (confirm(`Deseja realmente remover o cliente '${senha_cliente}' da fila de espera?`)) {
        
        // Remove do array principal
        queue = queue.filter(c => c.id !== id_cliente);
        del_client(id_cliente);
        alert(`Cliente removido: ID: ${id_cliente}, SENHA: ${senha_cliente}`);
        atualizarContagemDaFila();
        renderizarFilas();
    }
}

// Finaliza o atendimento do cliente atual
function finalizarAtendimento() {
    if (!currentCustomer) return;
    
    if(confirm("Deseja finalizar o atendimento?")){
        alert(`Atendimento de ${currentCustomer.numero} finalizado com sucesso`);
        del_client(currentCustomer.id);

        currentCustomer = null;

        renderizarClienteEmAtendimento();
        renderizarFilas();
        atualizarContagemDaFila();
    }
    else{
        return;
    }

}

// Renderiza todas as filas
function renderizarFilas() {
    const { prioritarios, normais } = getFilasSeparadas();
    renderizarFila(prioritarios, "fila-prioritarios", "PRIORITARIO");
    renderizarFila(normais, "fila-normais", "NORMAL");
}

// Inicialização
async function init() {

    await verificar_cliente_em_atendimento();
    await fetchQueue();
    renderizarClienteEmAtendimento();
    renderizarFilas();

    atualizarContagemDaFila();
    atualizarTempo();
    setInterval(atualizarTempo, 1000);
}

socket.on('fila_atualizada', async () =>{
    console.log("Evento 'fila atualizada' recebido! Atualizando interface...");
    await verificar_cliente_em_atendimento();
    await fetchQueue();
    renderizarClienteEmAtendimento();
    renderizarFilas();
    atualizarContagemDaFila();
});


init();
/*------------------Fim Atendente------------------*/
