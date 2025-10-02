// Variável para guardar o estado anterior dos atendimentos
let atendimentosAnteriores = {};

const socket = io(URL_WEBSOCKET);

// Função para buscar e renderizar a fila de espera e guichês
async function fetchAndRenderQueue() {
    const queueContainer = document.getElementById('fila-de-espera');
    const atendendoContainer = document.getElementById('guiches_atendimento');

    try {
        const response = await fetch(`${API_URL_NODE}/painel`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Dados recebidos:", data);
        
        queueContainer.innerHTML = '';
        if (atendendoContainer) {
            atendendoContainer.innerHTML = '';
        }

        // Renderizar a Fila de Espera
        if (data.fila_de_espera && data.fila_de_espera.length > 0) {
            data.fila_de_espera.slice(0, 4).forEach(item => {
                const queueItem = document.createElement('div');
                queueItem.className = 'fila-item';
                queueItem.innerHTML = `<span class="senha-numero">${item.numero}</span>`;
                if (item.tipo) {
                    const tipoElement = document.createElement('span');
                    tipoElement.className = 'senha-tipo';
                    tipoElement.textContent = ` (${item.tipo})`;
                    queueItem.appendChild(tipoElement);
                }
                queueContainer.appendChild(queueItem);
            });
        } else {
            queueContainer.innerHTML = '<p>Nenhuma senha na fila.</p>';
        }
    
        // Renderizar TODOS os Guichês dinamicamente
        if (atendendoContainer && data.guiches_disponiveis) {
            const atendimentos = data.guiches_atendimento || [];

            data.guiches_disponiveis.forEach(guiche => {
                // CORREÇÃO 1: Usar guiche.nome para a comparação
                const atendimentoAtual = atendimentos.find(at => at.guiche_nome === guiche.nome);
                const guicheItem = document.createElement('div');
                
                if (atendimentoAtual) {
                    const nomeGuiche = atendimentoAtual.guiche_nome;
                    const senhaAnterior = atendimentosAnteriores[nomeGuiche];
                    const senhaAtual = atendimentoAtual.numero;

                    guicheItem.className = 'guiche-item';

                    if (!senhaAnterior || senhaAnterior !== senhaAtual) {
                        guicheItem.classList.add('chamada-recente');
                    }

                    guicheItem.innerHTML = `
                        <h3>${atendimentoAtual.guiche_nome}</h3>
                        <div class="guiche_card">
                            Senha: <span class="senha-numero">${senhaAtual}</span>
                            ${atendimentoAtual.tipo ? `(${atendimentoAtual.tipo})` : ''}
                        </div>
                    `;
                } else {
                    guicheItem.className = 'guiche-item';
                    // CORREÇÃO 2: Usar guiche.nome para exibir o nome do guichê livre
                    guicheItem.innerHTML = `
                        <h3>${guiche.nome}</h3>
                        <div class="guiche_card guiche-livre">
                            <span>Livre</span>
                        </div>
                    `;
                }
                atendendoContainer.appendChild(guicheItem);
            });
        }

        // ATUALIZA O ESTADO ANTERIOR
        const novoEstado = {};
        if (data.guiches_atendimento) {
            data.guiches_atendimento.forEach(at => {
                novoEstado[at.guiche_nome] = at.numero;
            });
        }
        atendimentosAnteriores = novoEstado;

    } catch (error) {
        console.error("Falha ao buscar a fila:", error);
        if(atendendoContainer) {
            atendendoContainer.innerHTML = `<p style="color: red;">Erro ao carregar dados.</p>`
        }
    }
}

function atualizarRelogio() {
    const agora = new Date();
    const horas = String(agora.getHours()).padStart(2, '0');
    const minutos = String(agora.getMinutes()).padStart(2, '0');
    const segundos = String(agora.getSeconds()).padStart(2, '0');
    const horaAtual = `${horas}:${minutos}:${segundos}`;
    document.getElementById('relogio').textContent = horaAtual;
    const opcoes = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dataFormatada = agora.toLocaleDateString('pt-BR', opcoes);
    document.getElementById('date').textContent = dataFormatada;
}

async function inicializar_painel() {
    await fetchAndRenderQueue();
    setInterval(atualizarRelogio, 1000);
    atualizarRelogio();
}

socket.on('fila_atualizada', async () => {
    console.log("Evento 'fila atualizada' recebido! Atualizando painel");
    await fetchAndRenderQueue();
});

inicializar_painel();