const socket = io(URL_WEBSOCKET);

// Função para buscar e renderizar a fila de espera
async function fetchAndRenderQueue() {
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
    
    // Contêineres
    const queueContainer = document.getElementById('fila-de-espera');
    const atendendoContainer = document.getElementById('guiches_atendimento');
    const disponiveisContainer = document.getElementById('guiches_disponiveis');

    // Limpa os contêineres antes de renderizar novamente
    queueContainer.innerHTML = '';
    atendendoContainer.innerHTML = '';
    disponiveisContainer.innerHTML = '';

    // 1. Renderizar a Fila de Espera
    if (data.fila_de_espera && data.fila_de_espera.length > 0) {
        data.fila_de_espera.forEach(item => {
            const queueItem = document.createElement('div');
            queueItem.className = 'fila-item';
            queueItem.innerHTML = `<span class="senha-numero">${item.numero}</span>`;
            if (item.tipo) {
                const tipoElement = document.createElement('span');
                tipoElement.className = 'senha-tipo';
                tipoElement.textContent = item.tipo;
                queueItem.appendChild(tipoElement);
            }
            queueContainer.appendChild(queueItem);
        });
    } else {
        queueContainer.innerHTML = '<p>Nenhuma senha na fila.</p>';
    }

    // 2. Renderizar Guichês em Atendimento
    if (data.guiches_atendimento && data.guiches_atendimento.length > 0) {
        data.guiches_atendimento.forEach(item => {
            const atendendoItem = document.createElement('div');
            atendendoItem.className = 'guiche-atendimento-item';
            atendendoItem.innerHTML = `
                <h4>Guichê ${item.guiche_nome}</h4>
                <p>Senha: <span class="senha-numero">${item.numero}</span> (${item.tipo})</p>
            `;
            atendendoContainer.appendChild(atendendoItem);
        });
    } else {
        atendendoContainer.innerHTML = '<p>Nenhum guichê em atendimento.</p>';
    }

    // 3. Renderizar Guichês Disponíveis
    if (data.guiches_disponiveis && data.guiches_disponiveis.length > 0) {
        data.guiches_disponiveis.forEach(item => {
            const disponivelItem = document.createElement('div');
            disponivelItem.className = 'guiche-disponivel-item';
            disponivelItem.innerHTML = `<p>${item.nome}</p>`;
            disponiveisContainer.appendChild(disponivelItem);
        });
    } else {
        disponiveisContainer.innerHTML = '<p>Nenhum guichê disponível.</p>';
    }

  } catch (error) {
    console.error("Falha ao buscar a fila:", error);
  }
}


async function inicializar_painel() {
    await fetchAndRenderQueue();
}

socket.on('fila_atualizada', async () =>{
    console.log("Evento 'fila atualizada' recebido! Atualizando painel");

    await fetchAndRenderQueue();    
});

inicializar_painel();

// document.addEventListener('DOMContentLoaded', function() {
//   const btn = document.getElementById('animar-btn');
//   const topo = document.getElementById('painel-topo-texto');
//   const guiche1 = document.getElementById('guiche1-conteudo');
//   if (btn && topo-texto && guiche1) {
//     btn.addEventListener('click', function() {
//       // Fade out topo-texto
//       topo.classList.add('fade-out');
//       setTimeout(() => {
//         topo.style.visibility = 'hidden';
//         // Fade in no guiche
//         guiche1.textContent = topo-texto.textContent;
//         guiche1.classList.add('fade-in');
//         setTimeout(() => {
//           guiche1.classList.remove('fade-in');
//         }, 700);
//       }, 700);
//     });
//   }
// });