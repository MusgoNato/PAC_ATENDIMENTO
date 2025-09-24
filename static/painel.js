const TODOS_OS_GUICHES = [
    { guiche_nome: 'Guiche 1' },
    { guiche_nome: 'Guiche 2' },
    { guiche_nome: 'Guiche 3' },
    // Adicione mais guichês aqui se necessário, ex: { guiche_nome: '04' }
];

// Variável para guardar o estado anterior dos atendimentos
let atendimentosAnteriores = {};

const socket = io(URL_WEBSOCKET);

// Função para buscar e renderizar a fila de espera e guichês
async function fetchAndRenderQueue() {
    // Declaramos as variáveis aqui, no início da função, para que sempre existam.
    const queueContainer = document.getElementById('fila-de-espera');
    const atendendoContainer = document.getElementById('guiches_atendimento');

    try {
        const response = await fetch(`${API_URL_NODE}/painel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        
        const data = await response.json();
        console.log(data);
        
        // Limpa os contêineres antes de renderizar novamente
        queueContainer.innerHTML = '';
        if (atendendoContainer) {
            atendendoContainer.innerHTML = '';
        }

        // 1. Renderizar a Fila de Espera
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
    
        // 2. Renderizar TODOS os Guichês (em atendimento ou livres)
        if (atendendoContainer) {
            const atendimentos = data.guiches_atendimento || [];

            TODOS_OS_GUICHES.forEach(guiche => {
                const atendimentoAtual = atendimentos.find(at => at.guiche_nome === guiche.guiche_nome);

                const guicheItem = document.createElement('div');
                
                if (atendimentoAtual) {
                    // --- LÓGICA DA ANIMAÇÃO ---
                    const nomeGuiche = atendimentoAtual.guiche_nome;
                    const senhaAnterior = atendimentosAnteriores[nomeGuiche];
                    const senhaAtual = atendimentoAtual.numero;

                    guicheItem.className = 'guiche-item'; // Define a classe base

                    // Compara a senha atual com a anterior para este guichê
                    if (!senhaAnterior || senhaAnterior !== senhaAtual) {
                        // Se não havia senha antes OU se a senha mudou, é uma nova chamada!
                        guicheItem.classList.add('chamada-recente');
                    }
                    // --- FIM DA LÓGICA DA ANIMAÇÃO ---

                    guicheItem.innerHTML = `
                        <h3>${atendimentoAtual.guiche_nome}</h3>
                        <div class="guiche_card">
                            Senha: <span class="senha-numero">${senhaAtual}</span>
                            ${atendimentoAtual.tipo ? `(${atendimentoAtual.tipo})` : ''}
                        </div>
                    `;
                } else {
                    // Se não encontrou, o guichê está LIVRE
                    guicheItem.className = 'guiche-item'; // Garante a classe base
                    guicheItem.innerHTML = `
                        <h3>${guiche.guiche_nome}</h3>
                        <div class="guiche_card guiche-livre">
                            <span>Livre</span>
                        </div>
                    `;
                }
                atendendoContainer.appendChild(guicheItem);
            });
        }

        // ATUALIZA O ESTADO ANTERIOR PARA A PRÓXIMA COMPARAÇÃO
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

// Inicializa o painel quando o script carregar
inicializar_painel();